# OMP Replica

Repo instruksi untuk agen AI mereplikasi setup OMP yang ditangkap pada 2026-11-13. Snapshot nyata, bukan konfigurasi rekomendasi baru.

## Pakai dengan agen AI

Buka repo ini di agen coding pilihanmu, lalu berikan prompt dalam [docs/AGENT-PROMPT.md](docs/AGENT-PROMPT.md). Agen wajib mengikuti [AGENTS.md](AGENTS.md) dan [panduan instalasi](docs/INSTALL.md).

```bash
# Pratinjau: tidak mengubah home dan tidak menginstal paket
python3 scripts/replica.py plan

# Setelah prasyarat dan konflik ditangani
bash scripts/install-runtime.sh
python3 scripts/replica.py apply
python3 scripts/replica.py verify
```

`--home /path/ke/home-uji` pada plan/apply/verify mengarahkan SEMUA file payload ke direktori itu. Ini hanya simulasi pemulihan file, bukan instalasi/login OMP terisolasi. Installer runtime adalah langkah terpisah dan memakai home/runtime shell aktif.

## Isi snapshot

| Komponen | Tangkapan |
| --- | --- |
| OMP | 18.20.0 |
| Bun | 1.4.4 |
| Sistem sumber | macOS x64 |
| Default model tersimpan | `openai-codex/gpt-6.1-terra:low` |
| Tema / simbol | dark-catppuccin / unicode |
| Skill | 10, seluruh referensi disertakan |
| Plugin | graphify-pi, bridge lokal disertakan |
| Browser | relay extension lokal dan Chrome DevTools MCP |
| Provider tambahan | 9router, `http://127.0.0.1:20128/v1` |

Rincian sumber, versi dependency dan lisensi: [docs/ASSETS.md](docs/ASSETS.md). SHA-256 tiap file payload: [manifest.json](manifest.json). Manifest global/lock Bun sumber di `provenance/` adalah bukti inventaris, **bukan** paket instalasi lintas-platform.

## Arti “sama persis”

- File konfigurasi/skill/extension/bridge dipulihkan byte-exact, kecuali kredensial 9router yang sengaja diganti referensi `NINE_ROUTER_API_KEY`.
- Role tersimpan tidak sama dengan model override sesi. Model yang sedang membalas bisa berbeda; repo mempertahankan default tersimpan.
- Prompt inti dan agen bawaan datang dari versi OMP; tidak dibuat salinan prompt percakapan sebagai instruksi global baru.
- Login Codex, key 9router, layanan 9router, akses model akun, izin OS/Chrome, Node dan dependency skill harus tersedia pada mesin tujuan. Tidak disertakan auth, sesi, memori privat, cache atau profil Chrome.
- `update.auto: true` tetap dipertahankan. OMP bisa berubah setelah launch. MCP sumber memakai `chrome-devtools-mcp@latest`; versi server tidak terkunci. Reproduksi file tidak menjamin reproduksi jaringan/model di masa depan.
- Approval bawaan yang teramati: `yolo`; computer use nonaktif. Agen harus menjelaskan risiko auto-approval, bukan mengubah diam-diam.
- Pemulihan menolak symlink dan konflik file. Preflight menolak seluruh operasi sebelum menulis jika konflik sudah ada; kegagalan I/O/race setelah preflight bisa meninggalkan sebagian file baru. Tidak ada auto-delete, rollback destruktif, atau overwrite.

## Verifikasi

```bash
python3 -m unittest discover -s tests -v
```

File parity bukan bukti login/model/browser berfungsi. Panduan instalasi memuat gate fungsional yang wajib diperiksa langsung di mesin tujuan.

## Batas distribusi

Skill dan bridge adalah salinan aset pihak ketiga/lokal, bukan karya yang diklaim ulang. Pertahankan attribution/license yang tersedia. Asal/lisensi sebagian skill lokal belum dapat dibuktikan lengkap; jangan publikasi ulang sebagai proyek berlisensi tunggal tanpa meninjau provenance. Repo ini dibuat lokal terlebih dahulu, tanpa mengunggah kredensial atau riwayat.
