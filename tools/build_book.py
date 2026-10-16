#!/usr/bin/env python3
"""Build books/<id>/book.js from books/<id>/story.json and books/<id>/art/*.svg.

Usage: python3 tools/build_book.py <id> [--chapter N]

story.json fields: seriesTitle, bookTitle, subtitle, blurb, pages[{text}],
teaser, questions[], nextChapters[{title, anchor}], sourcesNotes.
Art: art/cover.svg and art/p01.svg, p02.svg ... (one per page).
A page's background color is read from a "<!-- bg:#xxxxxx -->" comment in its SVG.
"""
import json, re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
book_id = sys.argv[1]
chapter = int(sys.argv[sys.argv.index("--chapter") + 1]) if "--chapter" in sys.argv else 1
d = root / "books" / book_id
story = json.loads((d / "story.json").read_text(encoding="utf-8"))

def svg(name):
    s = (d / "art" / name).read_text(encoding="utf-8")
    s = re.sub(r"<\?xml[^>]*\?>", "", s).strip()
    return s

def bg(s):
    m = re.search(r"bg:\s*(#[0-9a-fA-F]{3,8})", s)
    return m.group(1) if m else "#FBF6EC"

pages = []
for i, p in enumerate(story["pages"], 1):
    art = svg(f"p{i:02d}.svg")
    pages.append({"text": p["text"], "bg": bg(art), "art": art})

book = {
    "id": book_id,
    "series": story["seriesTitle"],
    "chapter": chapter,
    "title": story["bookTitle"],
    "subtitle": story["subtitle"],
    "blurb": story["blurb"],
    "cover": svg("cover.svg"),
    "pages": pages,
    "teaser": story["teaser"],
    "questions": story["questions"],
    "nextChapters": story["nextChapters"],
    "sourcesNotes": story.get("sourcesNotes", ""),
}
out = "// נוצר אוטומטית על ידי tools/build_book.py — לערוך את story.json ואת art/*.svg\n"
out += "window.registerBook(" + json.dumps(book, ensure_ascii=False, indent=1) + ");\n"
(d / "book.js").write_text(out, encoding="utf-8")
print(f"wrote {d / 'book.js'} ({len(out)//1024} KB, {len(pages)} pages)")
