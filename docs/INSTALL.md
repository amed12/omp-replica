# Runbook replikasi OMP untuk agent

## Sasaran dan batas keberhasilan

Snapshot ini menyalin konfigurasi dan aset non-rahasia setup sumber macOS x64: **OMP 18.20.0**, **Bun 1.4.4**, skills, plugin graphify, ekstensi relay Chrome, konfigurasi MCP, dan deklarasi model yang sudah disanitasi. Daftar berkas dan hash otoritatif ada di `manifest.json`.

**Paritas berkas bukan paritas fungsional terautentikasi.** `verify` memeriksa berkas snapshot; hasilnya tidak membuktikan login provider, ketersediaan model, layanan 9router, koneksi browser, izin OS, atau kesetaraan perilaku semua model. Jangan melaporkan semuanya siap hanya karena penyalinan berhasil.

Tidak disertakan: kredensial/API key, OAuth, auth vault, session, database, riwayat, private memory, cache pribadi, profil Chrome, cookie, local storage, atau login situs. Jangan mengambilnya dari mesin sumber untuk melengkapi instalasi.

## 1. Siapkan target dan tinjau rencana

Gunakan checkout repo yang dipercaya, terminal pengguna target, `python3`, akses jaringan untuk instalasi runtime, dan ruang disk yang cukup. Contoh berikut dijalankan dari root repo:

```sh
python3 scripts/replica.py plan --home "$HOME"
```

Baca rencana dan konflik sebelum menulis. `--home` menentukan akar tujuan payload, bukan otomatis mengalihkan instalasi global Bun, konfigurasi shell, atau proses OMP. Untuk staging tanpa menyentuh konfigurasi aktif:

```sh
python3 scripts/replica.py plan --home /tmp/omp-replica-home
python3 scripts/replica.py apply --home /tmp/omp-replica-home
python3 scripts/replica.py verify --home /tmp/omp-replica-home
```

Staging tidak membuktikan OMP memakai home tersebut. Jalankan OMP fungsional di akun target sebenarnya. Opsi `--profile` mengisolasi state OMP tetapi bukan pengganti `--home` installer; profile terpisah tidak otomatis memuat konfigurasi agent default hasil restore.

## 2. Instal runtime yang dipin

Tinjau skrip, lalu jalankan pada akun target:

```sh
bash scripts/install-runtime.sh
```

Skrip menargetkan Bun **1.4.4** dan paket `@oh-my-pi/pi-coding-agent` **18.20.0**. Buka terminal baru atau sesuaikan PATH mengikuti keluaran installer. Periksa runtime yang benar-benar terpilih, terutama bila ada asdf/Homebrew/instalasi lama:

```sh
command -v bun
command -v omp
bun --version
omp --help
```

Header bantuan harus menunjukkan `omp v18.20.0`; versi Bun harus `1.4.4`. Jangan menjalankan `omp update` sebagai bagian restore yang dipin. Platform sumber adalah macOS x64; kesetaraan native dependency di platform lain tidak dijamin.

## 3. Pulihkan berkas tanpa menimpa konflik

```sh
python3 scripts/replica.py apply --home "$HOME"
python3 scripts/replica.py verify --home "$HOME"
```

Installer memvalidasi hash payload terhadap manifest dan tidak menimpa berkas tujuan yang isinya berbeda. Berkas identik dapat dipertahankan. Jika konflik ditemukan, laporkan path, minta pengguna memutuskan backup/merge/penggantian secara manual, lalu ulangi `plan`, `apply`, dan `verify`. Jangan menghapus konfigurasi pengguna atau menambahkan mode paksa sendiri. Perubahan payload tanpa pembaruan manifest yang sah harus dianggap kegagalan integritas, bukan diakali dengan melewati verifikasi.

`apply` memulihkan aset yang tercantum saja; tidak memasang otomatis semua program eksternal yang dipanggil konfigurasi.

## 4. Login dan model

Default konfigurasi yang direplikasi adalah **`openai-codex/gpt-6.1-terra:low`**. Ini nilai konfigurasi, bukan bukti model tersedia pada akun target. Model yang sedang menjalankan agent saat ini dapat berbeda karena override runtime/session/provider.

Pengguna menjalankan login interaktif di terminalnya sendiri:

```sh
omp login openai-codex
```

