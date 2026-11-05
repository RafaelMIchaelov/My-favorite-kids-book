"""Build the flip-book reader for התוף של מרים (production/reader-tof-miriam/index.html) from template.html.

Text, parents' notes, moral and questions come from books/tof-miriam/story.json; the picked illustration per page
comes from production/tof-miriam.json ("picks": page id -> frame name in assets/frames/tof-miriam/).
Publish index.html as a claude.ai artifact with img/full/<page>.webp and img/thumb/<page>.jpg mapped to the picked frames.
"""
import json
import pathlib

here = pathlib.Path(__file__).parent
root = here.parent.parent
story = json.loads((root / "books/tof-miriam/story.json").read_text(encoding="utf-8"))

pages = [{"id": "cover", "text": story["bookTitle"], "sub": story["blurb"], "source": "", "layers": []}]
for i, p in enumerate(story["pages"]):
    layers = ([["מקור", story["source"]]] if i == 0 else []) + p["layers"]
    pages.append({"id": p["id"], "text": p["text"], "sub": "", "source": "", "layers": layers})

data = {"pages": pages, "moral": story["moral"], "questions": story["questions"]}
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
template = (here / "template.html").read_text(encoding="utf-8")
(here / "index.html").write_text(template.replace("__DATA__", payload), encoding="utf-8")
print(f"index.html: {len(pages)} pages")
