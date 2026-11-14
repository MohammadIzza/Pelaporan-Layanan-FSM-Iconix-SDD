# Pelaporan Layanan FSM — ICONIX × Spec-Driven Development

Rancang bangun aplikasi pelaporan layanan operasional Fakultas Sains dan Matematika (FSM) Universitas Diponegoro berbasis Progressive Web App. Aplikasi dirancang dengan **ICONIX Process** dan dibangun dengan pendekatan **Spec-Driven Development** menggunakan AI coding agent (Claude Code) melalui GitHub Spec Kit, dengan integrasi **n8n**.

Repositori ini adalah bagian dari skripsi Program Studi Informatika, Universitas Diponegoro:

> *Rancang Bangun Aplikasi Pelaporan Layanan Operasional Fakultas Sains dan Matematika Universitas Diponegoro Menggunakan Metode ICONIX Process dan Pendekatan Spec-Driven Development dengan Integrasi n8n*
>
> Mohammad Izza Hakiki (24060123140139)

## Cakupan

Aplikasi mencakup 11 use case inti dalam tiga proses bisnis:

| Proses | Use case |
|---|---|
| Permintaan layanan ad-hoc | UC-01 Membuat Permintaan Layanan, UC-47 Mengklasifikasikan Tiket, UC-54 Mengklasifikasikan Tiket Secara Manual, UC-09 Claim Tiket, UC-15 Menyelesaikan Pekerjaan, UC-05 Memverifikasi Hasil Pekerjaan |
| Laporan pekerjaan mandiri | UC-16 Membuat Laporan Pekerjaan Mandiri, UC-29 Memverifikasi Laporan Mandiri |
| Tugas rutin terjadwal | UC-32 Membuat Jadwal Tugas Rutin, UC-18 Menjalankan Tugas Rutin, UC-30 Memverifikasi Tugas Rutin |

Rincian kebutuhan, teks use case, dan acceptance criteria ada di [`docs/requirements/use-case-inti.md`](docs/requirements/use-case-inti.md).

## Metode

```text
Requirements ─► Milestone 1: Requirements Review
   │
   └─► per use case:
       Robustness Analysis ─► Milestone 2: Preliminary Design Review
       Sequence + Class Diagram ─► Milestone 3: Critical Design Review
       Spec Kit: specify ─► plan ─► tasks ─► analyze ─► implement ─► converge
       Black-box testing ─► perbaikan iteratif sampai seluruh skenario lulus
```

- Analisis dan perancangan dilakukan oleh peneliti.
- AI coding agent hanya dipakai pada tahap implementation.
- Kasus uji disusun peneliti dari acceptance criteria. Kasus uji tidak dibuat oleh AI.

## Struktur Repositori

| Lokasi | Isi |
|---|---|
| `docs/` | Dokumen penelitian yang disusun peneliti: kebutuhan dan teks use case (`requirements/`), draf proposal skripsi Bab I–III sebagai konteks penelitian (`skripsi/`), serta templat catatan iterasi (`eksperimen/`) |

Struktur lain dibuat otomatis oleh GitHub Spec Kit (`specify init` dan tahap `/speckit.*`) dan oleh AI coding agent saat membangun aplikasi Next.js.

## Status

Tahap **Requirements** sedang berjalan dan belum melalui Milestone 1: Requirements Review.
