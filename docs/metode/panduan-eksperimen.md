# Panduan Eksperimen: ICONIX Process × Spec-Driven Development × GitHub Spec Kit

> **Tujuan:** menjadi pegangan agar setiap tahap eksperimen berjalan sesuai praktik terbaik dari tiga acuan utama skripsi.
> **Disusun:** 15 Nov 2026, dengan bantuan asisten AI (Claude Code) dari pembacaan langsung ketiga sumber. Isi dan keputusan akhirnya ditentukan peneliti.

| Kode | Sumber | Peran dalam penelitian |
|---|---|---|
| **[R]** | Rosenberg, D. & Stephens, M. (2007). *Use Case Driven Object Modeling with UML: Theory and Practice*. Apress. | Metode analisis dan perancangan (ICONIX Process) |
| **[M]** | Martinelli, S. (2026). *Spec-Driven Development: From Specs to Code with AI Agents*. Apress Pocket Guides. | Prinsip SDD: spesifikasi sebagai kontrak dan sumber kebenaran bagi AI coding agent |
| **[S]** | GitHub Spec Kit v1.4.0 (rilis 10 Nov 2026), dokumentasi resmi di `github.com/github/spec-kit`. | Alat yang menjalankan alur SDD bersama Claude Code |

---

## 1. Gambaran Besar

```text
TAHAP ICONIX (dikerjakan peneliti)                      SPEC KIT + CLAUDE CODE (eksperimen)
──────────────────────────────────                      ───────────────────────────────────
Requirements (sekali untuk seluruh sistem)
  domain model → GUI storyboard → teks use case
  → alokasi requirement → acceptance criteria
  ▼ Milestone 1: Requirements Review                     /speckit-constitution (sekali)

Per use case:
  Robustness analysis → tulis ulang teks use case
  → perbarui domain model (atribut)
  ▼ Milestone 2: Preliminary Design Review
  Sequence diagram → class diagram → skema DB, endpoint
  ▼ Milestone 3: Critical Design Review ───────────────▶ /speckit-specify  (teks use case + AC)
                                                         /speckit-plan     (domain, robustness, sequence, class, DB, API)
                                                         /speckit-tasks    (controller & pesan → tugas)
                                                         /speckit-analyze  (cek konsistensi)
                                                         /speckit-implement
                                                         /speckit-converge (ulang sampai Converged)
  Black-box testing oleh peneliti ◀──────────────────────
  ▼ Code Review and Model Update (selaraskan kode ↔ model)
```

Prinsip yang menyatukan ketiganya:

1. **Spesifikasi adalah kontrak dan sumber kebenaran.** Kode, pengujian, dan dokumentasi diturunkan darinya. Perubahan perilaku selalu dimulai dari spesifikasi [M Bab 1, Bab 10].
2. **Spesifikasi harus "executable".** Dua orang yang membaca harus membayangkan hasil yang sama. Penguji harus bisa menurunkan acceptance criteria darinya, dan AI tidak perlu mengarang aturan [M Bab 4, hlm. 48].
3. **ICONIX adalah cara membuat spesifikasi itu tidak ambigu.** Robustness analysis memaksa teks use case menjadi perilaku konkret yang terikat ke objek [R Bab 5].
4. **Manusia tetap bertanggung jawab.** AI boleh membantu, tetapi review tidak bisa diotomatisasi [M Bab 3 hlm. 32, Bab 10 hlm. 148].

---

## 2. Tahap Requirements

### 2.1 Domain model [R Bab 2]

Sudah dibuat di [`docs/iconix/domain-model.md`](../iconix/domain-model.md). Pedoman yang dipakai:

- Hanya nama kelas, agregasi (*has-a*), dan generalisasi (*is-a*). Tidak ada atribut, operasi, multiplisitas, atau kelas abstrak [R Figure 2-2; Exercise 2-1 dan 2-3 Solution].
- Domain model adalah glosarium proyek. **Semua istilah di teks use case wajib memakai nama kelas domain model** [R Bab 2 pedoman 4; Bab 3 pedoman 2].
- Domain model dianggap belum lengkap. Kelas yang hilang ditemukan saat robustness analysis (*object discovery*) [R Bab 5 pedoman 9].
- Atribut ditambahkan saat robustness analysis. Operasi baru ditambahkan saat sequence diagram [R Bab 1; Bab 5 "Updating Your Domain (Static) Model"].

