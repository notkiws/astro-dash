# DILI ORBIT — konsep game

Versi 8-bit / gaya NES dari DILI ORBIT. Semua batasan diambil dari hardware asli
(Nintendo Entertainment System) supaya terasa otentik, bukan sekadar filter pixel.

## 1. Spesifikasi teknis ala NES

- **Resolusi internal**: 256 x 240 piksel, ditampilkan dengan pembesaran bilangan bulat
  (`image-rendering: pixelated`), tanpa anti-alias dan tanpa sub-piksel.
- **Metatile**: 16 x 16 piksel. Layar menampung **16 x 15 tile** (sama seperti jumlah tile
  per layar di game NES kebanyakan).
- **Kamera**: hanya menggeser horizontal; vertikal dikunci di 0 sehingga komposisi layar
  selalu tetap. Nilai kamera dibulatkan ke bilangan bulat supaya piksel tidak bergetar.
- **Rendering**: sprite dan tile di-pra-render sekali ke offscreen canvas (sprite atlas)
  lalu di-`drawImage` per frame. Tidak ada gradient, tidak ada blur bayangan.
- **Palet**: 22 warna bergaya NES, dipakai lewat nama huruf (mis. `B` = #0058f8,
  `c` = #3cbcfc, `y` = #fce0a8, `Y` = #f8b800, `G` = #00a800, `P` = #d882f8).
  Setiap sprite dibatasi kurang dari 4 warna + transparan, mengikuti batasan hardware.
- **Font**: font bitmap 5 x 7 piksel buatan sendiri (A-Z, 0-9, tanda baca), digambar
  piksel per piksel. Tidak memakai font sistem sama sekali.
- **Overlay CRT** (opsional, tombol `V`): garis scanline 1 px + vignette.

## 2. Karakter: robot astronot 8-bit

Tinggi sprite 16 x 22 piksel, dibagi dua lapis:

- **Badan (16 x 16)**: helm kaca (2 warna: kaca muda + highlight), visor biru `#0058f8`,
  mata 1 px putih + pupil 1 px hitam, senyum 4 px hitam, jubah biru tua di sisi kiri-kanan
  badan, emblem putih di dada.
- **Strip kaki (16 x 6)** dengan 4 pose: `stand`, `run1`, `run2`, `jump`.
  Sepatu putih 4 x 2 piksel, mengayun tiap 2 frame lari.
- Semua frame punya versi cermin otomatis (`flipSprite`) untuk arah hadap kiri.

Animasi lari memakai 2 frame (aturan NES klasik: bergantian tanpa interpolasi),
dan frame `jump` dipakai saat karakter di udara.

## 3. Roster musuh

- **Walker (16 x 13)** — slime alien hijau dengan antena dan mata berkedip. Berjalan
  bolak-balik, berbalik arah sendiri di tepi jurang (deteksi tile kosong di depan).
  Dikalahkan dengan menginjak kepala (+25 orb), menabraknya dari samping = -1 nyawa.
- **Drone (16 x 12)** — piring terbang abu-abu dengan lampu merah, terbang naik-turun
  mengikuti gelombang sinus. Tidak bisa diinjak dari bawah; harus dilompati atau diinjak
  tepat di atasnya.

## 4. Objek & item

- **Orb plasma (8 x 8, 2 frame)**: +10, inti putih dengan tepi biru.
- **Kontainer `B`**: balok logam dengan penguat silang kuning.
- **Kontainer misteri `?`**: dipukul dari bawah → mengeluarkan orb, berubah jadi `u`.
- **Platform energi `-`**: balok cahaya, bisa dilompati dari bawah (one-way).
- **Plasma spike `^`**: duri oranye, -1 nyawa.
- **Portal `G` (16 x 32, 3 frame animasi)**: pintu keluar sektor, +200 orb.

## 5. Struktur level

Tiga sektor, tiap sektor punya palet dan latar langit sendiri:

- **SECTOR 1-1 ORBITAL STATION** (212 tile) — langit biru tua, planet bercincin biru.
- **SECTOR 2-1 ASTEROID BELT** (232 tile) — nuansa coklat, planet emas, tanah batu asteroid.
- **SECTOR 3-1 ALIEN MOTHERSHIP** (252 tile) — nuansa ungu, langit kapal alien, langit-langit
  kapal menutup bagian atas layar.

Panjang tiap sektor ±13 layar. Tiap sektor dibuka dengan kartu hitam
("SECTOR 1-1 / ORBITAL STATION") selama ±1,7 detik, seperti layar intro NES.

Aturan geometri yang **divalidasi otomatis saat build**:

- tidak boleh ada tile padat mengambang di baris 12 — kepala karakter (19 px, berdiri di
  baris 14) mencapai baris 12, jadi balok di sana akan jadi dinding tak terlihat;
- semua jurang harus lebar 2 tile — cukup terlihat, cukup adil, dan tidak memerangkap
  pemain seperti jurang 1 tile yang bersebelahan dengan dinding.

## 6. HUD & layar (gaya NES)

- **HUD 2 baris** di atas, latar hitam penuh: `ORB 000000` kiri atas, `SECTOR 1-1` kanan atas,
  deretan 3 hati piksel + label `LIVES` di baris kedua (hati di kartu sektor dihitung tepat di tengah layar 256 px).
- **Kartu sektor**, **PAUSED**, **SECTOR CLEAR**, **NO LIVES LEFT**, **GAME OVER**,
  **MISSION COMPLETE** — semua digambar dengan font bitmap, tanpa transparansi.
- Judul: `DILI / ORBIT` (dua baris logo), prompt `PRESS SPACE` berkedip.

## 7. Audio chiptune

Ditiru dengan WebAudio, 4 kanal virtual seperti 2A03 NES:

- **Pulse 1** — melodi utama (gelombang kotak), 64 langkah loop.
- **Pulse 2** — harmonisasi (dipakai untuk arpeggio SFX).
- **Triangle** — bass berjalan.
- **Noise** — drum: kick (lowpass 320 Hz), snare, hi-hat (6000 Hz).

Tempo 138 BPM, resolusi 1/16 not, penjadwalan look-ahead 250 ms supaya tidak goyang.
Musik hanya berjalan saat bermain (mulai saat sektor dimulai, berhenti saat jeda/clear/game over).
SFX memakai pola arpeggio cepat: lompat `E5→A5`, ambil orb `B5→E6`, kena musuh `G4→E4→C4`,
selesai sektor `C5-E5-G5-C6-G5-C6`, game over `C5-G4-E4-C4-G3`.

## 8. Kontrol & rasa permainan

Fisika versi 8-bit memakai skala tile 16 px (setengah dari versi 32-bit), jadi rasanya
identik dengan versi sebelumnya:

- Akselerasi 0.42 px/frame², kecepatan lari 2.35, sprint 3.3, gravitasi 0.31,
  lompatan -6.1 (tinggi ±3.75 tile, jarak ±5.6 tile saat lari).
- **Coyote time** 7 frame dan **jump buffer** 7 frame, lompat variabel (lepas tombol
  memotong lompatan).
- Kena musuh: **knockback** menjauh + 110 frame kebal (1.8 detik).
- Jatuh ke jurang: muncul lagi di **checkpoint** (titik tanah aman terakhir), bukan di
  awal sektor.

Kontrol: `A/D` atau panah kiri-kanan jalan, `Space`/`W`/`↑` lompat, `Shift` lari cepat,
`P` jeda, `R` ulang sektor, `M` bisu, `V` overlay CRT. Di HP tombol sentuh muncul otomatis.

## 9. Cara mengubah

- `8bit/game8_template.html` — seluruh mesin: palet `C`, font `FONT`, sprite `RAW`/`HERO_BODY`,
  tile `buildTiles()`, musik `SONG`.
- `8bit/build8.py` — menyusun level (memakai generator di `../build.py` yang sama),
  memvalidasi geometri, lalu menulis `dili-orbit.html`.

```
python3 build8.py     # hasil: dili-orbit.html (satu file, bisa dibuka langsung)
```

## 10. Status verifikasi

Autopilot (bot yang dipasang di dalam halaman, mode ghost: nyawa terus diisi) menembus
ketiga sektor sampai layar **MISSION COMPLETE** — sektor 1 skor 445, sektor 2 skor 550,
sektor 3 skor 590. Tidak ada error JavaScript dan tidak ada sprite dengan warna/panjang
baris yang salah (keduanya diperiksa otomatis oleh `window.__artErrors`).

## 11. Bahasa antarmuka

Seluruh teks di dalam game (judul, HUD, kartu sektor, jeda, clear, game over, misi selesai,
nama sektor) sudah **bahasa Inggris penuh** — sama seperti versi 32-bit. Dokumen ini dan
README tetap berbahasa Indonesia untuk keperluan penjelasan.

Penjaga otomatis: `drawText` mencatat setiap string yang keluar dari layar 256 px ke
`window.__textOverflow`, jadi penambahan teks baru bisa langsung diperiksa.
## 12. Nama pemain & papan skor TOP PILOTS

- Layar judul **tidak lagi** memuat frasa "8-BIT EDITION"; ruang itu dipakai untuk papan skor.
- Alur: judul -> `SPACE` -> layar **ENTER YOUR NAME** -> `ENTER` -> sektor mulai.
- Nama: `A-Z`/`0-9`, maksimum 8 karakter, `Backspace` menghapus.
- **Kembali**: `Esc` di keyboard mengembalikan ke layar judul; di keyboard sentuh ada tombol
  `ESC` (sebelah `DEL`). Ketukan di luar tombol tidak melakukan apa-apa (dulu ketukan di luar
  tombol = mulai, sekarang harus lewat `OK` supaya tidak salah mulai). Di perangkat sentuh muncul
  keyboard huruf 4 baris di dalam canvas (38 tombol: A-Z, 0-9, `<` hapus, `OK`) yang dikenali
  lewat hit-test `pointerdown`, jadi tetap bisa main di HP tanpa keyboard fisik.
- Nama terakhir disimpan (`localStorage`) dan otomatis terisi pada permainan berikutnya;
  kalau kosong dipakai `PILOT`.
- Skor dikirim **sekali** per permainan saat layar GAME OVER / MISSION COMPLETE muncul
  (`finishRun()` dijaga `game.submitted`), lalu diurutkan menurun dan dipotong 10 besar.
- **Nama identik = pemain yang sama**: `dedupeScores()` menyimpan hanya skor tertinggi per nama,
  baik saat dibaca dari penyimpanan maupun saat skor baru dikirim. Skor yang lebih rendah
  (atau sama) tidak menambah baris dan tidak menurunkan skor lama; layar akhir membedakan
  `NEW HIGH SCORE` (memperbaiki rekor pribadi) dari `YOUR BEST` (rekor lama masih bertahan).
- Papan skor tampil di layar judul (10 baris, peringkat 1 kuning, 2-3 biru, sisanya abu-abu),
  dan peringkat pemain ditampilkan di layar akhir (`NEW HIGH SCORE   RANK n`).
- Penyimpanan dibungkus `try/catch`: kalau browser melarang `localStorage` (mis. file:// di
  beberapa browser), game tetap jalan dan papan skor hanya tidak ikut tersimpan.
- Pintu debug: `window.__astro.scores` dan `window.__astro.pilotName` untuk verifikasi.
## 13. Perbaikan layar judul

- Baris `1 PLAYER` dihapus (sisa dari gaya layar "1 PLAYER / 2 PLAYERS" NES); blok kontrol
  digeser turun sedikit supaya jaraknya seimbang.
- **Hanya `Space` yang memindahkan halaman** (judul -> nama, kartu sektor -> main,
  clear/dead/game over/mission complete -> lanjut). Sebelumnya cabang judul tidak menyaring
  tombol, jadi `Shift`/`A`/`D`/`W`/panah ikut melompatkan halaman, padahal layarnya menulis
  `PRESS SPACE`. Sekarang penyaring memakai `e.code === 'Space'`.
- Di perangkat sentuh, ketukan layar dan tombol `▲` tetap berfungsi (layar judul menampilkan
  `TAP TO START`, desktop menampilkan `PRESS SPACE`). Di desktop, klik mouse tidak lagi
  memindahkan halaman.
## 14. Tata letak layar judul & halaman HIGH SCORES

Masalah: menaruh tabel 10 baris di tengah layar judul mendorong logo+karakter ke atas dan
instruksi tombol ke bawah. Konvensi arcade: di layar judul hanya **skor tertinggi** (satu baris
`HI`), tabel lengkap ada di halaman terpisah atau muncul setelah permainan selesai.

- Layar judul sekarang: logo (y 20/46) > karakter (y 80) > `HI <nama> <skor>` (y 114) >
  tiga baris instruksi (140/152/164) > `H  HIGH SCORES` (186) > prompt berkedip (210).
  Margin atas 20 px, bawah 23 px (layar 240 px) - seimbang.
- Halaman `HIGH SCORES` (state 9): judul y 22, 10 baris dari y 52 dengan jarak 10 px,
  prompt kembali di y 200/214. Kosong: `NO SCORES YET / PLAY TO SET ONE`.
- Tombol `H` membuka halaman ini dari judul, GAME OVER, dan MISSION COMPLETE. Saat ditutup
  (`Space` / `Esc` / `H`), pemain kembali ke layar asalnya lewat `scoresFrom`.
- Sentuh: ketukan pada baris hint (y 178-198) membuka halaman skor, ketukan lain di layar judul
  lanjut ke layar nama; di halaman skor, ketukan = kembali.
## 15. Penyederhanaan layar judul & halaman skor

- Layar judul **tanpa papan skor sama sekali** (termasuk baris `HI`): logo (y 24/50) > karakter
  (y 84) > prompt berkedip (y 134) > empat baris instruksi (164/176/188/200). Prompt `PRESS SPACE`
  sekarang **di atas** instruksi tombol, dan baris `H HIGH SCORES` masuk ke blok instruksi yang
  sama dengan warna abu-abu yang sama (dulu terpisah dan berwarna biru).
- Halaman `HIGH SCORES` hanya menampilkan **satu** instruksi kembali: `ESC = BACK` (desktop) atau
  `TAP TO GO BACK` (sentuh). `Space` masih berfungsi sebagai jalan pintas kembali, tetapi tidak
  lagi ditulis di layar supaya tidak ada instruksi ganda.
- Band ketuk untuk membuka halaman skor mengikuti posisi baris `H` (y 194-214 pada 8-bit,
  y 476-504 pada versi 32 px).
## 16. Tombol keluar dari halaman skor: kenapa bukan Esc

Pengguna melaporkan: menekan `Esc` di halaman HIGH SCORES memang kembali ke layar judul, tetapi
layar ikut keluar dari mode fullscreen ("menjadi minimize").

Hasil uji dengan input asli (`Input.dispatchKeyEvent` lewat CDP, bukan event sintetis):

- `F` asli saat di fullscreen: halaman menerima tombolnya dan bisa keluar sendiri dengan
  `Esc` (default browser, tidak bisa dibatalkan `preventDefault`). Bahkan handler halaman
  **tidak menerima keydown** untuk `Esc` saat fullscreen (terhitung 0 kali).
- Artinya `Esc` tidak boleh menjadi tombol "back" yang ditulis di layar untuk game yang bisa
  dimainkan fullscreen.

Perbaikan:

- Halaman HIGH SCORES sekarang menulis **`BACKSPACE = BACK`** (juga menerima `H`, `Space`, `Esc`
  sebagai alias tanpa ditulis). `Backspace` aman: browser modern tidak lagi memakainya untuk
  navigasi mundur.
- Ditambahkan tombol `F` untuk fullscreen on/off, supaya pemain yang terlempar keluar dari
  fullscreen bisa kembali dengan satu tombol (tidak ditulis di layar, hanya di README).
- Handler yang menangani `Esc`/`Backspace` sekarang memanggil `preventDefault()` +
  `stopPropagation()` supaya browser tidak ikut bereaksi (sebatas yang diizinkan browser).
