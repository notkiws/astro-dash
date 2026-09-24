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
- `O` — menu OPTIONS (pilih kecepatan/pace)
- Setelah game over / misi selesai: `Space` main lagi dengan nama yang sama, `N` ganti nama, `Backspace` ke layar judul
- Di HP: baris-baris menu itu bisa langsung ditap
- Di HP: tombol sentuh otomatis muncul (kiri, kanan, lompat) + keyboard huruf di layar untuk isi nama

## Aturan main

- Orb plasma +10, menginjak alien +25, portal +200 dan lanjut sektor. Total 126 orb.
- 3 nyawa per sektor. Kena alien/plasma = -1 nyawa, jatuh ke jurang = -1 nyawa.
- Jatuh ke jurang: muncul lagi di checkpoint terakhir, bukan di awal level.
- 3 sektor; setelah sektor 3 muncul layar kemenangan dan skor akhir.

## Kecepatan (pace)

Menu `OPTIONS` (tombol `O` di layar judul, atau `←`/`→` setelah masuk) punya tiga pilihan:
**SLOW 0,90x**, **NORMAL 1,00x**, **FAST 1,20x**. Yang berubah hanya kecepatan horizontal
(jalan dan lari), jadi **tinggi lompatan tetap sama** di semua pilihan dan tidak ada platform
yang jadi mustahil dinaiki karena tingginya.

Kenapa SLOW berhenti di 0,90x dan bukan lebih rendah? Karena diukur, bukan diperkirakan:

- `build8.py` menjalankan ulang pengecekan jangkauan untuk **setiap** pace; kalau ada satu saja
  platform atau orb yang tidak terjangkau, build gagal.
- Hasil pengukuran: 0,70x dan 0,75x menyisakan 10 tempat mustahil, 0,80x dan 0,85x menyisakan 9.
  Yang paling ketat: platform di sektor 1 kolom 100–103 baris 8 dan sektor 3 kolom 84–87 baris 9.
- 0,90x aman (termasuk margin 5%), dan FAST 1,20x juga aman.
- Diuji juga di dalam game: lompatan tersulit itu dicoba langsung di ketiga pace dan berhasil
  mendarat di platform yang sama (kaki di y=128) di SLOW, NORMAL, dan FAST.

Kalau suatu saat ingin pace yang lebih lambat lagi (misalnya 0,75x), yang perlu diubah bukan
kodenya melainkan dua platform tersebut supaya jaraknya lebih ramah.

## Papan skor bersama (global)

Papan skor **bukan** lagi per perangkat. Skor dikirim ke fungsi milik situs sendiri
(`netlify/functions/scores.mjs`, disimpan di Netlify Blobs), jadi semua pemain melihat papan
yang sama. Aturannya sama seperti sebelumnya: satu baris per nama, yang disimpan hanya skor
tertingginya.

- `GET /api/scores` — 10 besar; `POST /api/scores` — kirim skor
- Nama dipaksa A-Z0-9 maksimal 8 karakter, skor dibatasi rentang wajar, jadi papan tidak bisa
  diisi angka ngawur
- Yang disimpan hanya nama tampilan, skor, dan nomor sektor. Tanpa akun, tanpa wallet, tanpa data
  pribadi (sesuai aturan jam)
- Kalau server tidak terjangkau (misalnya file dibuka langsung tanpa server), game tetap jalan
  dan memakai papan di perangkat itu, dengan keterangan `THIS DEVICE ONLY` di halaman skor

### Reset papan skor

Papan bersama ada di satu blob `board`. Untuk mengosongkannya, ganti nama key di
`netlify/functions/scores.mjs` (mis. `board` -> `board2`) lalu deploy ulang, atau hapus blob-nya
lewat dashboard Netlify. Papan lokal per perangkat direset dengan menaikkan `diliOrbit.scores.v2`.

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

Sejak ada papan skor bersama, deploy harus menyertakan fungsi, jadi pakai `--build`
(atau hubungkan repo GitHub supaya tiap push otomatis ter-deploy):

    netlify deploy --build --prod --site diliorbit

Alternatif otomatis: di Netlify -> "Import an existing project" -> GitHub -> `notkiws/dili-orbit`
(publish dir `dist/` sudah diatur di `netlify.toml`, tiap push langsung ter-deploy).