Alternatif: `omp login` untuk memilih provider atau `/login` dari TUI. Pengguna menyelesaikan OAuth, MFA, passkey, dan dialog izin sendiri. Jangan memakai ekspor/impor autentikasi mesin sumber, membaca token dengan `omp token`, atau memasukkan rahasia ke prompt/log/repo/argumen CLI.

`models.yml` yang disanitasi merujuk **`NINE_ROUTER_API_KEY`**, bukan nilai kunci asli. Pengguna memasok variabel lingkungan itu melalui pengelola rahasia/terminal lokal tanpa membagikannya ke agent. Variabel harus diwarisi proses OMP; jangan menaruh nilai nyata di repo atau perintah yang tercatat di shell history.

**9router adalah layanan eksternal di localhost port 20128**, bukan komponen yang disalin atau dijalankan repo ini. Pengguna harus menyediakan layanan dan autentikasinya sendiri bila ingin memakai provider tersebut. Deklarasi model tidak membuktikan endpoint hidup atau alias model diterima.

Setelah login, gunakan `omp models --help` lalu perintah daftar/pencarian yang didukung untuk memeriksa model akun. Jika diminta pengguna, lakukan satu permintaan kecil dengan model yang dipilih, misalnya:

```sh
omp --model openai-codex/gpt-6.1-terra --thinking low --no-session -p "Balas tepat: OK"
```

Ini mengirim permintaan berbayar/berkuota; lakukan hanya dalam izin pengguna. Laporkan respons aktual atau kegagalan provider. Jangan mengganti model default diam-diam jika model tidak tersedia.

## 5. Skills dan graphify

Payload memulihkan skills ke lokasi yang tercantum dalam manifest, termasuk `captain`, `feature-sprint`, `graphify`, `herdr`, `omp-browser`, `playwright-cli`, `reverse-engineer-anything`, `systematic-debugging`, `test-driven-development`, dan `vercel-react-best-practices`. Baca `SKILL.md` yang cocok sebelum menggunakannya. Jangan mulai OMP dengan `--no-skills` jika ingin discovery normal. Skill adalah instruksi, bukan izin tambahan atau pemasang otomatis semua dependency.

Bridge lokal **`graphify-pi`** disalin ke `~/.omp/plugins/vendor/graphify-pi`, bukan environment Python sumber. Setelah apply, daftarkan secara eksplisit (menulis registry plugin pengguna):

```sh
omp plugin link "$HOME/.omp/plugins/vendor/graphify-pi"
omp plugin list
omp plugin doctor
```

Runtime sumber adalah **graphifyy 0.9.102**, Python **3.12.13**. Gunakan environment terisolasi: `uv tool install --python 3.12.13 graphifyy==0.9.102` bila uv tersedia, atau buat virtualenv dengan Python versi tersebut lalu jalankan `python -m pip install graphifyy==0.9.102` di dalamnya. Pastikan direktori executable absolut ada di PATH proses OMP. Jangan menyalin shebang/virtualenv mesin sumber. Lihat `docs/ASSETS.md` untuk provenance.

Untuk code-only corpus, ekstraksi AST graphify tidak memerlukan API key. Kunci Gemini opsional untuk ekstraksi semantik; jangan meminta OpenAI/Anthropic key atas nama graphify. Jangan membangun graph seluruh home untuk uji instalasi. Jika pengguna meminta uji, gunakan repo kecil yang disetujui, ikuti skill, dan laporkan output sebenarnya.

Runtime skill Playwright sumber: **@playwright/cli 0.1.23**. Pasang dengan `npm install --global @playwright/cli@0.1.23`, lalu periksa `playwright-cli --help`; dependency browser dan izin OS tetap harus dipenuhi sesuai skill. Native browser OMP tidak memerlukan CLI ini.

## 6. Browser: dua jalur berbeda

### Native OMP browser

Baca skill `omp-browser` dan `xd://eval/browser` sebelum mengoperasikan browser. API browser native berjalan melalui `eval`; keberadaan MCP bukan prasyaratnya. `app: "chromium"` memakai browser terisolasi dan tidak membawa login Chrome pribadi. `app: "relay"` mengakses Chrome pengguna melalui relay dan hanya boleh digunakan setelah izin eksplisit.

Ekstensi relay dipulihkan ke lokasi manifest, biasanya `~/.omp/browser-relay/extension`. Pengguna harus melakukan langkah manual di Chrome:

