"""Build downloadable PDFs of the picture books.

Each book becomes one PDF: a cover card, one card per page (illustration on top, words below,
page number in digits), the closing page (moral or teaser and questions) and the parents' notes.
The layout follows the flip-book readers. Chromium (Playwright) does the typesetting, so the
Hebrew niqqud is shaped exactly as in the browser; the fonts are the local copies in fonts/.

Usage: python3 production/pdf/build_pdf.py <book-id> [<book-id> ...]   (ids: see BOOKS)
Writes downloads/<file>.pdf. Needs Pillow and Node with Playwright (print.js).
"""
import html
import json
import pathlib
import subprocess
import sys

from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = ROOT / "production/pdf"
BUILD = HERE / ".build"   # working files (JPEG copies, HTML), not committed
OUT = ROOT / "downloads"


def jpg(src: pathlib.Path) -> str:
    """Re-encode an illustration as JPEG once (Chromium embeds JPEG as is, which keeps the PDF small)."""
    BUILD.mkdir(exist_ok=True)
    dst = BUILD / (src.parent.parent.name + "-" + src.stem + ".jpg")
    if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
        Image.open(src).convert("RGB").save(dst, "JPEG", quality=85, optimize=True, progressive=True)
    return dst.as_uri()


def esc(s: str) -> str:
    return html.escape(s or "", quote=True).replace(" —", " —")


def fonts_css() -> str:
    """The Google Fonts CSS with each font file inlined (a file:// page may not load fonts from disk)."""
    import base64, re
    css = (HERE / "fonts/fonts.css").read_text(encoding="utf-8")
    return re.sub(r"url\(([^)]+\.woff2)\)", lambda m: "url(data:font/woff2;base64,%s)" % base64.b64encode((HERE / "fonts" / m.group(1)).read_bytes()).decode(), css)


def svg_const(name: str, template: str) -> str:
    start = template.index(f"const {name} = '") + len(f"const {name} = '")
    return template[start:template.index("';", start)]


# ---------------------------------------------------------------- books

def book_yud_ch01():
    pages = json.loads((ROOT / "production/review/pages.json").read_text(encoding="utf-8"))
    story = json.loads((ROOT / "books/yud-vayaal/story.json").read_text(encoding="utf-8"))
    redrawn = json.loads((ROOT / "production/ch01-yud2.json").read_text(encoding="utf-8"))["picks"]
    frames = ROOT / "assets/frames/ch01/full"

    def img(p):  # edition Y (the letter-shaped Yud), version C where a page has no Y
        return jpg(frames / f"{p['id']}_{'Y' if p['id'] in redrawn else 'C'}.webp")

    cover, rest = pages[0], pages[1:]
    wordplay = ('<div class="wordplay" aria-hidden="true"><span class="wp-a">וְעַל</span><span class="wp-plus">+ י</span>'
                '<span class="wp-b">וְ<span class="wp-yud">יָ</span>עַל</span></div>')
    return {
        "file": "יוד-הקטנה-פרק-א-המילה-האחרונה.pdf",
        "title": "יוּד הַקְּטַנָּה · הַמִּלָּה הָאַחֲרוֹנָה",
        "cover": {"img": img(cover), "series": "יוּד הַקְּטַנָּה", "title": cover["text"], "sub": "פֶּרֶק א׳", "band": cover["sub"]},
        "orn": '<span class="orn-yud">י</span>',
        "pages": [{"num": int(p["num"]), "img": img(p), "text": p["text"], "quiet": "" if p["text"] else "עַמּוּד בְּלִי מִלִּים",
                   "overlay": wordplay if p["id"] == "p12" else ""} for p in rest],
        "end": {"icon": f'<img class="end-icon" src="{(ROOT / "production/reader/yud-joy.webp").as_uri()}" alt="">',
                "title": "סוֹף פֶּרֶק א׳", "teaser": story["teaser"], "questions": story["questions"],
                "extra": "הַפֶּרֶק הַבָּא: " + story["nextChapters"][0]["title"]},
        "notes": [{"num": int(p["num"]), "layers": ([["מקור", p["source"]]] if p.get("source") else []) + p["layers"]}
                  for p in rest if p["layers"] or p.get("source")],
    }


