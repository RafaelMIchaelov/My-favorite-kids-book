"""Build the chapter 1 storyboard review page (production/review/index.html) from template.html and pages.json.

Publish index.html as a claude.ai artifact with capabilities {db:{}, user:{}} and these files:
frames/thumb/<name>.jpg -> assets/frames/ch01/thumb/<name>.jpg and frames/full/<name>.webp -> assets/frames/ch01/full/<name>.webp.
Picks are stored in the artifact's db collection "picks" (doc id = page id, {variant, model, at}), notes in "notes" ({text, at}).
"""
import json
import pathlib

here = pathlib.Path(__file__).parent
template = (here / "template.html").read_text(encoding="utf-8")
pages = json.loads((here / "pages.json").read_text(encoding="utf-8"))
payload = json.dumps(pages, ensure_ascii=False).replace("</", "<\\/")
(here / "index.html").write_text(template.replace("__PAGES__", payload), encoding="utf-8")
print(f"index.html: {len(pages)} pages")
