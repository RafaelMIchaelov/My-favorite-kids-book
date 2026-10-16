"""Chapter-1 frame prompts, v2 (after art-direction critique).

Changes from v1: no layout sketch (the old sketches contradicted the briefs); one reference image = a single
Yud in the page's expression (assets/ref/ch01/yud/yud-<expr>.png); order idea > style > scene > character >
text space > avoid; positive constraints instead of naming forbidden symbols; no exact counts above four
(exact numeric hints are added later as SVG overlays); page 12 is a background plate for an SVG composite.
Run: python3 production/prompts/build_ch01_prompts_v2.py -> production/prompts/ch01_prompts_v2.json
"""
import json, pathlib

HERE = pathlib.Path(__file__).parent

STYLE = ("Style: a children's picture-book painting in flat matte gouache on warm, visibly textured paper; hand-cut "
         "shapes with slightly imperfect edges and fine hand-drawn gold line. Ancient Near-Eastern and Egyptian relief "
         "stylization: figures in profile, frieze rhythm, flat stacked space. A gentle magical boho warmth: patterned "
         "textile-like borders and a few tiny warm fairy-light specks painted as flat round dots. Calm negative space. "
         "Palette: lapis blue, midnight navy, mustard gold, terracotta, ivory, gold line, olive shadows, small teal accents.")

CHARACTER = ("Yud: copy exactly the single character in image 1, with the same silhouette, proportions and orientation: "
             "a flat deep-navy rounded head with one short thick tail pointing down to the lower left, and the same white "
             "eyes ({expr}). Add only a thin ivory outline. She has no mouth, nose, arms, legs or hands. Exactly one Yud "
             "in the picture.")

EXPR = {
    "calm": "two calm round dots",
    "sad": "two small dots set low",
    "half": "sleepy half-closed lids",
    "wide": "wide-open rings with small pupils",
    "curious": "one dot larger and higher than the other",
    "joy": "joyful closed upward arcs",
    "giggle": "squeezed giggling eyes shaped like > and <",
    "dizzy": "dizzy spirals, with three tiny gold dots circling her head",
    "determined": "two dots under short slanted brow lines",
}

TEXTSPACE = ("Keep the {area} an uninterrupted plain {surface}: only flat color and paper grain, with no moon, light, "
             "branch, figure or ornament in it.")

AVOID = ("No text, letters, numerals or script-like marks anywhere. Any moon is a full round disc; every star or light "
         "is a soft round dot, never pointed. Modest dress with long sleeves and long robes. Nothing divine is drawn: "
         "no figure, face or hand in the sky or the wind. No photorealism, no 3D rendering, no glossy gradients.")

