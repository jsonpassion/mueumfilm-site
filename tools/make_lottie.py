#!/usr/bin/env python3
"""무음필름 사이트 로티 생성기 — 담백, paper/ink/sky.
재생성: python3 tools/make_lottie.py  →  lottie/*.json
세트: rewind(히어로), silent, film-tone, level, stamp, lens
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "lottie")

SKY = [0.290, 0.616, 0.878]      # #4A9DE0
PALE = [0.663, 0.788, 0.925]     # #A9C9EC
HORIZON = [0.949, 0.914, 0.863]  # #F2E9DC
INK = [0.133, 0.192, 0.290]      # #22314A
PAPER = [0.984, 0.992, 1.0]      # #FBFDFF
SUN = [1.0, 0.839, 0.420]        # #FFD66B
CORAL = [0.957, 0.518, 0.373]    # #F4845F
GRAY = [0.72, 0.75, 0.79]

EASE = {"i": {"x": [0.35], "y": [1]}, "o": {"x": [0.65], "y": [0]}}

def kf(pairs):
    return {"a": 1, "k": [dict(t=t, s=(v if isinstance(v, list) else [v]), **EASE) for t, v in pairs]}

def st(v): return {"a": 0, "k": v}

def tr(p=(0, 0), s=(100, 100), r=0, o=100):
    return {"ty": "tr", "p": st(list(p)), "a": st([0, 0]), "s": st(list(s)),
            "r": st(r), "o": st(o), "sk": st(0), "sa": st(0)}

def group(shapes, transform=None):
    return {"ty": "gr", "it": shapes + [transform or tr()]}

def ellipse(w, h, p=(0, 0)): return {"ty": "el", "p": st(list(p)), "s": st([w, h])}
def rect(w, h, r=0, p=(0, 0)): return {"ty": "rc", "p": st(list(p)), "s": st([w, h]), "r": st(r)}
def fill(c, o=100): return {"ty": "fl", "c": st(c + [1]), "o": st(o), "bm": 0}
def stroke(c, w, o=100): return {"ty": "st", "c": st(c + [1]), "o": st(o), "w": st(w), "lc": 2, "lj": 2, "bm": 0}

def vgrad(c_top, c_mid, c_bot, h):
    stops = [0] + c_top + [0.55] + c_mid + [1] + c_bot
    return {"ty": "gf", "o": st(100), "r": 1, "bm": 0,
            "g": {"p": 3, "k": st(stops)}, "s": st([0, -h / 2]), "e": st([0, h / 2]), "t": 1}

def layer(ind, name, cx, cy, shapes, op, ks_extra=None):
    ks = {"o": st(100), "r": st(0), "p": st([cx, cy, 0]), "a": st([0, 0, 0]), "s": st([100, 100, 100])}
    if ks_extra: ks.update(ks_extra)
    return {"ddd": 0, "ind": ind, "ty": 4, "nm": name, "sr": 1, "ks": ks,
            "ao": 0, "shapes": shapes, "ip": 0, "op": op, "st": 0, "bm": 0}

def anim(name, w, h, op, layers):
    return {"v": "5.7.4", "fr": 30, "ip": 0, "op": op, "w": w, "h": h,
            "nm": name, "ddd": 0, "assets": [], "layers": layers}

def save(name, data):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print("✓", name)

# ── 1. rewind (히어로) — 필름 프레임 위로 캡처링이 '지금'에서 '지나간 순간'으로 되감긴다
def rewind():
    OP = 180
    W, H = 320, 150
    xs = [48, 104, 160, 216, 272]  # 5프레임 (오른쪽=지금)
    caught = xs[1]                  # 되감아 잡는 과거 프레임
    layers = []
    ind = 10
    for i, x in enumerate(xs):
        top = SKY if i % 2 == 0 else PALE
        layers.append(layer(ind, f"f{i}", x, 75,
            [group([rect(48, 78, 8), vgrad(top, PALE, HORIZON, 78)])], OP,
            {"o": st(55 if i != 1 else 100)}))
        ind += 1
    # 캡처 링: 지금(272) → 과거(104) 되감기 → 펄스 → 페이드아웃(루프 재시작)
    ring = layer(1, "ring", 272, 75,
        [group([rect(56, 88, 11), stroke(SKY, 4)])], OP,
        {"p": kf([(0, [272, 75, 0]), (45, [272, 75, 0]), (95, [caught, 75, 0]),
                  (150, [caught, 75, 0]), (180, [272, 75, 0])]),
         "s": kf([(95, [100, 100, 100]), (112, [112, 112, 100]), (128, [100, 100, 100]),
                  (180, [100, 100, 100])]),
         "o": kf([(0, 0), (18, 100), (160, 100), (179, 0)])})
    save("rewind.json", anim("rewind", W, H, OP, [ring] + layers))

# ── 2. silent — 셔터 누름 + 무음(∅) 배지 펄스, 소리 없음
def silent():
    OP = 120
    ring = layer(4, "ring", 100, 108, [group([ellipse(112, 112), stroke(INK, 6)])], OP)
    inner = layer(3, "inner", 100, 108, [group([ellipse(90, 90), fill(SKY)])], OP,
        {"s": kf([(0, [100, 100, 100]), (36, [100, 100, 100]), (46, [78, 78, 100]),
                  (58, [100, 100, 100]), (120, [100, 100, 100])])})
    # 무음 배지 ∅ (원 + 슬래시) 우상단, 셔터 누를 때 팝
    badge_o = kf([(0, 0), (40, 0), (50, 100), (95, 100), (110, 0)])
    circle = layer(2, "mute-o", 150, 58, [group([ellipse(38, 38), stroke(INK, 5)])], OP, {"o": badge_o})
    slash = layer(1, "mute-slash", 150, 58,
        [group([rect(46, 5, 2), fill(INK)], tr(r=45))], OP, {"o": badge_o})
    save("silent.json", anim("silent", 200, 180, OP, [slash, circle, inner, ring]))

# ── 3. film-tone — 프레임 안의 톤이 흐르듯 크로스페이드 (필름 톤은 덤)
def film_tone():
    OP = 210
    w, h = 220, 150
    frame = layer(3, "frame", 140, 100, [group([rect(w + 10, h + 10, 14), stroke(INK, 4)])], OP)
    cool = layer(2, "cool", 140, 100, [group([rect(w, h, 10), vgrad(SKY, PALE, HORIZON, h)])], OP,
        {"o": kf([(0, 100), (70, 100), (100, 0), (170, 0), (200, 100), (210, 100)])})
    warm = layer(1, "warm", 140, 100,
        [group([rect(w, h, 10), vgrad([0.988, 0.851, 0.627], CORAL, [0.616, 0.412, 0.502], h)])], OP,
        {"o": kf([(0, 0), (70, 0), (100, 100), (170, 100), (200, 0), (210, 0)])})
    save("film-tone.json", anim("film-tone", 280, 200, OP, [warm, cool, frame]))

# ── 4. level — 수평선: 기울다 수평 스냅 + sky 점등
def level():
    OP = 150
    side = layer(3, "side", 160, 60, [
        group([rect(24, 2), fill(GRAY, 70)], tr(p=(-120, 0))),
        group([rect(24, 2), fill(GRAY, 70)], tr(p=(120, 0)))], OP)
    tilt = layer(2, "tilt", 160, 60, [group([rect(150, 3, 1.5), fill(GRAY)])], OP,
        {"r": kf([(0, -9), (45, 1.5), (60, 0), (150, 0)]),
         "o": kf([(0, 100), (58, 100), (62, 0), (150, 0)])})
    lvl = layer(1, "level", 160, 60, [group([rect(150, 3, 1.5), fill(SKY)])], OP,
        {"o": kf([(0, 0), (58, 0), (62, 100), (140, 100), (150, 0)])})
    save("level.json", anim("level", 320, 120, OP, [lvl, tilt, side]))

# ── 5. stamp — 날짜·날씨 스탬프가 우하단에 사뿐히 각인
def stamp():
    OP = 150
    w, h = 220, 150
    photo = layer(3, "photo", 140, 100, [group([rect(w, h, 12), vgrad(PALE, HORIZON, [0.93, 0.90, 0.86], h)])], OP)
    frame = layer(2, "frame", 140, 100, [group([rect(w + 10, h + 10, 14), stroke(INK, 4)])], OP)
    chip = layer(1, "stamp", 140 + w / 2 - 52, 100 + h / 2 - 22, [
        group([rect(76, 20, 5), fill(INK, 78)]),
        group([rect(60, 4, 2), fill(PAPER)], tr(p=(0, -2))),
        group([rect(34, 3, 1.5), fill(PAPER, 70)], tr(p=(-8, 5)))], OP,
        {"o": kf([(0, 0), (35, 0), (55, 100), (140, 100), (150, 0)]),
         "p": kf([(35, [140 + w / 2 - 52, 100 + h / 2 - 12, 0]),
                  (55, [140 + w / 2 - 52, 100 + h / 2 - 22, 0]),
                  (150, [140 + w / 2 - 52, 100 + h / 2 - 22, 0])])})
    save("stamp.json", anim("stamp", 280, 200, OP, [chip, frame, photo]))

# ── 6. lens — 브랜드 렌즈: 하늘이 낮→노을→밤으로 순환
def lens():
    OP = 270
    d = 150
    def sky(ind, grad, fades):
        return layer(ind, f"sky{ind}", 120, 120, [group([ellipse(d, d), grad])], OP, {"o": kf(fades)})
    day = vgrad(SKY, PALE, HORIZON, d)
    dusk = vgrad([0.988, 0.851, 0.627], CORAL, [0.541, 0.353, 0.478], d)
    night = vgrad([0.169, 0.227, 0.333], [0.290, 0.353, 0.471], [0.561, 0.639, 0.769], d)
    ring = layer(1, "ring", 120, 120, [group([ellipse(d + 14, d + 14), stroke(INK, 5)])], OP)
    save("lens.json", anim("lens", 240, 240, OP, [ring,
        sky(2, day, [(0, 100), (75, 100), (95, 0), (250, 0), (269, 100)]),
        sky(3, dusk, [(0, 0), (75, 0), (95, 100), (160, 100), (180, 0)]),
        sky(4, night, [(0, 0), (160, 0), (180, 100), (250, 100), (269, 0)])]))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    # 무음필름 잔여 정리: 구 맑음 로티 제거
    for old in ["ti-meter.json", "level-snap.json", "shutter.json", "crossfade.json",
                "stamp-in.json", "widget-sun.json", "lens-cycle.json"]:
        p = os.path.join(OUT, old)
        if os.path.exists(p): os.remove(p)
    rewind(); silent(); film_tone(); level(); stamp(); lens()
    print("done")
