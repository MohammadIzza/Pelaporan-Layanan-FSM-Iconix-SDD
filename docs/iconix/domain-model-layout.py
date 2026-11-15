"""Gambar domain-model.png dengan garis lurus (gaya Rosenberg & Stephens, 2007, Bab 2).

Isi kelas dan relasi SAMA dengan domain-model.puml (sumber teks untuk agen AI).
Posisi kotak (POS) dicari agar tidak ada garis yang menembus kotak dan persilangan sedikit,
lalu dikunci di sini. Setiap garis punya titik sambung sendiri di sisi kotak.
Jalankan: python domain-model-layout.py   (butuh Pillow dan font Arial Windows)
"""
import math, os
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont

S = 2; BH = 40
FONT = ImageFont.truetype("arial.ttf", 15 * S); FONTL = ImageFont.truetype("arial.ttf", 12 * S); FONTT = ImageFont.truetype("arialbd.ttf", 17 * S)
@lru_cache(None)
def bw(n): return max(124, FONT.getlength(n) / S + 34)

# (a, b, jenis, label): 'dia' = berlian di a, 'arr' = panah ke b, 'gen' = b adalah induk
EDGES = [
    ("Pengguna", "Peran", "dia", None), ("Pengguna", "AkunTelegram", "dia", None), ("Pengguna", "Skill", "dia", None),
    ("Pengguna", "UnitKerja", "arr", "bekerja di"),
    ("Pekerjaan", "Pengguna", "arr", "primary assignee"), ("Verifikasi", "Pengguna", "arr", "verifikator"),
    ("TimelineEvent", "Pengguna", "arr", "pelaku"), ("Tiket", "Pengguna", "arr", "pelapor"),
    ("Tiket", "UnitKerja", "arr", "unit asal"), ("JadwalRutin", "Pengguna", "arr", "dibuat oleh, ditugaskan ke"),
    ("Pekerjaan", "TimelineEvent", "dia", None), ("Pekerjaan", "Verifikasi", "dia", None), ("Pekerjaan", "HasilPekerjaan", "dia", None),
    ("Pekerjaan", "AreaKerja", "arr", "lokasi"),
    ("Tiket", "Pekerjaan", "gen", None), ("LaporanMandiri", "Pekerjaan", "gen", None), ("TugasRutin", "Pekerjaan", "gen", None),
    ("JadwalRutin", "TugasRutin", "arr", "menghasilkan"), ("JadwalRutin", "AreaKerja", "arr", None),
    ("JadwalRutin", "ItemChecklist", "dia", None), ("HasilChecklist", "ItemChecklist", "arr", None),
    ("Tiket", "JenisTiket", "arr", None), ("Tiket", "Klasifikasi", "dia", None), ("Tiket", "Rating", "dia", None),
    ("Tiket", "Lampiran", "dia", None), ("Tiket", "LokasiGPS", "dia", None),
    ("LaporanMandiri", "JenisTiket", "arr", "jenis pekerjaan"), ("LaporanMandiri", "Lampiran", "dia", "foto awal"),
    ("Klasifikasi", "JenisTiket", "arr", None), ("JenisTiket", "Skill", "arr", "membutuhkan"),
    ("HasilPekerjaan", "Lampiran", "dia", None), ("HasilPekerjaan", "LokasiGPS", "dia", None), ("HasilPekerjaan", "HasilChecklist", "dia", None),
]

POS = {
    "Skill": (125, 60),
    "AkunTelegram": (1225, 90),
    "Pengguna": (680, 110),
    "UnitKerja": (340, 135),
    "Peran": (935, 160),
    "TimelineEvent": (455, 265),
    "Verifikasi": (115, 325),
    "AreaKerja": (1180, 330),
    "Pekerjaan": (660, 340),
    "HasilPekerjaan": (870, 545),
    "Tiket": (405, 590),
    "LaporanMandiri": (650, 590),
    "TugasRutin": (1075, 590),
    "JadwalRutin": (1270, 675),
    "Rating": (95, 750),
    "JenisTiket": (390, 775),
    "HasilChecklist": (1060, 780),
    "LokasiGPS": (825, 840),
    "Lampiran": (605, 885),
    "Klasifikasi": (240, 905),
    "ItemChecklist": (1375, 1000),
}

