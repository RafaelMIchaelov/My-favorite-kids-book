"""Build the chapter 1 flip-book reader (production/reader/index.html) from template.html.

Page text, sources, layers, variants and recommended picks come from production/review/pages.json;
the closing pages (teaser, questions, next chapter) come from books/yud-vayaal/story.json.
Publish index.html as a claude.ai artifact with these files:
img/full/<name>.webp -> assets/frames/ch01/full/<name>.webp, img/thumb/<name>.jpg -> assets/frames/ch01/thumb/<name>.jpg,
img/yud-joy.webp -> production/reader/yud-joy.webp.
"""
import json
import pathlib

here = pathlib.Path(__file__).parent
root = here.parent.parent
pages = json.loads((root / "production/review/pages.json").read_text(encoding="utf-8"))
story = json.loads((root / "books/yud-vayaal/story.json").read_text(encoding="utf-8"))

data = {
    "pages": [{k: p[k] for k in ("id", "num", "text", "sub", "source", "layers", "v", "rec")} for p in pages],
    "teaser": story["teaser"],
    "questions": story["questions"],
    "next": story["nextChapters"][0]["title"],
}
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
template = (here / "template.html").read_text(encoding="utf-8")
(here / "index.html").write_text(template.replace("__DATA__", payload), encoding="utf-8")
print(f"index.html: {len(data['pages'])} pages")