### 2.2 GUI storyboard [R Bab 3 pedoman 6; Bab 4 pedoman 3]

- Wajib ada sebelum Requirements Review. Cukup berupa gambar garis kasar, bukan desain jadi.
- Setiap halaman diberi nama, dan nama itu dipakai di teks use case (boundary object). Contoh: "Sistem menampilkan halaman Antrean Tiket".
- Semua tombol dan menu yang bisa diklik pengguna digambar, karena setiap tombol bisa memunculkan alternate course (misalnya tombol Batal).

### 2.3 Teks use case

Aturan dari [R Bab 3] dan [M Bab 3–4], beserta cara mendamaikan perbedaannya:

| Aturan | Sumber |
|---|---|
| Kalimat aktif dengan pola **kata benda–kata kerja–kata benda** ("Sistem menyimpan Tiket"). Hindari kalimat pasif ("Tiket disimpan"). | R Bab 3 pedoman 3 dan 8; M Bab 3 "Writing Good Flows" |
| Pola **event/response**: setiap langkah berisi aksi aktor dan respons sistem. Basic course sebaiknya dimulai dengan "Sistem menampilkan halaman X". | R Bab 3 pedoman 7 |
| **Sebut nama halaman (boundary) dan kelas domain** secara eksplisit. | R Bab 3 pedoman 1–2 |
| **Satu langkah, satu perilaku.** Kalimat dengan "dan" atau "atau" sering menyembunyikan dua aturan. | M Bab 4 "One Rule per Statement", hlm. 53 |
| Setiap langkah **dapat diamati dari luar sistem**. Tidak menyebut tabel, query, atau komponen UI. | M Bab 4 "Observable Behavior", hlm. 49 |
| Hindari kata kabur: "biasanya", "secara tepat", "jika perlu", "cepat". | M Bab 4 hlm. 51; Bab 10 Tabel 10-1 |
| Setiap **alternate course merujuk ke langkah tempat ia bercabang** dan menjelaskan respons sistem secara lengkap. | R Bab 3 Exercise 3-2; R Bab 6 pedoman 7; M Bab 3 hlm. 41 |
| **Use case tanpa alternate course adalah tanda bahaya.** Tanyakan "apa lagi yang bisa terjadi?" di setiap langkah. | R Bab 3 "three magic questions"; R Bab 4 |
| **Aturan dua paragraf:** use case harus ringkas. Kalau terlalu panjang, pecah menjadi beberapa use case. | R Bab 3 pedoman 10 |
| **Jangan campur pernyataan "Sistem harus…" (FR) ke dalam langkah use case** (*intermangling*). FR dialokasikan ke use case di bagian terpisah. | R Bab 4 pedoman 7; R Bab 13 |
| Use case adalah dialog aktor–sistem. Perhitungan kompleks (algoritma) ditulis sebagai **satu langkah bernama** dan dirinci di tempat lain. | R Bab 3 "Use Case or Algorithm?" |
| **Aktor selalu berada di luar sistem.** "Sistem" tidak boleh menjadi aktor utama. | R Bab 3 pedoman 9 |
| Relasi antar-use case cukup `<<invokes>>` dan `<<precedes>>`. Fokus pada isi teks, bukan pada panah. | R Bab 3 "Use Case Relationship Roundup" |

**Mendamaikan template.** [R] menolak template panjang dan *precondition*, karena precondition sering membuat langkah "Sistem menampilkan…" terlewat (Exercise 3-2). [M] justru menganjurkan precondition, postcondition, dan business rules karena dibutuhkan agar spesifikasi bisa dieksekusi AI (Bab 4). Jalan tengah yang dipakai dalam penelitian ini:

```text
UC-xx  Nama Use Case                    ← nama memakai istilah domain model
Aktor, Requirement terkait (alokasi), Status
Prasyarat: hanya KEADAAN yang harus benar (bukan langkah navigasi), sesingkat mungkin
BASIC COURSE: langkah bernomor, aktif, event/response, dimulai "Sistem menampilkan halaman X"
ALTERNATE COURSES: Ax (langkah n) kondisi: respons sistem lengkap + keadaan akhir
Postcondition: berhasil / gagal (keadaan yang dapat diperiksa)
Business rules: daftar terpisah ber-ID (bukan disisipkan ke langkah)
Acceptance criteria: Given–When–Then, diturunkan dari basic course, tiap alternate, BR, postcondition
```