1. Buka `chrome://extensions`.
2. Aktifkan Developer mode.
3. Pilih **Load unpacked** dan direktori ekstensi tersebut; bila sudah terpasang, **Reload** ekstensi yang benar.
4. Tanggapi sendiri dialog izin Chrome.

Bila aset ekstensi hilang, `omp browser-relay install` menulis ekstensi dan petunjuk lokasi. Jangan menjalankannya sekadar untuk menimpa snapshot yang sudah valid. OMP memulai relay lokal ketika diperlukan. Probe read-only yang tidak membaca tab/cookie:

```sh
curl --max-time 3 -sS http://127.0.0.1:9224/json/version
```

`relay extension is not connected` berarti server dapat dicapai tetapi ekstensi belum tersambung; endpoint tidak terjangkau adalah masalah berbeda. Probe ini saja bukan bukti kontrol tab berhasil. Jangan membuka port debugging publik, mematikan Chrome pengguna, atau mengubah default relay diam-diam. Login situs, CAPTCHA, MFA, dan izin OS tetap manual.

### Chrome DevTools MCP

`mcp.json` menjalankan `npx -y chrome-devtools-mcp@latest --autoConnect --no-usage-statistics --no-performance-crux`. Ini **koneksi terpisah** dari native relay. Sumber menggunakan Node.js **22.17.0**, npm **10.9.2**; pasang versi itu melalui pengelola runtime pilihan pengguna agar mendekati sumber. Pastikan `npx` ada di PATH. Bun saja tidak menjamin `npx` tersedia. Peluncuran awal dapat mengunduh paket dari jaringan.

`@latest` adalah referensi tidak dipin: yang direplikasi ialah konfigurasi snapshot, bukan versi paket MCP yang dapat direproduksi. Untuk mengunci versi nantinya, pengguna harus menyetujui perubahan konfigurasi dan manifest; jangan menyatakan snapshot ini sudah menguncinya.

`--autoConnect` memerlukan Chrome yang kompatibel dan pengaturan/izin koneksi yang sesuai versi Chrome. Ikuti dokumentasi/petunjuk Chrome DevTools MCP dan Chrome yang terpasang; pengguna mengaktifkan serta menyetujui akses secara manual. Tidak perlu mengaktifkan debugging Chrome hanya untuk memakai native relay.

Mount server belum membuktikan akses browser: panggilan **`list_pages` harus berhasil** sebelum mengklaim koneksi MCP berfungsi. Kegagalan `DevToolsActivePort` menunjukkan koneksi Chrome MCP tidak tersedia, bukan bukti native browser OMP rusak. Jangan mengarang keberhasilan koneksi atau melakukan inspeksi tab pribadi tanpa izin.

## 7. Herdr opsional

Skill `herdr`/`captain` ikut dipulihkan, tetapi binary, session, layout pane, dan akses mesin Herdr tidak ikut. OMP dapat berjalan tanpa Herdr. Bila pengguna memang meminta Herdr, pasang melalui distribusi resmi yang sesuai target, masuk ke pane Herdr, dan pastikan `HERDR_ENV=1` sebelum mengontrol session. Pelajari sintaks dari `herdr --help`; jangan menjalankan kontrol dari luar Herdr atau mengambil alih pane/tab pengguna. Tidak ada versi runtime Herdr yang dipin oleh snapshot ini.

## 8. Catat verifikasi dan drift

Laporkan terpisah:

- Runtime: path executable dan versi yang benar-benar diamati.
- Berkas: hasil `verify`, konflik, dan hash yang gagal.
- Autentikasi/model: login manual selesai atau belum; model yang benar-benar diuji, jika ada.
- Dependency eksternal: graphify, Node/npx, dan 9router tersedia atau belum.
- Browser: native isolated/relay/MCP mana yang benar-benar diuji, izin pengguna, dan hasil aktual.
- Langkah manual yang masih menunggu pengguna, tanpa mengklaim paritas penuh.

Snapshot mempertahankan **`update.auto: true`** sehingga OMP dapat drift setelah instalasi. Jika pengguna membutuhkan reproduksibilitas jangka panjang, minta persetujuan untuk menonaktifkan auto-update melalui antarmuka konfigurasi OMP dan catat bahwa ini deviasi dari snapshot. `chrome-devtools-mcp@latest`, dependency eksternal, layanan/provider, serta model akun juga dapat berubah. Setelah pengguna mengubah konfigurasi atau OMP menulis ulang berkas, `verify` boleh menunjukkan perbedaan; jangan otomatis menimpa perubahan itu.
