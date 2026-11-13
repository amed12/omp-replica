# Verifikasi snapshot — 2026-11-13

Dijalankan pada mesin sumber macOS x64, bukan mesin baru:

- `python3 -m unittest discover -s tests -v`: **7 lulus**. Mencakup pemulihan byte-exact/idempotent, konflik tanpa overwrite, plan tanpa mutasi, checksum rusak, symlink escape, path traversal, dan deteksi berkas hilang.
- `bash -n scripts/install-runtime.sh`: lulus.
- `bash scripts/install-runtime.sh`: mendeteksi `OMP 18.20.0 already available`, tidak menginstal ulang. Jalur download/install baru belum dieksekusi.
- CLI `plan`, `apply`, `verify`, lalu `apply` lagi pada temporary home: seluruhnya exit 0. Seluruh **130 berkas** sesuai SHA-256 manifest; **10 skill** terpulihkan. Direktori uji dibersihkan otomatis.
- Dibandingkan langsung dengan sumber: **124 berkas** (117 berkas skill, 5 relay, config.yml, mcp.json) identik. Bridge dan legal notices ditangkap dari distribusi Graphify oleh proses capture.
- Seluruh berkas repo diperiksa untuk nilai key 9router sumber dan marker private key: tidak ditemukan. Ini pemeriksaan terbatas, bukan jaminan semua format rahasia terdeteksi.
- Bun YAML parser menerima models.yml tersanitasi dan referensi `NINE_ROUTER_API_KEY` sesuai.

Tidak dijalankan: fresh install jaringan di mesin/akun baru, login OAuth baru, request model berbayar, koneksi 9router, pengendalian Chrome, pemasangan permission/extension, instalasi Graphify/Playwright baru, ataupun uji lintas-platform. Tidak mengubah konfigurasi OMP aktif, login, tab, atau registry plugin pengguna selama verifikasi.

Bukti ini menunjukkan paritas berkas dan perilaku aman restorer. Paritas fungsional terautentikasi memerlukan gate manual di docs/INSTALL.md pada mesin tujuan.