def seg_rect(p, q, r):
    (x0, y0), (x1, y1) = p, q; xa, ya, xb, yb = r
    # Liang-Barsky
    dx, dy = x1 - x0, y1 - y0; t0, t1 = 0.0, 1.0
    for pp, qq in ((-dx, x0 - xa), (dx, xb - x0), (-dy, y0 - ya), (dy, yb - y0)):
        if pp == 0:
            if qq < 0: return False
        else:
            t = qq / pp
            if pp < 0: t0 = max(t0, t)
            else: t1 = min(t1, t)
    return t0 < t1

def cross(p, q, r, s):
    def o(a, b, c): return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2, d3, d4 = o(p, q, r), o(p, q, s), o(r, s, p), o(r, s, q)
    return (d1 * d2 < 0) and (d3 * d4 < 0)

FORCE = {("Pekerjaan", "HasilPekerjaan"): "R", ("HasilPekerjaan", "Pekerjaan"): "T"}
def side_of(n, pos, tx, ty, other=None):
    if (n, other) in FORCE: return FORCE[(n, other)]
    x, y = pos[n]; w, h = bw(n) / 2, BH / 2; dx, dy = tx - x, ty - y
    if abs(dx) * h > abs(dy) * w: return "R" if dx > 0 else "L"
    return "B" if dy > 0 else "T"

def anchors(pos):
    """kembalikan list (p0, p1) per edge dengan titik sambung tersebar."""
    ends = {}                                     # (node, side) -> list of (key_sort, edge_idx, which)
    gen_pt = {}
    for i, (a, b, k, _) in enumerate(EDGES):
        if k == "gen":
            t = (pos[b][0], pos[b][1] + BH / 2 + 16); gen_pt[i] = t
            sa = "T"; ends.setdefault((a, sa), []).append((t[0], i, 0)); continue
        sa = side_of(a, pos, *pos[b], other=b); sb = side_of(b, pos, *pos[a], other=a)
        ka = pos[b][0] if sa in "TB" else pos[b][1]; kb = pos[a][0] if sb in "TB" else pos[a][1]
        ends.setdefault((a, sa), []).append((ka, i, 0)); ends.setdefault((b, sb), []).append((kb, i, 1))
    pts = {}
    for (n, sd), lst in ends.items():
        lst.sort(); x, y = pos[n]; w, h = bw(n) / 2, BH / 2; m = len(lst)
        for j, (_, i, which) in enumerate(lst):
            f = (j + 1) / (m + 1)
            if sd in "TB":
                span = min(2 * w - 24, 26 * (m - 1) + 1) if m > 1 else 0
                px = x - span / 2 + (span * j / (m - 1) if m > 1 else 0); py = y - h if sd == "T" else y + h
            else:
                span = min(2 * h - 12, 12 * (m - 1) + 1) if m > 1 else 0
                py = y - span / 2 + (span * j / (m - 1) if m > 1 else 0); px = x - w if sd == "L" else x + w
            pts[(i, which)] = (px, py)
    out = []
    for i, (a, b, k, _) in enumerate(EDGES):
        out.append((pts[(i, 0)], gen_pt[i]) if k == "gen" else (pts[(i, 0)], pts[(i, 1)]))
    return out

def rect(n, pos, pad):
    x, y = pos[n]; w = bw(n); return (x - w / 2 - pad, y - BH / 2 - pad, x + w / 2 + pad, y + BH / 2 + pad)
def ovl(r1, r2): return not (r1[2] < r2[0] or r1[0] > r2[2] or r1[3] < r2[1] or r1[1] > r2[3])