PAGES = [
    dict(id="cover", expr="joy", area="top 30%", surface="sky",
         idea="Picture-book cover: a tiny letter-character holds a thread of gold that leads from a night of exile to a dawn of home.",
         scene=("The right half is deep night-blue Babylon: a dark glazed-brick wall with one plain palmette band above a still "
                "canal. The left half is a golden dawn over pale limestone hills of Jerusalem with a few olive trees and one gold "
                "palm. A thin line of travelers in profile (wrapped headcloths, long mantles) winds over the dunes from right to "
                "left toward the dawn. In the center foreground Yud rests upright on a dune crest, about 18% of the image height; "
                "a fine glowing gold thread curls once around the tip of her tail and runs behind her to the right across the "
                "picture, ending at a tiny warm amber ember at the far right edge. One small round white point of light glows "
                "just above Yud. A thin gold palmette-lotus border frames the whole cover."),
         extra="No title or lettering; no crowd."),
    dict(id="p01", expr="calm", area="upper 40%", surface="deep-blue paper",
         idea="At the very end of a great scroll that looks like a sleeping city, one tiny window is still lit, and the smallest letter lives inside it.",
         scene=("Wide view, slightly from above, on deep night-blue paper. In the lower 60% of the picture lies a vast open scroll "
                "drawn as a sleeping city: many long horizontal rows of soft ivory dashes and little blocks, like streets of tiny "
                "dark houses, fading out toward the right. At the far lower left, at the very end of the last row, one single "
                "warm-lit window the size of a word glows gold; Yud sits inside it like a child at a lit window, about 9% of the "
                "image height. On the window sill lies one small black feather, a silhouette against the glow. At the right end of "
                "the top row, one tiny faint amber ember glows, warm and not white. An almost invisible gold thread runs along the "
                "margin from the window to the ember. The lit window is the only bright point of light. A thin gold palmette-lotus "
                "band runs along the bottom edge."),
         extra="No book or codex; no sparkle clusters."),
    dict(id="p02", expr="sad", area="upper 35%", surface="night sky",
         idea="By the rivers of Babylon at night, the exiles sit in a row and weep, remembering Zion.",
         scene=("Low, wide view across a still night canal. On the far bank a long, flat-topped dark-blue glazed-brick wall spans "
                "edge to edge like a shut door, with one plain band of palmettes; its skyline is one straight line. On the near bank "
                "below it, a thin frieze-like row of seated Judean exiles in profile (wrapped headcloths, long mantles, long veils "
                "for the women), heads bowed, all facing left. At the far left end of the row stands one small low mud-brick house "
                "whose single doorway glows a faint warm amber. In the foreground right a dark poplar branch crosses the frame; on it "
                "sits Yud, about 12% of the image height, her head drooping forward. A round pale full moon sits low on the left, "
                "just above the far wall; its reflection on the still water is the one white point of light. A band of many faint "
                "tiny ivory dots floats on the water, far dimmer than the reflection. The deepest night-blue of the book."),
         extra="No tears, no chains, no animals on the wall."),
    dict(id="p03", expr="half", area="lower-right 40%", surface="dark gouache",
         idea="Three old lyres hang silent on a poplar branch, and the little letter waits.",
         scene=("Close-up. One poplar branch runs diagonally across the upper part of the picture, from the upper right toward the "
                "middle left. From it hang three ancient Near-Eastern lyres (kinnor) of different sizes, all in the upper-left two "
                "thirds of the picture: asymmetric wooden frames with two arms and a crossbar, slack dusty strings, utterly still; "
                "the middle lyre is the largest. Yud sits on the crossbar of the middle lyre, slumped low, about 11% of the image "
                "height. A single round moon-glint on one string of the middle lyre is the point of light. Night-blue and silent. "
                "A thin gold palmette-lotus band along the top edge."),
         extra="Lyres only, never Greek or Celtic harps; no musical notes; no people."),
    dict(id="p04", expr="wide", area="upper-left corner", surface="night sky",
         idea="At midnight a single ribbon of golden wind sweeps through the exile camp and wakes everything it touches.",
         scene=("Wide wordless spread. One single ribbon of pale-gold night wind, finely outlined in gold, enters from the right "
                "edge and sweeps toward the left. The wind is seen only in what it bends: poplar leaves turning, a round teardrop "
                "oil-lamp flame leaning sideways, the flap of a black goat-hair tent lifting, one lyre string vibrating. Yud, on a "
                "swinging lyre at mid-left, about 10% of the image height, is jolted upright, eyes wide. The vibrating string glows "
                "as one round soft white glint, the point of light. A small round pale moon at the top center. On the dark horizon "
                "an arch formed by two palm trees catches a sliver of gold. Night-blue with the first breath of pale gold."),
         extra="Only one ribbon; no storm, no lightning, no visible source of the wind."),
    dict(id="p05", expr="determined", area="upper-right 35%", surface="night sky",
         idea="The golden wind flows into the one lit opening of the Persian king's palace, and the little letter holds on and follows.",
         scene=("Medium shot at night. On the left, a pale moonlit limestone palace facade in the style of Pasargadae: slender "
                "columns with plain column tops, a flat roofline, plain unadorned lintels, rows of tall dark openings; every opening "
                "is dark except one tall golden opening. A gold ribbon of wind pours from the right into that opening like breath. "
                "Yud rides the ribbon just right of the opening, about 12% of the image height, leaning forward into the flow; the "
                "tip of her tail curls around the ribbon, holding on. Where her tail grips, the gold is warmer and brighter, like a "
                "small knot of light. Nobody is visible inside the opening. In a thin strip at the very bottom, a dark moonlit "
                "garden with four narrow stone water channels meeting at a small square pool."),
         extra="No figures, guards or king; no symbols above doors or on columns."),
    dict(id="p06", expr="curious", area="upper-left 35%", surface="dawn sky",
         idea="At dawn a herald proclaims the king's call: whoever belongs to the people, let him go up!",
         scene=("Medium-wide view at sunrise. A long night-blue glazed-brick wall with horizontal bands of palmettes only. Yud "
                "perches on top of the wall at the upper right, about 10% of the image height, leaning toward the sound. Below, "
                "small in the frame on a low step, a Persian herald (short belted coat, trousers, soft rounded felt cap) holds open "
                "a blank leather scroll with only a gold border. From the herald, three identical gold sound-arcs of equal size and "
                "spacing rise along the frieze lines toward Yud. Two palm trees frame the herald, their fronds edged in gold. The "
                "dawn sky in bands of ivory and mustard above the blue wall: the first big gold of the book. A sunrise glint on the "
                "scroll's edge is the one white point of light."),
         extra="The scroll is blank; no king, soldiers or crowd; no animals on the wall; no musical notes."),
    dict(id="p07", expr="joy", area="upper-left 40%", surface="gold paper",
         idea="The little letter leaps with joy: the last word of the call is her own word.",
         scene=("Close-up on a field of warm gold. Yud mid-jump in the lower middle-right of the picture, about 22% of the image "
                "height, with a few short motion strokes beneath her. A halo of curling gold sound-arcs swirls around her like "
                "ribbons, their inner ends converging on one small clean round white dot just above her head; the arcs and the dot "
                "stay in the lower 55% of the picture. Along the bottom, a faint line of ivory hills and a path climbing to the left; "
                "at the top of the path stands one tiny pale square stone, the same ivory as the hills. The first all-gold page. "
                "A gold palmette-lotus band at top and bottom."),
         extra="No confetti, no pointed sparkles."),
    dict(id="p08", expr="giggle", area="top 35%", surface="pale sky",
         idea="Everyone packs for Jerusalem; the neighbors bring silver and gold, and the camel, like every camel, grumbles.",
         scene=("Wide frieze-like courtyard in morning sun: mud-brick walls, blue shadows in the corners, a few small warm lanterns "
                "along the wall. In the foreground a huge flat terracotta camel kneels facing left, pouting, lower lip out, heavy "
                "eyelids, a tasseled harness, a small puff of dust from its nostrils. Behind it, among rolled reed mats, clay jars "
                "and a folded black goat-hair tent, four people only: a grandmother pressing dates into a basket, a father knotting "
                "a cloth bundle (wrapped headcloths, long mantles, a veil), and two neighbors in Babylonian fringed robes holding out "
                "a silver bowl and a small gold jar. Yud sits on top of the tallest bundle at the center, tilted back, giggling, "
                "about 10% of the image height. The glint on the gold jar is the one white point of light. Colors turning from blue "
                "to terracotta."),
         extra="Only one camel and four people; no treasure piles."),
    dict(id="p09", expr="wide", area="upper 35%", surface="ivory wall",
         idea="The vessels of God's house go home: one gold bowl passes from a dark treasury into daylight, and the little letter peeks over its rim.",
         scene=("Close-up. Two hands pass one plain shallow gold bowl from a dark treasury doorway on the right into warm daylight "
                "on the left: the right hand in a pleated Persian court sleeve, the left hand in a plain undyed wool sleeve with a "
                "simple woven band. No faces. Yud peeks from inside the bowl, eyes just above the rim, about 12% of the image height, "
                "the tip of her tail curled over the rim. A glazed palmette border on the door jamb. The gleam on the rim is the one "
                "white point of light. Terracotta and sand tones."),
         extra="Exactly one vessel; no faces; no lamps or temple furniture; no symbols above the door."),
    dict(id="p10", expr="dizzy", area="upper 35%", surface="pale turquoise sky",
         idea="Six thousand seven hundred and twenty donkeys walk to Jerusalem, and the little letter loses count.",
         scene=("Wide comic view with a high horizon over an empty terracotta-and-sand road landscape. Three long rows of about "
                "twelve identical little grey donkeys in Egyptian-relief profile march to the left, one row behind another, each "
                "wearing one of four geometric saddle blankets (terracotta, rose, lapis, olive). One donkey in the back row wears a "
                "single round white bead, the point of light. In the lower-right foreground, Yud sits on a rock, tilted sideways, "
                "dizzy, about 11% of the image height."),
         extra="No numbers or tally marks; no horses."),
    dict(id="p11", expr="calm", area="upper 35%", surface="soft dusty-rose haze",
         idea="A little girl in the caravan asks, 'Me too? I'm still small,' and her mother's hand answers, 'You too.'",
         scene=("Medium shot from a small child's eye level; the adults are cropped at the knee. A forest of donkey legs and robe "
                "hems passes rhythmically to the left. In the middle stands a small girl (terracotta dress with a thin woven "
                "geometric hem band, small headcloth over a short braid), holding a tiny cloth bundle and looking up. Her mother's "
                "open hand in a sage-green sleeve with the same woven band enters from the right edge at the girl's head height, "
                "reaching down toward her. Yud sits on the girl's bundle, tilted up toward the hand, about 9% of the image height. A "
                "thin willow sprig with a few narrow olive-green leaves is tucked into the bundle's knot. A round bead on the bundle "
                "string is the one white point of light. Warm terracotta and dusty rose, afternoon light."),
         extra="No adult faces; no kissing, hugging or tears; no modern clothing."),
    dict(id="p12", expr=None, area="bottom 30%", surface="paper",
         idea="A background plate for a typographic page about one small letter.",
         scene=("A flat graphic background plate with no characters and no objects. The page is split vertically into two halves "
                "divided by a thin vertical gold palmette-lotus band. Right half: flat dusty-rose gouache paper, empty. Left half: "
                "warm gold gouache paper with soft dunes climbing toward the upper left in the background. Fine paper grain everywhere."),
         extra="No tiles, boxes or frames; no characters."),
    dict(id="p13", expr="curious", area="upper 35%", surface="banded sunset sky",
         idea="The caravan goes up toward Jerusalem, but the little letter looks back and wonders: if I am at the end, what is at the beginning?",
         scene=("Wide sunset; the sun has already set behind the left horizon. The whole caravan winds away to the left over the "
                "dunes as one long thin line of silhouettes, a pouting camel last in line. Alone on a dune crest at the lower right, "
                "Yud faces the opposite way, toward the right, about 10% of the image height, her body tilted to the right and her "
                "eyes placed toward her right side. Far on the right horizon stands a lone arch of two golden palm trees like a gate; "
                "exactly in the center of its opening, a very small pure-white round point of light with a faint soft halo and no "
                "rays, the only bright thing on the right side of the sky. Terracotta into rose sunset; the far-right haze glows "
                "soft gold."),
         extra="Nobody waving; the mood is curious, not lonely."),
    dict(id="p14", expr="determined", area="upper-left 40%", surface="dawn sky",
         idea="'I will go up,' said Yud, 'but backward, all the way to the beginning!'",
         scene=("Close-up at first light. Yud, upright and resolute, about 16% of the image height, rests at the center-right and "
                "turns toward the right edge, her eyes placed toward the right. Tiny caravan specks line the far-left horizon, with "
                "one tiny amber lamp at the very end of the line. Her long shadow stretches to the left across sand that shows faint "
                "wave-like parallel rows, like the lines of a scroll, reaching halfway to the caravan. Dawn gold rises behind "
                "blue-violet dunes. Above the right horizon the morning star is a single round soft white dot, the only point left "
                "in the sky."),
         extra="No moon; no arrows or signs."),
    dict(id="p15", expr="joy", area="upper-left 35%", surface="ivory sky",
         idea="Between the lines a golden thread shimmers; Yud grabs it with her tail and climbs.",
         scene=("Medium shot. The dunes turn into the rows of a great scroll: terraced bands of abstract ivory dashes with no "
                "letters, fading out toward the upper left. One fine gold thread winds up and to the right between the rows, with a "
                "few tiny gold lotus buds clustered at its bends. Yud climbs the thread, about 12% of the image height, mid-right, "
                "tilted up and to the right, the tip of her tail curled around the thread, with a short trail of tiny round gold "
                "dots behind her. A round gleam at the highest visible point of the thread is the one white point of light. Golden "
                "dawn, glowing ivory paper, lapis shadows. A gold palmette-lotus band along the bottom."),
         extra="No rope ladder; no letters; no people."),
    dict(id="p16", expr="curious", area="upper-left 40%", surface="sky",
         idea="Tap... tap... tap... who is building there?",
         scene=("Medium shot at golden dawn. The corner of a broken city wall of large pale Judean limestone blocks fills the right "
                "third of the frame; its top is broken, with grasses and a young olive shoot in the cracks. A fine gold thread runs "
                "into the wall through a small dark gap low in the stones, with warm light and one round white glint behind the gap "
                "(the point of light). Yud rests on the thread just left of the wall, about 12% of the image height, turned "
                "three-quarters toward the viewer and tilted toward the wall, the tip of her tail curled around the thread. From "
                "behind the wall rise three small gold tap-arcs and little puffs of stone dust: someone unseen is building. Soft "
                "flat hills far behind with one gold palm, no buildings."),
         extra="No people or builders; the wall is unfinished; no towers or temple."),
]


def build(p):
    parts = [p["idea"], STYLE, p["scene"]]
    if p["expr"]:
        parts.append(CHARACTER.format(expr=EXPR[p["expr"]]))
    parts += [TEXTSPACE.format(area=p["area"], surface=p["surface"]), AVOID, p["extra"]]
    return " ".join(parts)


if __name__ == "__main__":
    out = {p["id"]: {"expr": p["expr"], "prompt": build(p)} for p in PAGES}
    (HERE / "ch01_prompts_v2.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    for k, v in out.items():
        print(k, v["expr"], len(v["prompt"].split()), "words")