def book_from_story(story_path, state_path, frames_dir, reader_template, file, series, cover_sub, orn_const, end_const):
    story = json.loads((ROOT / story_path).read_text(encoding="utf-8"))
    picks = json.loads((ROOT / state_path).read_text(encoding="utf-8"))["picks"]
    frames = ROOT / frames_dir
    tpl = (ROOT / reader_template).read_text(encoding="utf-8")
    pages = story["pages"]
    return {
        "file": file,
        "title": story["bookTitle"],
        "cover": {"img": jpg(frames / f"{picks['cover']}.webp"), "series": series, "title": story["bookTitle"], "sub": cover_sub,
                  "band": story["blurb"]},
        "orn": svg_const(orn_const, tpl).replace('width="1.35em" height="1.35em"', 'class="orn-svg"'),
        "pages": [{"num": n, "img": jpg(frames / f"{picks[p['id']]}.webp"), "text": p["text"], "quiet": "", "overlay": ""}
                  for n, p in enumerate(pages, 1)],
        "end": {"icon": f'<span class="end-icon">{svg_const(end_const, tpl)}</span>', "title": "סוֹף",
                "teaser": story["moral"], "questions": story["questions"], "extra": ""},
        "notes": [{"num": n, "layers": ([["מקור", story["source"]]] if n == 1 and story.get("source") else []) + p.get("layers", [])}
                  for n, p in enumerate(pages, 1) if p.get("layers") or (n == 1 and story.get("source"))],
    }


BOOKS = {
    "yud-ch01": book_yud_ch01,
    "meah-zraim": lambda: book_from_story(
        "books/meah-zraim/story.json", "production/meah-zraim.json", "assets/frames/meah-zraim/full",
        "production/reader-meah-zraim/template.html", "מאה-זרעים.pdf", "מָשָׁל", "מֶלֶךְ, נְסִיכָה וְעָצִיץ קָטָן", "SPROUT", "POT"),
    "tof-miriam": lambda: book_from_story(
        "books/tof-miriam/story.json", "production/tof-miriam.json", "assets/frames/tof-miriam/full",
        "production/reader-tof-miriam/template.html", "התוף-של-מרים.pdf", "סִפּוּר מִן הַתּוֹרָה",
        "אָחוֹת גְּדוֹלָה, תֵּבָה קְטַנָּה וְתִקְוָה גְּדוֹלָה", "DRUM", "DRUM_BIG"),
}

# ---------------------------------------------------------------- page