def render(pos, out):
    INK, LINE, LAB = (33, 33, 33), (90, 90, 90), (40, 40, 40)
    minx = min(x - bw(n) / 2 for n, (x, y) in pos.items()) - 40; miny = min(y for x, y in pos.values()) - 110
    OX, OY = -minx, -miny + 70
    W = int(max(x + bw(n) / 2 for n, (x, y) in pos.items()) + OX + 60); H = int(max(y for x, y in pos.values()) + OY + 70)
    img = Image.new("RGB", (W * S, H * S), "white"); d = ImageDraw.Draw(img)
    def sp(p): return ((p[0] + OX) * S, (p[1] + OY) * S)
    def ln(a, b): d.line([sp(a), sp(b)], fill=LINE, width=2 * S)
    sg = anchors(pos)
    for (a, b, k, lab), (p, q) in zip(EDGES, sg): ln(p, q)
    pk = pos["Pekerjaan"]; tip = (pk[0], pk[1] + BH / 2); base = (pk[0], pk[1] + BH / 2 + 16); ln(base, tip)
    px_, py_ = pos["Pengguna"]; w = bw("Pengguna") / 2
    loop = [(px_ + 10, py_ - BH / 2), (px_ + 10, py_ - BH / 2 - 28), (px_ + 54, py_ - BH / 2 - 28), (px_ + 54, py_ - BH / 2)]
    for a_, b_ in zip(loop, loop[1:]): ln(a_, b_)
    for n, (x, y) in pos.items():
        ww = bw(n); d.rectangle([sp((x - ww / 2, y - BH / 2)), sp((x + ww / 2, y + BH / 2))], fill="white", outline=INK, width=2 * S)
        d.text(sp((x, y)), n, font=FONT, fill=INK, anchor="mm")
    def head(tip, frm, kind):
        ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0]); ux, uy = math.cos(ang), math.sin(ang); px, py = -uy, ux
        if kind == "arr":
            ln((tip[0] - 12 * ux + 5 * px, tip[1] - 12 * uy + 5 * py), tip); ln((tip[0] - 12 * ux - 5 * px, tip[1] - 12 * uy - 5 * py), tip)
        elif kind == "dia":
            m = (tip[0] - 9 * ux, tip[1] - 9 * uy); e = (tip[0] - 18 * ux, tip[1] - 18 * uy)
            d.polygon([sp(tip), sp((m[0] + 6 * px, m[1] + 6 * py)), sp(e), sp((m[0] - 6 * px, m[1] - 6 * py))], fill="white", outline=LINE, width=2 * S)
        elif kind == "tri":
            b1 = (tip[0] - 15 * ux + 9 * px, tip[1] - 15 * uy + 9 * py); b2 = (tip[0] - 15 * ux - 9 * px, tip[1] - 15 * uy - 9 * py)
            d.polygon([sp(tip), sp(b1), sp(b2)], fill="white", outline=LINE, width=2 * S)
    for (a, b, k, lab), (p, q) in zip(EDGES, sg):
        if k == "dia": head(p, q, "dia")
        if k == "arr": head(q, p, "arr")
    head(tip, base, "tri"); head(loop[-1], loop[-2], "arr")
    boxes = [rect(n, pos, 3) for n in pos]; placed = []
    def ok(r, own):
        if any(ovl(r, b) for b in boxes + placed): return False
        return not any(seg_rect(p, q, r) for j, (p, q) in enumerate(sg) if j != own)
    for i, ((a, b, k, lab), (p, q)) in enumerate(zip(EDGES, sg)):
        if not lab: continue
        tw = FONTL.getlength(lab) / S; best = None
        for t in (0.5, 0.42, 0.58, 0.34, 0.66, 0.26, 0.74, 0.2, 0.8):
            cx, cy = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
            r = (cx - tw / 2 - 3, cy - 8, cx + tw / 2 + 3, cy + 8)
            if ok(r, i): best = (cx, cy, r); break
            if best is None: best = (cx, cy, r)
        cx, cy, r = best; placed.append(r)
        d.rectangle([sp((r[0], r[1])), sp((r[2], r[3]))], fill="white"); d.text(sp((cx, cy)), lab, font=FONTL, fill=LAB, anchor="mm")
    d.text(sp((loop[2][0] + 8, loop[2][1] + 2)), "atasan dari", font=FONTL, fill=LAB, anchor="lm")
    d.text(((W / 2) * S, 30 * S), "Domain Model — Aplikasi Pelaporan Layanan Operasional FSM UNDIP", font=FONTT, fill=INK, anchor="mm")
    d.text(((W / 2) * S, 55 * S), "Berlian kosong = agregasi (has-a)  ·  Segitiga kosong = generalisasi (is-a)  ·  Panah = asosiasi",
           font=FONTL, fill=(110, 110, 110), anchor="mm")
    img.save(out)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "domain-model.png")
    render({k: tuple(v) for k, v in POS.items()}, out)
    print(out)
