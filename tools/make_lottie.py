#!/usr/bin/env python3
"""맑음 사이트 로티 7종 생성기 — 디자인시스템 「관측」 (paper/ink/sky, 담백)
재생성: python3 tools/make_lottie.py  →  lottie/*.json
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "..", "lottie")

# 브랜드 (0~1 RGB)
SKY = [0.290, 0.616, 0.878]      # #4A9DE0
PALE = [0.663, 0.788, 0.925]     # #A9C9EC
HORIZON = [0.949, 0.914, 0.863]  # #F2E9DC
INK = [0.133, 0.192, 0.290]      # #22314A
PAPER = [0.984, 0.992, 1.0]      # #FBFDFF
SUN = [1.0, 0.839, 0.420]        # #FFD66B
CORAL = [0.957, 0.518, 0.373]    # #F4845F
NIGHT_A = [0.169, 0.227, 0.333]  # #2B3A55
NIGHT_B = [0.561, 0.639, 0.769]  # #8FA3C4
GRAY = [0.72, 0.75, 0.79]

EASE = {"i": {"x": [0.35], "y": [1]}, "o": {"x": [0.65], "y": [0]}}

def kf(pairs):
    """[(t, value), ...] → 애니메이션 속성 (value: list)"""
    keys = []
    for t, v in pairs:
        k = {"t": t, "s": v if isinstance(v, list) else [v]}
        k.update(EASE)
        keys.append(k)
    return {"a": 1, "k": keys}

def st(v):
    return {"a": 0, "k": v}

def tr(p=(0, 0), s=(100, 100), r=0, o=100):
    return {"ty": "tr", "p": st(list(p)), "a": st([0, 0]), "s": st(list(s)),
            "r": st(r), "o": st(o), "sk": st(0), "sa": st(0)}

def group(shapes, transform=None):
    return {"ty": "gr", "it": shapes + [transform or tr()]}

def ellipse(w, h, p=(0, 0)):
    return {"ty": "el", "p": st(list(p)), "s": st([w, h])}

def rect(w, h, r=0, p=(0, 0)):
    return {"ty": "rc", "p": st(list(p)), "s": st([w, h]), "r": st(r)}

def fill(c, o=100):
    color = c if isinstance(c, dict) else st(c + [1])
    op = o if isinstance(o, dict) else st(o)
    return {"ty": "fl", "c": color, "o": op, "bm": 0}

def stroke(c, w, o=100):
    return {"ty": "st", "c": st(c + [1]), "o": st(o), "w": st(w), "lc": 2, "lj": 2, "bm": 0}

def vgrad(c_top, c_mid, c_bot, h):
    """세로 3스톱 그라데이션 (하늘)"""
    stops = [0] + c_top + [0.55] + c_mid + [1] + c_bot
    return {"ty": "gf", "o": st(100), "r": 1, "bm": 0,
            "g": {"p": 3, "k": st(stops)},
            "s": st([0, -h / 2]), "e": st([0, h / 2]), "t": 1}

def layer(ind, name, cx, cy, shapes, op, ks_extra=None):
    ks = {"o": st(100), "r": st(0), "p": st([cx, cy, 0]), "a": st([0, 0, 0]), "s": st([100, 100, 100])}
    if ks_extra:
        ks.update(ks_extra)
    return {"ddd": 0, "ind": ind, "ty": 4, "nm": name, "sr": 1, "ks": ks,
            "ao": 0, "shapes": shapes, "ip": 0, "op": op, "st": 0, "bm": 0}

def anim(name, w, h, op, layers):
    return {"v": "5.7.4", "fr": 30, "ip": 0, "op": op, "w": w, "h": h,
            "nm": name, "ddd": 0, "assets": [], "layers": layers}

def save(name, data):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print("✓", name)

# ── 1. lens-cycle — 관측창: 하늘이 낮→노을→밤으로 순환
def lens_cycle():
    OP = 270
    d = 150
    def sky_layer(ind, grad, fades):
        return layer(ind, f"sky{ind}", 120, 120,
                     [group([ellipse(d, d), grad])], OP,
                     {"o": kf(fades)})
    day = vgrad(SKY, PALE, HORIZON, d)
    dusk = vgrad([0.988, 0.851, 0.627], CORAL, [0.541, 0.353, 0.478], d)
    night = vgrad(NIGHT_A, [0.290, 0.353, 0.471], NIGHT_B, d)
    ring = layer(1, "ring", 120, 120, [group([ellipse(d + 14, d + 14), stroke(INK, 5)])], OP)
    l_day = sky_layer(2, day, [(0, 100), (75, 100), (95, 0), (250, 0), (269, 100)])
    l_dusk = sky_layer(3, dusk, [(0, 0), (75, 0), (95, 100), (160, 100), (180, 0)])
    l_night = sky_layer(4, night, [(0, 0), (160, 0), (180, 100), (250, 100), (269, 0)])
    save("lens-cycle.json", anim("lens-cycle", 240, 240, OP, [ring, l_day, l_dusk, l_night]))

# ── 2. ti-meter — 수은주: 게이지가 차오르다 '안 들키는 선' 안에서 멈춤
def ti_meter():
    OP = 150
    track_w = 260
    track = layer(4, "track", 160, 40, [group([rect(track_w, 6, 3), fill(GRAY, 45)])], OP)
    ticks = layer(3, "ticks", 160, 40, [
        group([rect(2, 14), fill(INK, 60)], tr(p=(-track_w / 2 + track_w * 0.25, 0))),
        group([rect(2, 14), fill(INK, 60)], tr(p=(-track_w / 2 + track_w * 0.60, 0))),
    ], OP)
    # 채움: 왼쪽 고정, scale-x 0→58→46 (자연스러움 구간에서 안착)
    gauge = layer(2, "fill", 160 - track_w / 2, 40, [
        group([rect(track_w, 6, 3, p=(track_w / 2, 0)), fill(SKY)],
              tr(s=(100, 100)))
    ], OP, {"s": kf([(0, [0, 100, 100]), (55, [58, 100, 100]), (80, [46, 100, 100]), (150, [46, 100, 100])])})
    save("ti-meter.json", anim("ti-meter", 320, 80, OP, [gauge, ticks, track]))

# ── 3. level-snap — 관측 수평선: 기울다 수평 스냅 + sky 점등
def level_snap():
    OP = 150
    side = layer(3, "side-ticks", 160, 60, [
        group([rect(24, 2), fill(GRAY, 70)], tr(p=(-120, 0))),
        group([rect(24, 2), fill(GRAY, 70)], tr(p=(120, 0))),
    ], OP)
    line_gray = layer(2, "line-tilt", 160, 60,
                      [group([rect(150, 3, 1.5), fill(GRAY)])], OP,
                      {"r": kf([(0, -9), (45, 1.5), (60, 0), (150, 0)]),
                       "o": kf([(0, 100), (58, 100), (62, 0), (150, 0)])})
    line_sky = layer(1, "line-level", 160, 60,
                     [group([rect(150, 3, 1.5), fill(SKY)])], OP,
                     {"o": kf([(0, 0), (58, 0), (62, 100), (140, 100), (150, 0)])})
    save("level-snap.json", anim("level-snap", 320, 120, OP, [line_sky, line_gray, side]))

# ── 4. shutter — 셔터: 눌림 + 플래시
def shutter():
    OP = 120
    ring = layer(3, "ring", 100, 100, [group([ellipse(120, 120), stroke(INK, 6)])], OP)
    inner = layer(2, "inner", 100, 100, [group([ellipse(96, 96), fill(SKY)])], OP,
                  {"s": kf([(0, [100, 100, 100]), (40, [100, 100, 100]), (48, [80, 80, 100]),
                            (58, [100, 100, 100]), (120, [100, 100, 100])])})
    flash = layer(1, "flash", 100, 100, [group([rect(200, 200), fill(PAPER)])], OP,
                  {"o": kf([(0, 0), (48, 0), (52, 85), (66, 0), (120, 0)])})
    save("shutter.json", anim("shutter", 200, 200, OP, [flash, inner, ring]))

# ── 5. crossfade — 톤 크로스페이드: 사진 프레임의 빛이 흐르듯 전환
def crossfade():
    OP = 210
    w, h = 220, 150
    frame = layer(3, "frame", 140, 100, [group([rect(w + 10, h + 10, 14), stroke(INK, 4)])], OP)
    cool = layer(2, "cool", 140, 100,
                 [group([rect(w, h, 10), vgrad(SKY, PALE, HORIZON, h)])], OP,
                 {"o": kf([(0, 100), (70, 100), (100, 0), (170, 0), (200, 100), (210, 100)])})
    warm = layer(1, "warm", 140, 100,
                 [group([rect(w, h, 10), vgrad([0.988, 0.851, 0.627], CORAL, [0.616, 0.412, 0.502], h)])], OP,
                 {"o": kf([(0, 0), (70, 0), (100, 100), (170, 100), (200, 0), (210, 0)])})
    save("crossfade.json", anim("crossfade", 280, 200, OP, [warm, cool, frame]))

# ── 6. stamp-in — 관측 기록 스탬프: 우하단에 사뿐히 각인
def stamp_in():
    OP = 150
    w, h = 220, 150
    photo = layer(3, "photo", 140, 100, [group([rect(w, h, 12), vgrad(PALE, HORIZON, [0.93, 0.90, 0.86], h)])], OP)
    frame = layer(2, "frame", 140, 100, [group([rect(w + 10, h + 10, 14), stroke(INK, 4)])], OP)
    chip = layer(1, "stamp", 140 + w / 2 - 52, 100 + h / 2 - 22, [
        group([rect(76, 20, 5), fill(INK, 78)]),
        group([rect(60, 4, 2), fill(PAPER)], tr(p=(0, -2))),
        group([rect(34, 3, 1.5), fill(PAPER, 70)], tr(p=(-8, 5))),
    ], OP, {"o": kf([(0, 0), (35, 0), (55, 100), (140, 100), (150, 0)]),
            "p": kf([(35, [140 + w / 2 - 52, 100 + h / 2 - 12, 0]), (55, [140 + w / 2 - 52, 100 + h / 2 - 22, 0]),
                     (150, [140 + w / 2 - 52, 100 + h / 2 - 22, 0])])})
    save("stamp-in.json", anim("stamp-in", 280, 200, OP, [chip, frame, photo]))

# ── 7. widget-sun — 위젯: 지평선 위로 해가 떠오름
def widget_sun():
    OP = 210
    card = layer(4, "card", 120, 80, [group([rect(190, 120, 18), fill(PAPER), ]), group([rect(190, 120, 18), stroke(INK, 4)])], OP)
    horizon = layer(3, "horizon", 120, 92, [group([rect(140, 2.5, 1)]), group([rect(140, 2.5, 1), fill(INK, 35)])], OP)
    # 해: 지평선 아래에서 떠오른다 (마스크 대신 카드 안 위치 이동 + 페이드)
    sun = layer(2, "sun", 120, 92, [group([ellipse(34, 34), fill(SUN)]),
                                    group([ellipse(34, 34), stroke(INK, 3)])], OP,
                {"p": kf([(0, [120, 110, 0]), (70, [120, 66, 0]), (170, [120, 62, 0]), (210, [120, 110, 0])]),
                 "o": kf([(0, 0), (12, 100), (185, 100), (205, 0), (210, 0)])})
    save("widget-sun.json", anim("widget-sun", 240, 160, OP, [sun, horizon, card]))

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    lens_cycle(); ti_meter(); level_snap(); shutter(); crossfade(); stamp_in(); widget_sun()
    print("done")