CSS = """
@page{size:150mm 255mm;margin:0}
:root{--paper:#FBF6EC;--ink:#24305E;--soft:#5B6386;--gold:#A86A12;--edge:#E2D4B8;
  --serif:"Frank Ruhl Libre","Noto Serif Hebrew",serif;--sans:"Rubik","Assistant",sans-serif}
*{box-sizing:border-box}
html,body{margin:0;background:var(--paper);color:var(--ink)}
body{font-family:var(--serif);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.card{position:relative;width:150mm;height:255mm;overflow:hidden;break-after:page;background:var(--paper)}
.pic{position:absolute;inset:0 0 auto 0;height:200.9mm;overflow:hidden;container-type:inline-size}
.pic>img{display:block;width:100%;height:100%;object-fit:cover}
.words{position:absolute;inset:200.9mm 0 0 0;display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:2.6mm;padding:3.2mm 13mm 9.5mm;text-align:center}
.orn{display:flex;align-items:center;gap:2.4mm;color:var(--gold);font-size:15pt;line-height:1}
.orn::before,.orn::after{content:"";width:13mm;height:.25mm;background:currentColor;opacity:.55}
.orn-yud{font-family:var(--serif);font-weight:700}
.orn-svg{width:7.2mm;height:7.2mm;display:block}
.line{font-weight:500;font-size:15.5pt;line-height:1.55;margin:0;max-width:118mm;text-wrap:balance}
.line.quiet{font-size:11pt;color:var(--soft)}
.band{font-size:12.5pt;line-height:1.6;color:var(--soft);margin:0;max-width:118mm;text-wrap:balance}
.folio{position:absolute;bottom:4mm;left:0;right:0;text-align:center;font-weight:700;font-size:10.5pt;color:var(--gold)}
/* cover title over the sky, as in the reader */
.cover-title{position:absolute;inset:0 0 auto 0;container-type:inline-size;display:flex;flex-direction:column;align-items:center;gap:.4em;
  text-align:center;padding:7% 8% 20%;color:#FBF6EC;background:linear-gradient(to bottom,rgba(11,17,40,.74),rgba(11,17,40,.42) 62%,rgba(11,17,40,0))}
.c-series{font-family:var(--sans);font-size:3.3cqw;letter-spacing:.14em;color:#F2C66F}
.c-title{font-family:var(--serif);font-weight:900;font-size:11.5cqw;line-height:1.08;margin:0;text-wrap:balance;text-shadow:0 2px 14px rgba(0,0,0,.35)}
.c-sub{font-family:var(--serif);font-weight:500;font-size:4.6cqw;color:#F6E7C8}
/* the page-12 word play of יוד הקטנה */
.wordplay{position:absolute;top:14%;bottom:30%;right:5%;width:41%;container-type:inline-size;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:.1em;font-family:var(--serif);color:var(--ink)}
.wp-a{font-size:29cqw;font-weight:700;line-height:1.1;opacity:.5}
.wp-plus{font-family:var(--sans);font-size:11cqw;font-weight:600;color:#7A4E05;line-height:1.2}
.wp-b{font-size:33cqw;font-weight:900;line-height:1.15}
.wp-yud{display:inline-block;color:#E9A23B;transform:translateY(-.2em);-webkit-text-stroke:.025em #24305E;paint-order:stroke fill}
/* closing page */
.end{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5mm;padding:16mm 15mm;text-align:center}
.end-icon{display:block;width:30mm;height:auto}
.end-icon svg{display:block;width:100%;height:auto}
.end-title{font-weight:900;font-size:24pt;line-height:1.1;margin:0}
.end-teaser{font-size:13pt;line-height:1.65;color:var(--soft);margin:0;max-width:112mm;text-wrap:balance}
.rule{width:40mm;height:.25mm;background:var(--edge)}
.end-h{font-weight:700;font-size:14pt;margin:0;color:var(--gold)}
.qs{margin:0;padding:0;list-style:none;display:flex;flex-direction:column;gap:3.4mm;max-width:116mm}
.qs li{font-size:12.5pt;line-height:1.6}
.qs li::before{content:attr(data-n) ". ";color:var(--gold);font-weight:700}
.extra{font-family:var(--sans);font-size:10pt;color:var(--soft);margin:0}
/* parents' notes */
.notes{padding:13mm 12.5mm 13mm}
.notes-h{font-weight:900;font-size:19pt;margin:0 0 1mm;text-align:center}
.notes-intro{font-family:var(--sans);font-size:9.5pt;color:var(--soft);text-align:center;margin:0 0 4mm}
.note{margin:0 0 2.2mm}
.note-page{font-weight:700;font-size:11pt;color:var(--gold);margin:2mm 0 .8mm;border-bottom:.25mm solid var(--edge);padding-bottom:.6mm}
.note dt{font-family:var(--sans);font-weight:600;font-size:9pt;color:var(--gold);margin:0 0 .3mm}
.note dd{margin:0;font-size:10pt;line-height:1.46}
.notes .folio{bottom:6mm}
"""

