# ASTRO DASH — platformer luar angkasa

Game platformer bergaya Super Mario Bros, tapi latarnya ruang angkasa: stasiun orbit,
sabuk asteroid, dan kapal induk alien. Pemain memakai karakter robot astronot biru
(helm kaca, jubah, sepatu putih, membawa ponsel).

File utama: **index.html** — satu file mandiri, tanpa internet, tanpa install.
Buka langsung di browser (double click) atau:

    python3 -m http.server 8000     # lalu buka http://localhost:8000

## Kontrol

- `←` `→` atau `A` `D` — jalan
- `Space` / `W` / `↑` — lompat (tahan lebih lama = lompat lebih tinggi)
- `Shift` — lari cepat
- `P` atau `Esc` — jeda, `R` — ulang level, `M` — matikan suara, `F` — fullscreen on/off
- Di layar judul / kartu sektor / clear / game over: hanya `Space` yang melanjutkan
  (tombol lain seperti `Shift`, `W`, panah tidak lagi ikut melompatkan halaman).
  Di HP tetap bisa lewat ketukan layar dan tombol `▲`.
- Di layar nama: ketik `A-Z` / `0-9` (maks 8 karakter), `Enter` = mulai, `Backspace` = hapus,
  `Esc` = kembali ke layar judul. Di HP muncul keyboard huruf di layar: ketuk huruf,
  `ESC` = kembali ke judul, `DEL` = hapus, `OK` = mulai.
- Di HP: tombol sentuh otomatis muncul (kiri, kanan, lompat)

## Aturan main

- Orb plasma = +10, menginjak alien = +25, menyentuh portal = +200 dan lanjut sektor.
- 3 nyawa per sektor. Kena alien/plasma = -1 nyawa, jatuh ke jurang = -1 nyawa.
- Kalau nyawa habis, game over dan kembali ke menu.
- Kalau jatuh ke jurang, kamu muncul lagi di titik aman terakhir (checkpoint otomatis),
  bukan di awal level.
- Kena musuh akan membuat karakter terdorong mundur supaya tidak terkena berulang.
- Ada 3 sektor; setelah sektor 3 selesai muncul layar kemenangan dan skor akhir.
- Sebelum mulai pemain mengisi nama (tersimpan sebagai nama terakhir), dan skor akhir
  masuk ke papan **10 besar** yang bisa dibuka dari layar judul atau layar akhir dengan
  tombol `H` (di HP: ketuk baris `H HIGH SCORES`). Keluar dari halaman itu: `Backspace`
  (yang tertulis di layar). `Space` / `Esc` / `H` juga berfungsi tapi tidak ditulis, karena
  `Esc` dipakai browser untuk keluar dari mode fullscreen dan tidak bisa dicegat halaman. Nama yang sama dianggap pemain yang
  sama: yang disimpan hanya skor tertingginya (skor lebih rendah tidak menambah baris baru). Papan skor disimpan di browser
  (`localStorage`), jadi tetap ada walau game ditutup — tapi terpisah per browser/perangkat.

## Kalau mau membangun ulang / mengubah level

Level dibuat oleh generator supaya geometrinya konsisten:

- `game_template.html` — seluruh kode game (fisika, karakter, latar, level kosong `/*%%LEVELS%%*/`)
- `build.py` — menyusun 3 level dari kode Python lalu menulis `index.html`

    python3 build.py        # hasilnya index.html

Arti karakter di peta level:

- `#` pelat logam stasiun, `R` batu asteroid, `-` platform energi (bisa dilompati dari bawah)
- `B` kontainer, `?` kontainer misteri (bisa dipukul dari bawah)
- `o` orb, `e` alien jalan, `f` drone terbang, `^` plasma (berbahaya)
- `P` titik awal, `G` portal keluar

Contoh menambah orb di level 1: edit `level1()` di `build.py`, tambah
`g.row_of(20, 24, 12)`, lalu jalankan `python3 build.py`.

Catatan desain yang sudah divalidasi otomatis oleh `build.py`:
tidak boleh ada balok padat yang mengambang di baris 12 (kepala karakter bisa
menabraknya), dan setiap lubang/jurang harus lebar 2 petak supaya jelas terlihat
dan adil untuk dilompati.

## Folder preview/

- `astro_dash_gameplay.mp4` — rekaman gameplay singkat (sektor 1)
- `title.png`, `sector3.png`, `hero_sheet.png`, `lv1_play.png`, `lv2_play.png`, `lv3_play.png`
