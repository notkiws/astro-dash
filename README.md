# DILI ORBIT — platformer luar angkasa gaya NES

Game platformer satu file (HTML+canvas), gaya **8-bit NES**: resolusi internal **256 x 240**,
tile 16 px, palet NES, sprite pixel art, font bitmap 5x7, dan musik chiptune. Tanpa internet,
tanpa install, tanpa server — buka `8bit/dili-orbit.html` di browser.

Karakter: robot astronot biru (helm kaca, jubah, sepatu putih). Latar: tiga sektor luar angkasa —
stasiun orbit, sabuk asteroid, kapal induk alien.

- Live: <https://diliorbit.netlify.app/>
- Repo: <https://github.com/notkiws/dili-orbit>

## Kontrol

- `←` `→` atau `A` `D` — jalan
- `Space` / `W` / `↑` — lompat (tahan lebih lama = lompat lebih tinggi: ketuk ~3,5 petak, tahan ~4,3 petak)
- `Shift` — lari cepat
- `P` atau `Esc` — jeda, `R` — ulang level, `M` — matikan suara, `V` — efek CRT, `F` — fullscreen on/off
- `H` — buka papan skor dari layar judul / game over / misi selesai (keluar: `Backspace`)
- Di HP: tombol sentuh otomatis muncul (kiri, kanan, lompat) + keyboard huruf di layar untuk isi nama

## Aturan main

- Orb plasma +10, menginjak alien +25, portal +200 dan lanjut sektor. Total 126 orb.
- 3 nyawa per sektor. Kena alien/plasma = -1 nyawa, jatuh ke jurang = -1 nyawa.
- Jatuh ke jurang: muncul lagi di checkpoint terakhir, bukan di awal level.
- 3 sektor; setelah sektor 3 muncul layar kemenangan dan skor akhir.

## Nama pemain & papan skor

- Sebelum mulai pemain mengetik nama (A-Z, 0-9, maks 8 karakter). Nama terakhir diingat.
- Skor akhir masuk papan **10 besar**. Nama yang sama dianggap pemain yang sama: yang disimpan
  hanya skor tertingginya.
- Papan skor disimpan di browser (`localStorage`) — per perangkat, bukan server.

### Reset papan skor

Key penyimpanan: `astroDash8.scores.v2` (+ `astroDash8.pilot.v2` untuk nama terakhir).
Untuk mereset saat rilis baru, naikkan versinya (mis. `v2` -> `v3`); key lama otomatis dihapus
saat game dibuka.

## Struktur & build

    8bit/game8_template.html   template game (semua kode; level disuntik saat build)
    8bit/build8.py             build: validasi geometri + jangkauan, lalu tulis HTML
    8bit/levels.py             generator level 3 sektor + validasi fisika
    8bit/dili-orbit.html  hasil build (file yang dimainkan)
    8bit/KONSEP-8BIT.md        dokumen konsep 8-bit
    make_site.py               menyusun folder `dist/` untuk hosting

    cd 8bit && python3 build8.py      # tulis ulang dili-orbit.html
    python3 make_site.py              # susun dist/ (index.html + gambar share)

Setiap build **gagal** kalau ada platform atau orb yang tidak terjangkau busur lompatan, jadi
level tidak bisa diam-diam punya tempat yang mustahil dinaiki.

### Deploy ulang (Netlify site `diliorbit`)

    cd 8bit && python3 build8.py && cd .. && python3 make_site.py
    netlify deploy --prod --dir=dist --site diliorbit

Alternatif otomatis: di Netlify -> "Import an existing project" -> GitHub -> `notkiws/dili-orbit`
(publish dir `dist/` sudah diatur di `netlify.toml`, tiap push langsung ter-deploy).
