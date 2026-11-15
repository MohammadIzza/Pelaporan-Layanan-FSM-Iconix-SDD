# Milestone 1: Requirements Review

**Proyek:** Aplikasi Pelaporan Layanan Operasional FSM UNDIP
**Tahap ICONIX:** akhir tahap Requirements (Subbab 3.2.3) [Rosenberg & Stephens, 2007, Bab 4]
**Peserta:** Koordinator Sistem Informasi FSM UNDIP (pemangku kepentingan) dan peneliti. Sebaiknya juga satu calon pengguna, yaitu petugas layanan atau atasan.
**Status:** bahan disiapkan. Sesi review belum dilaksanakan.

> **Catatan asal-usul.** Bahan ini dan hasil pra-pemeriksaan di Bagian B disiapkan dengan bantuan asisten AI (Claude Code) atas arahan peneliti (Bab III 3.2.8.1). Keputusan review sepenuhnya diambil peneliti bersama Koordinator SI FSM.

---

## Bagian A — Bahan Sesi Review

### A.1 Tujuan

Menyamakan pemahaman tentang **apa yang akan dibangun** sebelum perancangan dimulai. Yang dipastikan dalam sesi ini:
1. Alur kerja di aplikasi sesuai dengan cara kerja layanan operasional FSM yang sebenarnya.
2. Tidak ada kebutuhan penting yang terlewat, dan tidak ada yang dibangun di luar kebutuhan.
3. Istilah, aturan, dan tampilan bisa dipahami pengguna.

Hasil sesi ini menjadi dasar tahap berikutnya (analysis/preliminary design). Perubahan yang diminta di sesi ini jauh lebih murah dilakukan sekarang daripada setelah aplikasi dibangun.

### A.2 Bahan yang ditinjau

| Bahan | Lokasi | Isi singkat |
|---|---|---|
| Teks use case dan acceptance criteria | [`docs/requirements/use-case-inti.md`](../requirements/use-case-inti.md), draf 3.5 | 10 use case inti, 3 proses sistem, 63 kebutuhan fungsional, 64 skenario uji, keputusan K-1 sampai K-28 |
| Domain model | [`docs/iconix/domain-model.md`](../iconix/domain-model.md) | 21 istilah utama (Tiket, Laporan Mandiri, Tugas Rutin, dan lainnya) beserta hubungannya |
| GUI storyboard dan prototype | [`docs/iconix/storyboard/`](../iconix/storyboard/) | 123 layar dalam 4 zona; 50 flow prototype (satu flow per skenario) yang bisa dicoba di FigCraft lewat Present |

**Persiapan teknis:**
- buka `storyboard.figcraft` di FigCraft;
- siapkan keempat PNG per proses sebagai cadangan atau untuk dicetak;
- siapkan dokumen use case untuk dirujuk bila ada pertanyaan rinci.

### A.3 Agenda (± 90 menit)

| Waktu | Kegiatan | Bahan |
|---|---|---|
| 10 menit | Pembukaan: tujuan, cakupan 3 proses bisnis, dan yang **tidak** dibangun | A.4 |
| 10 menit | Istilah: apakah domain model sudah mewakili objek nyata di layanan FSM? | Domain model, glosarium |
| 50 menit | Telusur alur per proses bisnis dengan prototype | A.5 |
| 15 menit | Keputusan dan konfirmasi aturan | A.6 |
| 5 menit | Kesimpulan, daftar perbaikan, dan keputusan milestone | Bagian C |

### A.4 Cakupan yang perlu dikonfirmasi

**Dibangun:**

| Proses bisnis | Use case | Proses sistem (tanpa halaman) |
|---|---|---|
| Permintaan layanan ad-hoc | UC-01 Membuat Permintaan Layanan, UC-54 Mengklasifikasikan Tiket Secara Manual, UC-09 Claim Tiket, UC-15 Menyelesaikan Pekerjaan, UC-05 Memverifikasi Hasil Pekerjaan | PS-01 Klasifikasikan Tiket (AI melalui n8n) |
| Laporan pekerjaan mandiri | UC-16 Membuat Laporan Pekerjaan Mandiri, UC-29 Memverifikasi Laporan Mandiri | — |
| Tugas rutin terjadwal | UC-32 Membuat Jadwal Tugas Rutin, UC-18 Menjalankan Tugas Rutin, UC-30 Memverifikasi Tugas Rutin | PS-02 Buat Tugas Rutin Terjadwal, PS-03 Tandai Tugas Overdue |

