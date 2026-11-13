# Prompt untuk agent pemasang

Salin instruksi berikut ke agent di mesin target. Jalankan dari checkout repo `omp-replica` yang sudah dipercaya.

---

Replikasikan setup OMP non-rahasia dari repo ini ke akun saya dengan aman. Baca `AGENTS.md`, `README.md`, `docs/INSTALL.md`, manifest, dan skrip sebelum bertindak. Ikuti instruksi repo serta skill yang relevan. Jangan push atau mengubah snapshot tanpa permintaan saya.

## Kontrak

- Target runtime: OMP **18.20.0**, Bun **1.4.4**; sumber macOS x64. Gunakan `scripts/install-runtime.sh`, bukan installer `latest` atau `omp update`.
- Gunakan `python3 scripts/replica.py plan`, `apply`, dan `verify`, semuanya dengan `--home` tujuan yang sama; default adalah home pengguna. `--home` hanya mengarahkan restore payload, bukan mengalihkan runtime global atau login OMP.
- Pertahankan hash manifest dan larangan menimpa berkas berbeda. Bila konflik, laporkan path dan tunggu keputusan saya tentang berkas itu; lanjutkan pekerjaan independen yang aman. Jangan menghapus konfigurasi lama atau melewati hash untuk memaksakan restore.
- Jangan membaca, menyalin, mengekspor, mencetak, atau memasukkan ke repo: API key, OAuth, auth vault, session, database, history, private memory, cookie, profil browser, atau storage login. Jangan meminta rahasia di chat. Login/MFA/passkey/CAPTCHA/izin Chrome dan OS adalah pekerjaan manual saya.
- Default model yang diminta konfigurasi: **`openai-codex/gpt-6.1-terra:low`**. Model agent yang sedang berjalan dapat berbeda. Jangan menjanjikan model tersedia sebelum ada bukti akun target dan jangan menggantinya diam-diam.
- `models.yml` memakai **`NINE_ROUTER_API_KEY`** dari lingkungan. Saya memasok nilainya sendiri secara lokal. 9router di localhost port **20128** adalah layanan eksternal; repo ini tidak menyertakan layanan atau autentikasinya.

## Eksekusi

1. Jalankan `plan --home` tujuan dan jelaskan konflik/risiko yang nyata. Untuk preview terisolasi boleh memakai direktori staging baru, bukan menyalin state akun sumber.
2. Instal runtime pin pada akun target, periksa PATH agar instalasi lama tidak membayangi, dan catat versi/path aktual.
3. Jalankan `apply --home`, kemudian `verify --home` pada tujuan yang sama. Bedakan keberhasilan hash/berkas dari keberhasilan fitur yang memerlukan autentikasi.
4. Pandu saya menjalankan `omp login openai-codex` atau `/login` secara interaktif. Jangan mengambil token dari mesin asal. Setelah saya menyelesaikannya, periksa model melalui CLI yang didukung. Permintaan model berbayar/berkuota hanya dalam izin saya; laporkan hasil aktual.
5. Pastikan skills payload ditemukan tanpa `--no-skills`. Baca skill sebelum dipakai. Untuk graphify, bedakan plugin lokal `graphify-pi` yang dipulihkan dari runtime Python/executable `graphify` yang perlu dipasang terpisah. Gunakan environment terisolasi dan instruksi skill, bukan scan seluruh home. Paket graphifyy tidak dipin oleh snapshot.
6. Pisahkan browser native OMP dan Chrome DevTools MCP:
   - Native browser: baca `omp-browser` dan `xd://eval/browser`. Gunakan isolated Chromium untuk tugas publik; relay Chrome pribadi hanya dengan izin saya. Jangan diam-diam mengganti relay dengan isolated bila perlu login pribadi.
   - Ekstensi relay perlu saya **Load unpacked** di `chrome://extensions` setelah Developer mode diaktifkan, biasanya dari `~/.omp/browser-relay/extension`. Keberadaan direktori tidak berarti ekstensi sudah aktif. Jangan menimpa aset yang benar hanya untuk setup ulang.
   - MCP menjalankan `npx` dengan `chrome-devtools-mcp@latest --autoConnect`; butuh Node/npm/npx dan koneksi Chrome tersendiri. `@latest` tidak dipin. Mounted tools bukan bukti browser terhubung; baru klaim koneksi setelah `list_pages` berhasil dengan izin saya. Jangan mematikan Chrome atau membuka debugging publik.
   - Probe relay atau MCP yang belum dijalankan harus dilaporkan sebagai belum diuji, bukan sukses. Jangan membaca tab/cookie pribadi untuk membuktikan instalasi.
7. Herdr opsional: skill bukan instalasi binary/session. Gunakan hanya jika saya meminta dan agent berada dalam pane dengan `HERDR_ENV=1`. Jangan kontrol pane/tab saya dari luar Herdr.
8. Jangan menjalankan build/test/lint/formatter repo sebagai bagian pemasangan. Lakukan hanya verifikasi installer/runtime yang diperlukan dan smoke fungsional yang saya izinkan; jangan menggandakan permintaan model atau efek eksternal saat hasil sebelumnya belum jelas.

## Laporan akhir

Berikan ringkasan singkat berbasis bukti:

- Runtime yang terpilih dan hasil paritas berkas (`verify`).
- Konflik dan langkah manual yang belum selesai.
- Status login/model, 9router, graphify, native browser/relay, dan MCP: **terverifikasi / belum diuji / gagal**, masing-masing dengan bukti atau blocker konkret.
- Ingatkan bahwa `update.auto: true` dapat mengubah versi OMP setelah restore dan MCP `@latest` bisa drift. Jangan mengubahnya tanpa persetujuan saya.
- Tegaskan bahwa **paritas berkas tidak sama dengan paritas fungsional terautentikasi**. Jangan menulis “sama persis/semua siap” bila login, model, browser, atau layanan eksternal belum terbukti.