### 2.4 Acceptance criteria [M Bab 4 hlm. 60; R Bab 12]

| Sumber di use case | Menjadi |
|---|---|
| Basic course | Satu kriteria alur sukses |
| Setiap alternate course | Satu kriteria per variasi |
| Business rule | Pemeriksaan tingkat aturan |
| Postcondition | Pemeriksaan keadaan akhir |

**Jumlah skenario uji minimal = 1 + jumlah alternate course** [R Bab 1 "Expand Threads"].

### 2.5 Milestone 1: Requirements Review [R Bab 4]

Peserta: Koordinator SI FSM (pemangku kepentingan), peneliti, dan sebaiknya calon pengguna (petugas atau atasan). Bahan: teks use case, domain model, dan GUI storyboard.

**Delapan langkah review** [R Bab 4 pedoman 1]:
1. Buang semua yang di luar cakupan, termasuk langkah yang sebenarnya milik use case lain.
2. Ubah kalimat pasif menjadi aktif.
3. Pastikan teks tidak terlalu abstrak.
4. Pastikan teks mencerminkan GUI (nama halaman dan tombol).
5. Sebut objek domain yang terlibat dengan namanya.
6. Pastikan semua alternate course ada.
7. Telusuri setiap requirement ke use case-nya.
8. Pastikan setiap use case menggambarkan apa yang ingin dicapai pengguna.

Ceklis Top 10 [R Bab 4]:
- domain model memuat ≥80% abstraksi penting dengan bahasa yang dipahami pengguna;
- ada agregasi dan generalisasi;
- use case punya basic dan alternate course dalam kalimat aktif;
- FR tidak tercampur di teks;
- use case dikelompokkan dalam paket dan ada use case diagram;
- teks terikat ke model objek dan ke GUI;
- ada storyboard;
- direview bersama pemangku kepentingan nonteknis.

Hasilnya dicatat di `docs/reviews/` (nama artefak, versi, reviewer, peran, tanggal, keputusan, catatan, dan tindak lanjut).

---

## 3. Tahap Analysis/Preliminary Design (per use case)

### 3.1 Robustness analysis [R Bab 5]

- **Satu diagram per use case**, memuat basic dan **semua** alternate course. Objek alternate course boleh diberi warna lain [R Bab 5 pedoman 1; Bab 6 pedoman 10].
- **Tempel teks use case di diagram** (sebagai note), lalu kerjakan kalimat demi kalimat [R Bab 5 pedoman 10].
- Jenis objek:
  - **boundary** = layar atau halaman (bukan tombol);
  - **entity** = kelas domain model;
  - **controller** = fungsi logis perangkat lunak, biasanya bukan kelas sungguhan [R Bab 5 pedoman 6–7].
- **Aturan sintaks** [R Bab 5 "More About Robustness Diagram Rules"]:
  - aktor ↔ boundary;
  - boundary ↔ controller;
  - controller ↔ controller;
  - controller ↔ entity;
  - **dilarang:** aktor → controller/entity, boundary ↔ boundary, boundary ↔ entity, entity ↔ entity.
- Pakai controller **Display/Inisialisasi halaman** bila halaman perlu mengambil data sebelum tampil [R Bab 5 sidebar "Display controllers"].
- Validasi yang ditulis di teks use case menjadi controller, misalnya "Is Book Review length OK?" [R Bab 3, Bab 5].
- Use case lain yang dipanggil cukup diseret ke diagram [R Bab 5 pedoman 4].
- **Tulis ulang teks use case** sampai teks dan diagram cocok persis [R Bab 5 pedoman 8].
- **Perbarui domain model**: kelas baru dan atribut ya, operasi belum [R Bab 5 "Updating Your Domain Model"].
- Arah panah tidak penting [R Bab 5 pedoman 5]. Jangan masuk ke desain rinci [R Bab 6 pedoman 2].
- Sistem luar (n8n dan bot Telegram) adalah aktor. Endpoint aplikasi yang dipanggil n8n adalah boundary.