Bot Telegram menjadi jalur kedua untuk membuat laporan, mengerjakan Tiket, Laporan Mandiri, dan Tugas Rutin.

**Tidak dibangun:** rincian lengkap ada di Bagian 8 dokumen use case. Yang perlu dikonfirmasi Koordinator:
- pengelolaan data oleh admin (Pengguna, Jenis Tiket, Skill, dan lainnya) disiapkan sebagai **data awal**, tanpa halaman pengelolaan;
- tidak ada SLA, dashboard pimpinan, penugasan otomatis, penutupan otomatis, dan form khusus per Jenis Tiket;
- tidak ada fitur status/timeline/komentar Tiket (UC-02–UC-04), pause/progress (UC-10–UC-14), dan laporan retrospektif (UC-17);
- tidak ada unggahan file selain foto.

### A.5 Urutan telusur prototype

Setiap flow di FigCraft dinamai `UC-xx · …`, dan deskripsinya memuat skenario uji serta acceptance criteria-nya. Untuk menghemat waktu, telusuri **basic course** setiap use case, lalu alternate course yang paling berpengaruh pada proses kerja. Flow lain tetap tersedia kalau Koordinator ingin melihatnya.

| No | Flow | Pertanyaan pemandu untuk Koordinator |
|---|---|---|
| 1 | `UC-01 · Basic course` | Apakah isian laporan (deskripsi, satu foto, lokasi opsional) cukup bagi pelapor di FSM? |
| 2 | `UC-01 · A4 PS-01 gagal` | Bila AI gagal mengklasifikasi, Tiket tetap masuk dan diklasifikasi manual. Apakah ini sesuai? |
| 3 | `UC-54 · Basic course` | Siapa atasan yang ditunjuk mengklasifikasi Tiket (K-13)? |
| 4 | `UC-09 · Basic course`, `UC-09 · A2` | Apakah aturan "siapa cepat dia dapat" sesuai praktik petugas? |
| 5 | `UC-15 · Basic course` | Apakah bukti selesai (catatan dan satu foto hasil) cukup? |
| 6 | `UC-05 · Basic course`, `UC-05 · A1` | Apakah pelapor yang memverifikasi dan memberi rating 1–5 sesuai harapan? |
| 7 | `UC-16 · Basic course` | Apakah laporan mandiri (pekerjaan yang ditemukan sendiri oleh petugas) dengan foto awal wajib sesuai praktik? |
| 8 | `UC-29 · Basic course`, `UC-29 · A1` | Apakah atasan langsung yang memverifikasi laporan mandiri? |
| 9 | `UC-32 · Basic course` | Apakah isian jadwal (area, checklist wajib/opsional, pola hari, jam, bukti, petugas) mencakup kebutuhan tugas rutin? |
| 10 | `UC-18 · Basic course`, `UC-18 · A3 Overdue` | Apakah tugas yang terlambat tetap boleh diajukan dengan tanda Overdue permanen? |
| 11 | `UC-30 · Basic course` | Apakah atasan langsung yang memverifikasi tugas rutin? |
| 12 | `Pendukung · Masuk dan penautan Telegram` | Bagaimana cara login yang diinginkan (lihat A.6 no. 2)? |

**Pertanyaan umum untuk setiap use case** (langkah 8 Rosenberg): *"Apakah alur ini menggambarkan apa yang sebenarnya ingin dicapai pengguna?"*

### A.6 Keputusan dan konfirmasi yang dibutuhkan dari Koordinator

| No | Hal | Keadaan saat ini | Yang perlu diputuskan |
|---|---|---|---|
| 1 | **Bahasa label status** | Campuran: Open, Assigned, In Progress, Reopen, Closed, Overdue; tetapi juga Menunggu Verifikasi dan Aktif | Tetap campuran, atau diseragamkan ke Bahasa Indonesia (misalnya Baru, Diambil, Dikerjakan, Menunggu Verifikasi, Dibuka Kembali, Selesai, Terlambat)? Dasarnya NFR-USE-001/004: status harus mudah dipahami Pelapor. |
| 2 | **Cara login** [USULAN] | Email UNDIP dan kata sandi | Memakai SSO UNDIP, atau akun khusus aplikasi? Bagaimana pesan saat login gagal? |
| 3 | **Isi Halaman Profil** [USULAN] | Nama, Peran, Unit Kerja (hanya dibaca) | Apakah cukup? |
| 4 | **Teks petunjuk kode Telegram** [USULAN] | "Kirim kode ini ke bot Telegram aplikasi." | Setuju, atau perlu nama bot tertentu? |
| 5 | **Daftar Jadwal Tugas Rutin** | Hanya menampilkan jadwal; tidak bisa diubah atau dinonaktifkan | Perlukah ubah atau nonaktifkan jadwal? Kalau ya, ini menambah use case baru. Kalau tidak, dicatat sebagai saran (Bab V). |
| 6 | **Tugas Rutin yang sudah diajukan** | Belum diatur apa yang terjadi bila Petugas memilihnya di Tugas Rutin Hari Ini | Bisa dibuka hanya untuk dilihat, atau tidak bisa dipilih? |
| 7 | **Aturan bisnis yang perlu dikonfirmasi** | Lihat daftar di bawah | Konfirmasi setiap butir, atau ubah |
| 8 | **Data awal** | Belum ada | Siapa yang menyediakan, dan kapan? Daftarnya di bawah. |
| 9 | **Kelengkapan istilah** | 21 istilah di domain model | Apakah ada objek nyata di layanan FSM yang belum terwakili (pedoman ≥ 80% abstraksi penting)? |

