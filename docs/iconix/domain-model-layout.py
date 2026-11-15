"""Gambar domain-model.png dengan tata letak tetap (garis siku, tanpa tumpang tindih).

Isi kelas dan relasi SAMA dengan domain-model.puml (sumber teks untuk agen AI).
File ini hanya mengatur posisi agar diagram rapi dibaca manusia.
Jalankan: python domain-model-layout.py  (butuh Pillow; font Arial Windows)
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

S = 2                      # skala render (ketajaman)
OY = 70                    # ruang judul
W, H = 1380, 900
INK, LINE, LABEL = (33, 33, 33), (90, 90, 90), (40, 40, 40)
FONT = ImageFont.truetype("arial.ttf", 15 * S)
FONTL = ImageFont.truetype("arial.ttf", 12 * S)
FONTT = ImageFont.truetype("arialbd.ttf", 17 * S)

R1, R2, R3, R4 = 110, 310, 510, 730
POS = {
    "Skill": (160, R1), "UnitKerja": (390, R1), "Pengguna": (640, R1), "Peran": (900, R1), "AkunTelegram": (1140, R1),
    "Verifikasi": (160, R2), "TimelineEvent": (390, R2), "Pekerjaan": (640, R2), "HasilPekerjaan": (900, R2), "AreaKerja": (1160, R2),
    "Tiket": (250, R3), "LaporanMandiri": (500, R3), "TugasRutin": (750, R3), "JadwalRutin": (1160, R3),
    "Rating": (90, R4), "Klasifikasi": (250, R4), "JenisTiket": (420, R4), "Lampiran": (610, R4),
    "LokasiGPS": (800, R4), "HasilChecklist": (1000, R4), "ItemChecklist": (1220, R4),
}
BH = 40
def bw(n): return max(124, FONT.getlength(n) / S + 34)
def L(n, dy=0): x, y = POS[n]; return (x - bw(n) / 2, y + dy)
def R(n, dy=0): x, y = POS[n]; return (x + bw(n) / 2, y + dy)
def T(n, dx=0): x, y = POS[n]; return (x + dx, y - BH / 2)
def B(n, dx=0): x, y = POS[n]; return (x + dx, y + BH / 2)

P = "Pengguna"
# (titik jalur, ujung_awal, ujung_akhir, label, posisi_label)
# ujung: "dia" = berlian agregasi (sisi keseluruhan), "arr" = panah asosiasi, "tri" = segitiga generalisasi, None
E = [
    ([R(P), L("Peran")], "dia", None, None, None),
    ([T(P, 40), (680, 45), (1140, 45), T("AkunTelegram")], "dia", None, None, None),
    ([T(P, -40), (600, 45), (160, 45), T("Skill")], "dia", None, None, None),
    ([L(P), R("UnitKerja")], None, "arr", "bekerja di", (515, 98)),
    ([T(P, -12), (628, 76), (652, 76), T(P, 12)], None, "arr", "atasan dari", (640, 62)),
    ([T("Pekerjaan"), B(P)], None, "arr", "primary assignee", (696, 222)),
    ([T("Verifikasi"), (160, 205), (605, 205), B(P, -35)], None, "arr", "verifikator", (300, 197)),
    ([T("TimelineEvent"), (390, 240), (620, 240), B(P, -20)], None, "arr", "pelaku", (500, 232)),
    ([L("Tiket", -10), (60, 500), (60, 172), (590, 172), B(P, -50)], None, "arr", "pelapor", (480, 164)),
    ([L("Tiket", 10), (40, 520), (40, 150), (390, 150), B("UnitKerja")], None, "arr", "unit asal", (200, 142)),
    ([R("JadwalRutin"), (1310, 510), (1310, 185), (680, 185), B(P, 40)], None, "arr", "dibuat oleh, ditugaskan ke", (1000, 177)),
    ([L("Pekerjaan"), R("TimelineEvent")], "dia", None, None, None),
    ([B("Pekerjaan", -30), (610, 368), (160, 368), B("Verifikasi")], "dia", None, None, None),
    ([R("Pekerjaan"), L("HasilPekerjaan")], "dia", None, None, None),
    ([T("Pekerjaan", 30), (670, 265), (1160, 265), T("AreaKerja")], None, "arr", "lokasi", (1000, 257)),
    ([R("JadwalRutin", 0), R("JadwalRutin", 0)], None, None, None, None),   # placeholder (diabaikan)
    ([L("JadwalRutin"), R("TugasRutin")], None, "arr", "menghasilkan", (1000, 498)),
    ([T("JadwalRutin"), B("AreaKerja")], None, "arr", None, None),
    ([B("JadwalRutin"), (1160, 662), (1220, 662), T("ItemChecklist")], "dia", None, None, None),
    ([R("HasilChecklist"), L("ItemChecklist")], None, "arr", None, None),
    ([B("Tiket", 5), (255, 600), (390, 600), T("JenisTiket", -30)], None, "arr", None, None),
    ([B("Tiket", -20), T("Klasifikasi", -20)], "dia", None, None, None),
    ([B("Tiket", -45), (205, 590), (90, 590), T("Rating")], "dia", None, None, None),
    ([B("Tiket", 30), (280, 572), (596, 572), T("Lampiran", -14)], "dia", None, None, None),
    ([B("Tiket", 55), (305, 555), (785, 555), T("LokasiGPS", -15)], "dia", None, None, None),
    ([B("LaporanMandiri", -40), T("JenisTiket", 40)], None, "arr", "jenis pekerjaan", (400, 545)),
    ([B("LaporanMandiri", 30), (530, 688), (624, 688), T("Lampiran", 14)], "dia", None, "foto awal", (578, 545)),
    ([R("Klasifikasi"), L("JenisTiket")], None, "arr", None, None),
    ([B("JenisTiket"), (420, 810), (20, 810), (20, 110), L("Skill")], None, "arr", "membutuhkan", (220, 800)),
]
E = [e for e in E if e[0][0] != e[0][1]]
# agregasi HasilPekerjaan (satu batang ke tiga bagian)
HPBUS = 632
E += [([B("HasilPekerjaan"), (900, HPBUS), (610, HPBUS), T("Lampiran")], "dia", None, None, None),
      ([(815, HPBUS), T("LokasiGPS", 15)], None, None, None, None),
      ([(900, HPBUS), (1000, HPBUS), T("HasilChecklist")], None, None, None, None)]
# generalisasi: satu segitiga di Pekerjaan, batang ke tiga turunan
GEN = (B("Pekerjaan"), 425, ["Tiket", "LaporanMandiri", "TugasRutin"])

img = Image.new("RGB", (W * S, (H + OY) * S), "white")
d = ImageDraw.Draw(img)
def sp(p): return (p[0] * S, (p[1] + OY) * S)

# kumpulkan segmen vertikal (untuk lompatan pada garis horizontal)
vert = []
for pts, *_ in E:
    for a, b in zip(pts, pts[1:]):
        if abs(a[0] - b[0]) < 0.5: vert.append((a[0], min(a[1], b[1]), max(a[1], b[1]), id(pts)))
gx, gy = GEN[0]
vert.append((gx, gy, GEN[1], -1))
for c in GEN[2]: vert.append((POS[c][0], GEN[1], T(c)[1], -1))

def hline(a, b, owner):
    y = a[1]; x0, x1 = sorted((a[0], b[0]))
    hops = sorted(v[0] for v in vert if v[3] != owner and x0 + 6 < v[0] < x1 - 6 and v[1] + 2 < y < v[2] - 2)
    xs = x0
    for hx in hops:
        d.line([sp((xs, y)), sp((hx - 6, y))], fill=LINE, width=2 * S // 1)
        d.arc([sp((hx - 6, y - 6)), sp((hx + 6, y + 6))], 180, 360, fill=LINE, width=2 * S // 1)
        xs = hx + 6
    d.line([sp((xs, y)), sp((x1, y))], fill=LINE, width=2 * S // 1)

def poly(pts, owner):
    for a, b in zip(pts, pts[1:]):
        if abs(a[1] - b[1]) < 0.5 and abs(a[0] - b[0]) > 0.5: hline(a, b, owner)
        else: d.line([sp(a), sp(b)], fill=LINE, width=2 * S // 1)

def head(tip, frm, kind):
    ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
    ux, uy = math.cos(ang), math.sin(ang); px, py = -uy, ux
    if kind == "arr":
        p1 = (tip[0] - 11 * ux + 5 * px, tip[1] - 11 * uy + 5 * py); p2 = (tip[0] - 11 * ux - 5 * px, tip[1] - 11 * uy - 5 * py)
        d.line([sp(p1), sp(tip), sp(p2)], fill=LINE, width=2 * S)
    elif kind == "dia":
        m = (tip[0] - 9 * ux, tip[1] - 9 * uy); e = (tip[0] - 18 * ux, tip[1] - 18 * uy)
        d.polygon([sp(tip), sp((m[0] + 6 * px, m[1] + 6 * py)), sp(e), sp((m[0] - 6 * px, m[1] - 6 * py))], fill="white", outline=LINE, width=2 * S)
    elif kind == "tri":
        b1 = (tip[0] - 14 * ux + 9 * px, tip[1] - 14 * uy + 9 * py); b2 = (tip[0] - 14 * ux - 9 * px, tip[1] - 14 * uy - 9 * py)
        d.polygon([sp(tip), sp(b1), sp(b2)], fill="white", outline=LINE, width=2 * S)

# garis
for pts, s0, s1, lab, lp in E: poly(pts, id(pts))
gtip = GEN[0]; gbase = (gtip[0], gtip[1] + 14)
d.line([sp(gbase), sp((gx, GEN[1]))], fill=LINE, width=2 * S)
xs = [POS[c][0] for c in GEN[2]]
hline((min(xs), GEN[1]), (max(xs), GEN[1]), -1)
for c in GEN[2]: d.line([sp((POS[c][0], GEN[1])), sp(T(c))], fill=LINE, width=2 * S)
# kotak kelas
for n, (x, y) in POS.items():
    w = bw(n)
    d.rectangle([sp((x - w / 2, y - BH / 2)), sp((x + w / 2, y + BH / 2))], fill="white", outline=INK, width=2 * S)
    d.text(sp((x, y)), n, font=FONT, fill=INK, anchor="mm")
# ujung garis (di atas kotak)
for pts, s0, s1, lab, lp in E:
    if s0: head(pts[0], pts[1], s0)
    if s1: head(pts[-1], pts[-2], s1)
head(gtip, gbase, "tri")
# label
for pts, s0, s1, lab, lp in E:
    if lab:
        tw = FONTL.getlength(lab) / S
        d.rectangle([sp((lp[0] - tw / 2 - 3, lp[1] - 8)), sp((lp[0] + tw / 2 + 3, lp[1] + 8))], fill="white")
        d.text(sp(lp), lab, font=FONTL, fill=LABEL, anchor="mm")
d.text(sp((W / 2, -40)), "Domain Model — Aplikasi Pelaporan Layanan Operasional FSM UNDIP", font=FONTT, fill=INK, anchor="mm")
d.text(sp((W / 2, -18)), "Berlian kosong = agregasi (has-a)  ·  Segitiga kosong = generalisasi (is-a)  ·  Panah = asosiasi  ·  Lengkung kecil = garis bersilangan tanpa sambungan",
       font=FONTL, fill=(110, 110, 110), anchor="mm")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "domain-model.png")
img.save(out); print(out, img.size)