FIT_JS = """
document.fonts.ready.then(() => {
  // shrink a page's words until they fit their band
  for (const w of document.querySelectorAll('.words')) {
    const line = w.querySelector('.line,.band'); if (!line) continue;
    let pt = parseFloat(getComputedStyle(line).fontSize) * 0.75;
    while (w.scrollHeight > w.clientHeight + 1 && pt > 11) { pt -= 0.5; line.style.fontSize = pt + 'pt'; }
  }
  // flow the parents' notes over as many cards as they need
  const src = document.getElementById('notes-src');
  if (src) {
    const items = [...src.children]; src.remove();
    const first = Number(src.dataset.folio);
    let page = null, n = 0;
    const open = () => {
      page = document.createElement('section'); page.className = 'card notes';
      if (n === 0) page.innerHTML = '<h2 class="notes-h">לַהוֹרִים</h2><p class="notes-intro">מָה מִסְתַּתֵּר בַּסִּפּוּר, עַמּוּד אַחַר עַמּוּד</p>';
      const f = document.createElement('span'); f.className = 'folio'; f.textContent = String(first + n); page.append(f);
      document.body.append(page); n++;
    };
    open();
    for (const it of items) {
      page.insertBefore(it, page.querySelector('.folio'));
      if (page.scrollHeight > page.clientHeight + 1 && page.querySelectorAll('.note').length > 1) { it.remove(); open(); page.insertBefore(it, page.querySelector('.folio')); }
    }
  }
  document.body.dataset.ready = '1';
});
"""


def render(book: dict) -> str:
    c = book["cover"]
    out = [f'<!doctype html><html lang="he" dir="rtl"><head><meta charset="utf-8"><title>{esc(book["title"])}</title>',
           f'<style>{fonts_css()}{CSS}</style></head><body>']
    out.append(f'<section class="card"><div class="pic"><img src="{c["img"]}" alt=""><div class="cover-title">'
               f'<span class="c-series">{esc(c["series"])}</span><h1 class="c-title">{esc(c["title"])}</h1>'
               f'<span class="c-sub">{esc(c["sub"])}</span></div></div>'
               f'<div class="words"><p class="band">{esc(c["band"])}</p></div></section>')
    for p in book["pages"]:
        words = f'<p class="line">{esc(p["text"])}</p>' if p["text"] else f'<p class="line quiet">{esc(p["quiet"])}</p>'
        out.append(f'<section class="card"><div class="pic"><img src="{p["img"]}" alt="">{p["overlay"]}</div>'
                   f'<div class="words"><span class="orn">{book["orn"]}</span>{words}</div>'
                   f'<span class="folio">{p["num"]}</span></section>')
    e = book["end"]
    qs = "".join(f'<li data-n="{"אבג"[i] if i < 3 else i + 1}">{esc(q)}</li>' for i, q in enumerate(e["questions"]))
    extra = f'<p class="extra">{esc(e["extra"])}</p>' if e["extra"] else ""
    out.append(f'<section class="card end">{e["icon"]}<p class="end-title">{esc(e["title"])}</p>'
               f'<p class="end-teaser">{esc(e["teaser"])}</p><span class="rule"></span>'
               f'<p class="end-h">שְׁאֵלוֹת לְשִׂיחָה</p><ol class="qs">{qs}</ol>{extra}</section>')
    if book["notes"]:
        items = []
        for nt in book["notes"]:
            for k, (label, text) in enumerate(nt["layers"]):
                head = f'<p class="note-page">עַמּוּד {nt["num"]}</p>' if k == 0 else ""
                items.append(f'<div class="note">{head}<dl><dt>{esc(label)}</dt><dd>{esc(text)}</dd></dl></div>')
        out.append(f'<div id="notes-src" data-folio="{len(book["pages"]) + 2}">{"".join(items)}</div>')
    out.append(f"<script>{FIT_JS}</script></body></html>")
    return "".join(out)


def main(ids):
    OUT.mkdir(exist_ok=True)
    for bid in ids:
        book = BOOKS[bid]()
        BUILD.mkdir(exist_ok=True)
        page = BUILD / f"{bid}.html"
        page.write_text(render(book), encoding="utf-8")
        pdf = OUT / book["file"]
        subprocess.run(["node", str(HERE / "print.js"), page.as_uri(), str(pdf)], check=True)
        print(f"{pdf.relative_to(ROOT)}: {pdf.stat().st_size / 1e6:.1f} MB, {len(book['pages'])} pages + cover, end and notes")


if __name__ == "__main__":
    main(sys.argv[1:] or ["yud-ch01", "meah-zraim"])