**Aturan bisnis untuk dikonfirmasi (no. 7):**
- Pelapor **tidak dapat membatalkan** Tiket yang sudah dikirim (BR-018).
- Petugas **tidak dapat meng-claim Tiket yang ia laporkan sendiri**. Pekerjaan sesuai keahliannya dicatat sebagai Laporan Mandiri (K-6).
- Jenis pekerjaan Laporan Mandiri hanya dari Jenis Tiket yang sesuai Skill Petugas (K-4), dan **foto awal wajib** (K-18).
- Penolakan oleh Pelapor atau Atasan **wajib disertai alasan**, dan pekerjaan kembali ke petugas yang sama (K-5, FR-VER-004/006).
- Rating 1–5 **wajib** saat Pelapor menerima hasil. Komentar opsional, dan keduanya terkunci setelah Tiket selesai (FR-VER-011/012/014).
- Hanya **satu Atasan yang ditunjuk** yang dapat mengklasifikasi Tiket secara manual (K-13).
- Klasifikasi AI ditunggu **paling lama 30 detik**. Setelah itu Tiket ditandai Belum terklasifikasi (K-14).
- Foto: **satu foto JPG/PNG maksimal 5 MB** per unggahan (K-19).
- Bukti Tugas Rutin (foto akhir, GPS) **mengikuti pengaturan jadwal**; jadwal boleh tidak mewajibkan bukti (K-20).
- Tanda Overdue **permanen**, dan tugas yang terlambat tetap boleh diselesaikan (BR-037).
- Bot Telegram dapat dipakai **semua pengguna aktif**. Kode penautan berlaku **10 menit** (K-12, K-23).

**Data awal yang dibutuhkan (no. 8):**
- Pengguna, Peran, dan status aktif;
- struktur atasan–bawahan, termasuk Atasan yang ditunjuk sebagai pengklasifikasi;
- daftar **Jenis Tiket** dan **Skill** yang dibutuhkan setiap jenis;
- Skill setiap Petugas;
- daftar **Unit Kerja**;
- daftar **Area Kerja** (gedung dan lantai) untuk tugas rutin.

---

## Bagian B — Pra-pemeriksaan Peneliti (sebelum sesi)

### B.1 Ceklis Top 10 Requirements Review [Rosenberg & Stephens, 2007, Bab 4]

| No | Pedoman | Status | Bukti |
|---|---|---|---|
| 10 | Domain model memuat ≥ 80% abstraksi penting dalam bahasa yang dipahami pengguna | **Perlu konfirmasi** | 21 kelas dengan glosarium berbahasa Indonesia; kecukupannya dinilai Koordinator (A.6 no. 9) |
| 9 | Domain model menunjukkan generalisasi dan agregasi | Terpenuhi | `Pekerjaan` digeneralisasi menjadi Tiket, Laporan Mandiri, dan Tugas Rutin; ada relasi has-a |
| 8 | Use case memuat basic dan alternate course dalam kalimat aktif | Terpenuhi | Semua langkah memakai klausa utama aktif; setiap alternate course punya AC (K-28) |
| 7 | FR tidak tercampur di teks use case | Terpenuhi | FR di tabel Bagian 4 dan dirujuk lewat baris Requirement; business rule terpisah (K-17) |
| 6 | Use case dikelompokkan dalam paket dan punya use case diagram | Terpenuhi | 3 paket proses bisnis di use case diagram (Bagian 3.3) |
| 5 | Use case ditulis dalam konteks model objek | Terpenuhi | Istilah berhuruf kapital adalah kelas domain model; semua kelas dipakai di teks |
| 4 | Use case ditulis dalam konteks antarmuka | Terpenuhi | Setiap langkah menyebut halaman dan tombol; konvensi Bagian 7 |
| 3 | Use case dilengkapi storyboard atau prototype | Terpenuhi | 123 layar dan 50 flow prototype |
| 2 | Direview bersama pengguna dan pemangku kepentingan nonteknis | **Sesi ini** | — |
| 1 | Review mengikuti "delapan langkah" | Lihat B.2 | — |