### 3.2 Technical architecture [R Bab 7]

Ditetapkan sebelum detailed design: deployment model, pembagian komponen, dan data model. Pilihan didasarkan pada requirement, bukan tren. Sistem luar diidentifikasi beserta perilaku saat tidak tersedia. Pengujian sudah dipikirkan sejak arsitektur (misalnya mock n8n dan cara memajukan waktu untuk menguji cron dan Overdue) [R Bab 7 pedoman 2–4, Don'ts 3].

### 3.3 Milestone 2: Preliminary Design Review [R Bab 6]

**Enam langkah** [R Bab 6 pedoman 1]:
1. diagram cocok dengan teks (*highlighter test*);
2. diagram mengikuti aturan robustness;
3. diagram fokus pada alur logis;
4. semua alternate course tergambar;
5. tidak ada *design-pattern-itis*;
6. diagram belum menjadi desain rinci.

Periksa juga:
- semua entity ada di domain model;
- aliran data dari halaman ke entity dapat ditelusuri;
- kedua sisi dialog tertulis.

Review melibatkan orang nonteknis dan teknis. Arsitektur teknis ikut direview [R Bab 6]. Di penelitian ini, review dikonsultasikan dengan dosen pembimbing (Bab III 3.2.5).

---

## 4. Tahap Detailed Design (per use case)

### 4.1 Sequence diagram [R Bab 8]

**Satu diagram per use case**, memuat basic dan alternate course. Tidak boleh berisi flowchart (alt/loop berlebihan) [R Bab 8 pedoman 9 dan sidebar]. Ada **empat langkah** [R Bab 8 "Four Essential Steps"]:

1. Salin teks use case ke margin kiri.
2. Salin entity dari robustness diagram.
3. Salin boundary dan aktor dari robustness diagram.
4. **Ubah setiap controller menjadi pesan atau operasi** pada kelas yang tepat. Gunakan robustness diagram sebagai ceklis.

Tambahan:
- Sekitar 80% controller menjadi operasi pada kelas entity atau boundary [R Bab 8].
- Tanggung jawab diletakkan di kelas domain yang relevan (*Responsibility-Driven Design*). Hindari kelas "berkepribadian ganda" [R Bab 8 Step 4].
- Tidak perlu repot dengan *focus of control* [R Bab 8 pedoman 5].
- Setiap pesan langsung menjadi operasi di class diagram [R Bab 8 pedoman 4].
- Bersihkan model statis sebelum CDR [R Bab 8 pedoman 1].

### 4.2 Class diagram, skema basis data, dan endpoint

- Domain model berkembang menjadi class diagram (atribut bertipe dan operasi dengan parameter) [R Bab 9 pedoman 3].
- Domain model bukan data model. Skema basis data digambar terpisah dari kelas entitas [R Bab 2 pedoman 6; Bab 10 catatan pedoman 10].
- Daftar endpoint disusun dari controller dan pesan sequence diagram (Bab III 3.2.6).

### 4.3 Milestone 3: Critical Design Review [R Bab 9]

Peserta: pihak teknis saja (peneliti dan dosen pembimbing), **tanpa pemangku kepentingan nonteknis**. Ceklis:
- sequence diagram cocok dengan teks use case (*highlighter test*);
- basic dan alternate course tercakup;
- operasi berada di kelas yang tepat;
- atribut dan operasi lengkap;
- **semua FR dan NFR tertelusur ke use case dan kelas**;
- tipe data dan parameter benar;
- **rencana uji (test plan) direview**.

Artefak yang lolos CDR menjadi versi spesifikasi bagi AI. Beri **tag git** di titik ini, misalnya `uc01-cdr-v1`.

---

## 5. Spec Kit v1.4.0 bersama Claude Code

### 5.1 Instalasi (sekali)

```bash
uv tool upgrade specify-cli          # naik ke v1.4.0, lalu jangan diganti sampai eksperimen selesai
specify version                      # catat di log
specify init --here --force --integration claude --integration-options="--no-model-invocation"
```

- `--here --force` diperlukan karena repo sudah berisi file. Perintah ini tidak menghapus `docs/`. Buat commit dulu agar perubahannya bisa direview [S existing-projects].
- **`--no-model-invocation` disarankan untuk eksperimen.** Dengan opsi ini, skill Spec Kit hanya berjalan ketika peneliti mengetik `/speckit-…`, sehingga Claude tidak bisa memanggilnya sendiri dan setiap tahap tercatat sebagai keputusan peneliti [S integrations/claude].
- Perintah dipanggil sebagai skill: `/speckit-specify`, `/speckit-plan`, dan seterusnya. Penulisan `/speckit.specify` di dokumentasi adalah notasi umum [S agentic-sdd].
- **Branch git tidak dibuat otomatis lagi.** Fitur aktif dicatat di `.specify/feature.json`. Branch per fitur adalah ekstensi opsional (`specify extension add git`) [S quickstart, existing-projects].

**Keputusan: satu branch per use case lewat ekstensi git Spec Kit.**

```bash
specify extension add git            # sekali, langsung setelah init; catat versinya di log
```

- Setiap `/speckit-specify` membuat branch fitur bernomor, misalnya `001-uc-01-…`.
- Semua iterasi use case itu (spesifikasi, kode, perbaikan) dikerjakan di branch tersebut.
- Branch di-merge ke `main` hanya setelah seluruh skenario black-box lulus dan Code Review and Model Update selesai. Dengan begitu `main` hanya berisi use case yang sudah lulus.
- Setelah dipasang, periksa perilaku nyata ekstensi (nama branch, kapan dibuat), lalu catat di log iterasi pertama. Kalau berbeda dari uraian di atas, ikuti perilaku alatnya dan perbarui panduan ini.

### 5.2 Constitution (sekali) [S agentic-sdd; R Bab 7; Bab III Tabel 3.2]

Isinya hanya prinsip yang benar-benar dipegang. Jangan mengarang aturan sekadar untuk mengisi template [S existing-projects §2]. Template bawaan memuat contoh prinsip seperti *Library-First* dan *Test-First (NON-NEGOTIABLE)* [S spec-driven.md]. **Keduanya tidak dipakai mentah-mentah:**
- *Library-First* tidak relevan untuk aplikasi web satu proyek.
- *Test-First* untuk semua lapisan bertentangan dengan Martinelli, yang menempatkan TDD di dalam alur spec-first dan hanya cocok untuk logika bisnis, layanan, dan API, bukan UI [M Bab 6 hlm. 93, 97].

Isi constitution yang ditetapkan (dimasukkan sebagai bahan `/speckit-constitution`):

| No | Prinsip | Dasar |
|---|---|---|
| 1 | **Spesifikasi adalah sumber kebenaran.** Agen hanya mengerjakan use case atau proses sistem yang ID-nya disebut. Perilaku di luar teks use case tidak boleh ditambahkan, dan business rule tidak boleh dilewati. | M Bab 1, Bab 5 |
| 2 | **Alternate course wajib diimplementasikan**, sama seperti basic course. | R Bab 10 pedoman 1 |
| 3 | **Keterlacakan.** ID use case (UC-xx/PS-xx), FR, dan BR dirujuk di nama tes, komentar seperlunya, dan pesan commit (Conventional Commits, bahasa Indonesia). | M Bab 4; R Bab 13 |
| 4 | **Teknologi:** Next.js + TypeScript, PostgreSQL, REST API. Bot Telegram dan n8n memanggil endpoint yang sama dengan aplikasi web. | Bab III, technical architecture [R Bab 7] |
| 5 | **Keamanan:** otorisasi peran diperiksa di backend. Secret (kunci OpenRouter, token bot, kredensial n8n) tidak pernah dikirim ke client atau di-commit. | NFR |
| 6 | **Integrasi n8n:** kegagalan atau timeout n8n tidak menggagalkan transaksi utama (misalnya Tiket tetap tersimpan). Alur di dalam n8n **di luar cakupan agen**. | K-14; Bab III |
| 7 | **Tes dua lapis.** Agen menulis unit/integration test dari spesifikasi: minimal satu per controller robustness, satu per alur, dan satu per business rule. Nama tes memuat ID use case, dan assertion memakai postcondition, bukan detail internal. Tes ini wajib direview peneliti dan **tidak menentukan kelulusan**. Kelulusan ditentukan black-box test peneliti. | R Bab 1 hlm. 17–18, Bab 12; M Bab 6 hlm. 94, 97; Bab III 3.2.9 |
| 8 | **Sinkronisasi, bukan regenerasi.** Kalau use case berubah, ubah hanya bagian kode yang terdampak. | M Bab 5 hlm. 76–78 |

Template `tasks.md` Spec Kit menganggap tugas tes **opsional dan hanya dibuat kalau diminta** [S tasks-template]. Prinsip no. 7 membuat permintaan itu eksplisit, sehingga setiap `tasks.md` memuat tugas tes.

### 5.3 Template spesifikasi berformat use case [S customization]

Template bawaan `spec.md` berbentuk user story (User Story P1/P2/P3, Acceptance Scenarios, FR-001, Success Criteria). Agar sesuai Bab III 3.2.8.1, pasang **project-local override** di:

```text
.specify/templates/overrides/spec-template.md
```

Isinya mengikuti format §2.3 di atas: identitas, alokasi requirement, prasyarat, basic course, alternate courses, postcondition, business rules, dan AC. Urutan resolusi template: override proyek → preset → ekstensi → bawaan [S customization]. Preset baru diperlukan kalau template ingin dipakai di banyak proyek.

### 5.4 Tahap per use case

| Perintah | Masukan dari ICONIX | Catatan praktik terbaik |
|---|---|---|
| `/speckit-specify` | Teks use case final (setelah PDR) dan AC | Fokus pada *apa* dan *mengapa*, tanpa teknologi [S]. Otomatis membuat `checklists/requirements.md` [S]. |
| `/speckit-clarify` *(opsional)* | — | Bab III menyatakan tidak dipakai karena ambiguitas sudah dibereskan di Requirements Review dan PDR. Kalau `analyze` menemukan celah requirement, kembali ke sini [S]. |
| `/speckit-plan` | Domain/class diagram, robustness, sequence, skema DB, endpoint, arsitektur | Di sinilah teknologi disebut [S]. Menghasilkan `plan.md`, `research.md`, `data-model.md`, `contracts/`, `quickstart.md`. Rujuk file di `docs/iconix/UC-xx/`, jangan disalin. |
| `/speckit-tasks` | Controller (robustness) dan pesan (sequence) | Fase: Setup → Foundational → per user story → Polish [S]. Periksa setiap controller punya tugas. |
| `/speckit-analyze` | — | **Read-only.** Kalau ada masalah, perbaiki di artefak sumbernya lalu ulangi [S]. |
| `/speckit-implement` | Semua di atas | Untuk fitur besar, jalankan per fase dan periksa setiap tahap [S]. Perintah selalu menyebut ID use case: "Implement UC-01" [M Bab 5]. |
| `/speckit-converge` | — | **Append-only**: hanya menambah tugas ke `tasks.md`. Ulangi implement → converge sampai `Converged` [S]. Converge bukan penentu kelulusan, karena kelulusan ditentukan black-box testing (Bab III 3.2.8.2). |

### 5.5 Struktur proyek Next.js

Martinelli membuat kerangka proyek dengan generator atau template standar, bukan lewat AI [M Bab 8 Step 5]. Bab III menyatakan kode dibuat AI. Karena itu **kerangka Next.js dibuat agen pada fase Setup di `tasks.md` use case pertama**. Kalau peneliti terpaksa membuatnya sendiri, catat sebagai intervensi.

---

## 6. Implementasi, Sinkronisasi, dan Review Kode

- **Kode diturunkan langsung dari desain. Kalau desain ternyata salah, perbaiki desainnya lalu tinjau ulang prosesnya** [R Bab 10 pedoman 9–10]. Di Spec Kit: perbaiki di artefak sumber, bukan di kode [S evolving-specs].
- **Alternate course wajib diimplementasikan** [R Bab 10 pedoman 1].
- **Sinkronisasi, bukan regenerasi.** Kalau use case berubah, terapkan hanya perubahan perilakunya supaya diff kecil dan mudah direview [M Bab 5 hlm. 76–78].
- **Urutan review:** spesifikasi lebih dulu, baru kode [M Bab 5 hlm. 75]:
  1. review spesifikasi;
  2. pastikan perilakunya benar;
  3. review implementasi;
  4. cek kode cocok dengan spesifikasi;
  5. cek test mencakup semua alur dan aturan.
- **Kode yang menambah perilaku di luar use case, atau melewatkan business rule, adalah masalah** [M Bab 5].
- **Code Review and Model Update** [R Bab 11]:
  - daftar review diturunkan dari judul use case, lalu dirinci per controller;
  - telusuri teks use case → sequence diagram → kode;
  - fokus mencari kesalahan, bukan memperbaikinya di tempat;
  - hasilnya: kode diselaraskan ke model, atau model diperbarui.

---

## 7. Pengujian

| Aturan | Sumber |
|---|---|
| Uji sejak awal: siapkan kasus uji segera setelah robustness analysis, bukan setelah kode selesai | R Bab 12 Don'ts 7 |
| **Skenario uji per use case = basic course + setiap alternate course** | R Bab 1, Bab 12 pedoman 3–4 |
| Satu kasus uji per controller pada robustness diagram, dan satu skenario per alur use case | R Bab 12 "Driving Test Cases from Robustness Diagrams" |
| Gunakan matriks ketertelusuran requirement → use case → test | R Bab 12 pedoman 5; Bab 13 |
| Tes melindungi **perilaku yang dapat diamati**, bukan struktur internal | M Bab 6 hlm. 87 |
| **AI boleh membuat tes, tetapi tidak bisa memastikan kebenarannya.** Setiap tes harus direview manusia. | M Bab 6 hlm. 97 |
| Tiga pertanyaan untuk setiap tes: (1) apakah assert cocok dengan postcondition? (2) apakah setup hanya memakai prasyarat? (3) **apakah tes gagal kalau aturannya sengaja dirusak?** | M Bab 6 hlm. 94 |
| Cakupan diukur terhadap spesifikasi: setiap alur dan setiap business rule harus teruji | M Bab 6 hlm. 95 |
| Jangan berlebihan memakai mock. Mock n8n hanya untuk mensimulasikan respons dan kegagalan sistem luar. | R Bab 12 Don'ts 10 |

Dalam penelitian ini pengujian dibagi **dua lapis** (Bab III 3.2.9):

| Lapis | Dibuat oleh | Isi | Fungsi |
|---|---|---|---|
| Unit/integration test otomatis | Agen, pada tahap implement | Minimal satu per controller [R], satu per alur, dan satu per business rule [M]. Assertion memakai postcondition. | Pengaman regresi selama iterasi. Direview peneliti dengan tiga pertanyaan di atas, dan hasil review dicatat di log iterasi. **Tidak menentukan kelulusan.** |
| Black-box test (acceptance) | **Peneliti**, dari AC | Satu skenario untuk basic course dan untuk setiap alternate course | **Penentu kelulusan use case.** Dicatat di `docs/pengujian/UC-xx.md` beserta statusnya (Lulus/Gagal/Tidak dapat dijalankan). |

Kalau tes buatan agen gagal pada pertanyaan ketiga (tetap lulus saat aturan sengaja dirusak), catat sebagai temuan kualitas tes buatan AI di log iterasi. Temuan ini bisa menjadi bahan pembahasan Bab IV.

---

## 8. Pencatatan Data Penelitian

| Yang dicatat | Tempat |
|---|---|
| Versi artefak yang diserahkan ke agen | Tag git (`uc01-cdr-v1`) |
| Versi Spec Kit, versi Claude Code, model, dan effort | `docs/eksperimen/log/UC-xx-iterasi-n.md` |
| Perintah dan prompt yang diberikan, disalin apa adanya | Log iterasi |
| Hasil converge dan hasil black-box per skenario | Log iterasi dan `docs/pengujian/` |
| Penyimpangan kode terhadap use case beserta dugaan penyebabnya (spesifikasi kurang jelas atau kesalahan agen) | Log iterasi |
| Intervensi peneliti (umpan balik, perbaikan artefak, edit manual) | Log iterasi |
| Perubahan desain beserta alasannya | Commit `docs(uc01): …` dan log |

Sesi Claude Code untuk **diskusi** dan untuk **eksperimen** dipisahkan. Eksperimen dijalankan di sesi baru supaya agen hanya membaca repo, bukan riwayat percakapan.

---

## 9. Temuan yang Perlu Ditindaklanjuti

Hasil membandingkan dokumen saat ini dengan ketiga sumber:

| No | Temuan | Dasar | Usulan | Status |
|---|---|---|---|---|
| 1 | **UC-47 memakai "Sistem" sebagai aktor utama.** Menurut ICONIX, aktor harus berada di luar sistem, dan proses yang seluruhnya dikerjakan sistem adalah algoritma, bukan use case. | R Bab 3 pedoman 9; "Use Case or Algorithm?" | Klasifikasi menjadi langkah bernama di UC-01, lalu dirinci sebagai proses sistem. | **Selesai (K-15):** UC-47 menjadi PS-01, dan n8n menjadi aktor sekunder UC-01. |
| 2 | **UC-32 langkah 6** (penjadwal membuat tugas rutin) bukan bagian dialog atasan, karena terjadi kemudian dan dipicu waktu. | R Bab 3 (use case = dialog); M Bab 3 (satu tujuan per use case) | Catat sebagai proses sistem bernama. | **Selesai (K-16):** menjadi PS-02. Penandaan Overdue menjadi PS-03. |
| 3 | **Istilah di teks use case belum sama dengan domain model.** Contoh: "completion attempt"/"hasil" vs `HasilPekerjaan`, "timeline" vs `TimelineEvent`, "log klasifikasi"/"tanda belum terklasifikasi" vs `Klasifikasi`. | R Bab 3 pedoman 2; Bab 4 langkah 5 | Samakan semua istilah dengan nama kelas domain model. | **Selesai (K-17)**, di requirement draf 3. |
| 4 | **Ada kalimat pasif** di teks use case, misalnya "tiket tidak dibuat" dan "status tidak berubah". | R Bab 3 pedoman 8; Bab 4 langkah 2 | Ubah menjadi aktif: "Sistem tidak menyimpan Tiket". | **Selesai (K-17)**, di requirement draf 3. |
| 5 | **GUI storyboard belum ada.** | R Bab 4 pedoman 3 | Buat sketsa setiap halaman yang disebut di use case (daftar halaman ada di requirement Bagian 11). | Belum: sebelum Requirements Review |
| 6 | Beberapa use case cukup panjang (UC-05 punya 5 alternate, UC-18 punya 6). | R Bab 3 aturan dua paragraf | Periksa saat robustness analysis. Kalau diagramnya terlalu padat, pecah use case-nya. | Belum: tahap Analysis |
| 7 | **Bab III Tabel 3.2** menyebut keluaran implement adalah "kode sumber dan pengujian yang dihasilkan AI", sedangkan **3.2.9** menyatakan kasus uji tidak diserahkan ke AI. | M Bab 6 hlm. 97 | Tegaskan di Bab III dan constitution: tes otomatis buatan agen boleh ada sebagai pelengkap, tetapi **kelulusan ditentukan kasus uji black-box buatan peneliti**. | **Selesai:** pengujian dua lapis berdasarkan R Bab 1 & 12 dan M Bab 6. Naskah 2.2.13, Tabel 3.2, 3.2.8.2, dan 3.2.9 sudah direvisi. Lihat §5.2 no. 7 dan §7. |
| 8 | Spec Kit v1.4.0 tidak lagi membuat branch otomatis, karena branch kini ekstensi opsional. (Koreksi: naskah Bab III ternyata tidak menyebut branch, jadi naskah tidak perlu diubah.) | S quickstart | Putuskan: pakai `specify extension add git`, atau buat branch manual per use case. | **Selesai:** ekstensi git, satu branch per use case, merge setelah lulus (§5.1). Diterapkan saat instalasi. |
| 9 | Template constitution bawaan Spec Kit berisi Test-First (TDD oleh agen) dan Library-First. | S spec-driven.md | Jangan mengikuti template mentah-mentah. Isi constitution sesuai §5.2. | **Selesai:** isi ditetapkan di §5.2 (8 prinsip). Diterapkan saat `/speckit-constitution`. |