### B.2 Delapan langkah memperbaiki use case [Rosenberg & Stephens, 2007, Bab 4]

| No | Langkah | Hasil pra-pemeriksaan |
|---|---|---|
| 1 | Buang yang di luar cakupan | Proses yang seluruhnya dijalankan sistem dipisah menjadi PS-01–PS-03 (K-15, K-16). Percakapan bot dan alur n8n di luar ICONIX. Daftar Bagian 8 dikonfirmasi di A.4. |
| 2 | Ubah kalimat pasif menjadi aktif | Klausa utama semua langkah aktif. Bentuk "di-" hanya muncul di frasa keterangan atau teks pesan. |
| 3 | Pastikan teks tidak terlalu abstrak | Semua pesan ditulis kata per kata, dan isi halaman ditetapkan (K-22, K-24, K-27). |
| 4 | Teks mencerminkan GUI | Nama halaman dan tombol sama persis dengan storyboard. Temuan storyboard dimasukkan sebagai K-18–K-27. |
| 5 | Sebut objek domain dengan namanya | Semua istilah memakai nama kelas domain model (K-17). |
| 6 | Semua alternate course ada | 64 skenario uji minimal; setiap alternate punya AC (K-28). |
| 7 | Telusuri setiap requirement ke use case | Ke-63 FR sudah dirujuk minimal satu use case atau proses sistem (diperiksa otomatis). |
| 8 | Use case menggambarkan tujuan pengguna | **Dikonfirmasi di sesi** (pertanyaan umum di A.5). |

### B.3 Pemeriksaan silang (Subbab 3.2.3)

| Pemeriksaan | Hasil |
|---|---|
| Setiap FR terwakili use case | 63/63 FR dirujuk |
| Setiap objek pada use case ada di domain model | Semua kelas domain model muncul di teks; tidak ditemukan istilah domain yang tidak terdaftar |
| Setiap alternate course punya acceptance criteria | Terpenuhi setelah K-28 |
| Setiap halaman di teks use case punya storyboard | Ke-20 halaman di Bagian 11 dokumen use case (termasuk Halaman Profil) ditambah Halaman Masuk |

---

## Bagian C — Catatan Hasil Review (diisi saat sesi)

**Tanggal:** ……………… **Tempat:** ……………… **Durasi:** ………

| Artefak | Versi | Reviewer | Peran | Keputusan* | Catatan |
|---|---|---|---|---|---|
| Teks use case dan AC | draf 3.5 | | Koordinator SI FSM | | |
| Domain model | 15 Nov 2026 | | Koordinator SI FSM | | |
| GUI storyboard dan prototype | commit `efee6f2` | | Koordinator SI FSM | | |

\* Disetujui / Disetujui dengan perbaikan / Perlu review ulang

### C.1 Jawaban atas A.6

| No | Keputusan Koordinator | Dampak ke dokumen |
|---|---|---|
| 1 Bahasa label status | | |
| 2 Cara login | | |
| 3 Isi Halaman Profil | | |
| 4 Teks petunjuk kode | | |
| 5 Daftar Jadwal | | |
| 6 Tugas Rutin yang sudah diajukan | | |
| 7 Aturan bisnis | | |
| 8 Data awal | | |
| 9 Kelengkapan istilah | | |

### C.2 Daftar perbaikan

| No | Artefak / UC / halaman | Temuan | Perbaikan yang disepakati | Status |
|---|---|---|---|---|
| 1 | | | | Belum |
| 2 | | | | Belum |

### C.3 Keputusan milestone

- [ ] **Lulus:** lanjut ke analysis/preliminary design, dimulai dari UC-01 dan PS-01.
- [ ] **Lulus dengan perbaikan:** perbaikan di C.2 diselesaikan dulu, lalu lanjut tanpa sesi ulang.
- [ ] **Perlu review ulang:** jadwalkan sesi berikutnya.

Tanda tangan / konfirmasi: ………………………… (Koordinator SI FSM)  ………………………… (Peneliti)
