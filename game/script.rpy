## ============================================================
##  VISUAL NOVEL: "Yang Hemat Ya" - Mahasiswa Perantau Ilkomp UPI
##  Taruh file ini di folder  game/  (ganti script.rpy bawaan).
##
##  Struktur aset yang dipakai:
##    game/images/Background/*.jpg
##    game/images/Karakter/Az|Bz|Cz|Dz/*.png
##    game/audio/bad_end.mp3, neutral_end.mp3, good_end.mp3
## ============================================================

## ------------------------------------------------------------
##  PENGATURAN TAMPILAN (ubah di sini kalau ukuran tidak pas)
## ------------------------------------------------------------
init python:
    SPRITE_ZOOM = 0.55      # perkecil/perbesar semua sprite karakter
    SPR_DIR = "images/Karakter/"

## ------------------------------------------------------------
##  LATAR BELAKANG
##  (gambar di-scale ke ukuran layar game)
## ------------------------------------------------------------
image bg fmipa     = im.Scale("images/Background/ruang-fpmipa.jpg",      config.screen_width, config.screen_height)
image bg space52   = im.Scale("images/Background/space-52.jpg",          config.screen_width, config.screen_height)
image bg nongkrong = im.Scale("images/Background/tempat-nongkrong.jpg",  config.screen_width, config.screen_height)
image bg mpool     = im.Scale("images/Background/warung-mpool.jpg",      config.screen_width, config.screen_height)
image bg kantin = Transform(
    "images/Background/kantin-jica.jpg",
    xysize=(config.screen_width, config.screen_height),
    fit="cover"
)
image bg kosan = Transform(
    "images/Background/kosan-malam.jpg",
    xysize=(config.screen_width, config.screen_height),
    fit="cover"
)
image bg kosan_pg = Transform(
    "images/Background/kosan-pagi.jpg",
    xysize=(config.screen_width, config.screen_height),
    fit="cover"
)

## Belum ada gambarnya -> sementara pakai warna polos.
## Kalau sudah punya, ganti dengan im.Scale("images/Background/xxx.jpg", ...)
image bg parkir    = Solid("#4a4f57")

## ------------------------------------------------------------
##  SPRITE KARAKTER
##  Format: ekspresi: (file saat diam, file saat bicara)
##  Di script dipakai lewat:  $ tampil("az", "smile")  /  $ eks("az", "oof")
## ------------------------------------------------------------
init python:
    SPRITES = {
        "az": ("Az", {
            "hmm":   ("idle-hmm.png",         "talking-hmm.png"),
            "oof":   ("idle-oof.png",         "talking-oof.png"),
            "smile": ("idle-smile.png",       "talking-smile.png"),
            "sweet": ("sweetsmile-idle.png",  "sweetsmile-talking.png"),
        }),
        "bz": ("Bz", {
            "neutral": ("idle.png",             "talking-with-little smile.png"),
            "oof":     ("idle-oof.png",         "idle-oof.png"),
            "sweet":   ("idle-sweet-smile.png", "talking-with-little smile.png"),
        }),
        "cz": ("Cz", {
            "smile":      ("idle-smile.png",       "talking-smile.png"),
            "stand":      ("idle-stand.png",       "talking-stand.png"),
            "standsmile": ("idle-stand-smile.png", "talking-stand.png"),
            "oof":        ("idle-oof.png",         "talking-oof.png"),
            "hmm":        ("talking-hmm.png",      "talking-hmm.png"),
        }),
        "dz": ("Dz", {
            "smile": ("idle-smile.png", "talking.png"),
            "oof":   ("idle-oof.png",   "talking.png"),
            "angry": ("angry.png",      "angry.png"),
            "sad":   ("sad.png",        "sad.png"),
        }),
    }

    # Posisi horizontal tiap karakter di layar (0.0 kiri - 1.0 kanan)
    POS_X = {"az": 0.0, "bz": 0.33, "cz": 0.66, "dz": 1.0}

    # Urutan tumpukan: angka lebih besar = lebih depan
    ZORDER = {"dz": 1, "az": 2, "bz": 2, "cz": 2}

    # Daftarkan semua sprite sebagai image:  "az idle_smile", "az talk_smile", dst.
    for _tag, (_folder, _exps) in SPRITES.items():
        for _exp, (_idle, _talk) in _exps.items():
            renpy.image(_tag + " idle_" + _exp,
                        Transform(SPR_DIR + _folder + "/" + _idle, zoom=SPRITE_ZOOM))
            renpy.image(_tag + " talk_" + _exp,
                        Transform(SPR_DIR + _folder + "/" + _talk, zoom=SPRITE_ZOOM))

    def tampil(tag, exp):
        """Munculkan karakter dengan ekspresi tertentu."""
        store.cur_exp[tag] = exp
        renpy.show(tag + " idle_" + exp,
                   at_list=[Transform(xalign=POS_X[tag], yalign=-1.0)],
                   zorder=ZORDER[tag])

    def eks(tag, exp):
        """Ganti ekspresi karakter yang sedang tampil."""
        store.cur_exp[tag] = exp
        if renpy.showing(tag):
            renpy.show(tag + " idle_" + exp)

    def sembunyi(*tags):
        for t in (tags or POS_X.keys()):
            renpy.hide(t)

    def _talk_cb(tag, event, interact=True, **kwargs):
        """Saat karakter bicara -> sprite 'talk', selesai -> kembali 'idle'."""
        if not interact:
            return
        if not renpy.showing(tag):
            return
        exp = store.cur_exp.get(tag)
        if exp is None:
            return
        if event == "show":
            renpy.show(tag + " talk_" + exp)
        elif event in ("slow_done", "end"):
            renpy.show(tag + " idle_" + exp)

default cur_exp = {}

## ------------------------------------------------------------
##  KARAKTER
##  Az = Darren | Bz = Jubariah | Cz = Mukidi | Dz = Keane
## ------------------------------------------------------------
define n  = Character(color="#cccccc")
define az = Character("Darren",   color="#4aa3ff", callback=lambda event, **kw: _talk_cb("az", event, **kw))
define bz = Character("Jubariah", color="#5fd38d", callback=lambda event, **kw: _talk_cb("bz", event, **kw))
define cz = Character("Mukidi",   color="#ff7a59", callback=lambda event, **kw: _talk_cb("cz", event, **kw))
define dz = Character("Keane",    color="#f2c94c", callback=lambda event, **kw: _talk_cb("dz", event, **kw))
define pj = Character("Penjual",     color="#bbbbbb")
define mm = Character("Mbak Kantin", color="#bbbbbb")

## Monolog batin Darren
define az_hati = Character("Darren (Dalam Hati)", color="#4aa3ff", what_italic=True,
                           callback=lambda event, **kw: _talk_cb("az", event, **kw))

## ------------------------------------------------------------
##  AUDIO
##  (baru ada musik ending; musik latar bisa ditambah nanti)
## ------------------------------------------------------------
define MUSIK_BAD     = "audio/bad_end.mp3"
define MUSIK_NEUTRAL = "audio/neutral_end.mp3"
define MUSIK_GOOD    = "audio/good_end.mp3"
define MUSIK_MAIN    = "audio/main.mp3"   # lalu  play music MUSIK_MAIN fadein 1.5  di label start

## ------------------------------------------------------------
##  VARIABEL & KONFIGURASI KEUANGAN
## ------------------------------------------------------------
default duid       = 1000000   # saldo bulanan
default hemat      = 0         # Meteran Hemat
default validasi   = 0         # Meteran Validasi Sosial
default boros_cnt  = 0         # jumlah pilihan Opsi A
default pinjol     = False
default saldo_txt  = ""
default rp_now     = "Rp1.000.000"

define SAKU_AWAL     = 1000000
define SALDO_GOOD    = 800000  # >= ini            -> Good Ending
define SALDO_NEUTRAL = 600000  # >= ini            -> Neutral Ending
                               # < ini (Sabtu)     -> Pinjol -> Bad Ending
define SALDO_TABUNG  = 700000  # sisa aman 23 hari ke depan; kelebihannya = tabungan
define DANA_PINJOL   = 300000

init python:
    def rp(angka):
        """Format angka jadi 'Rp1.000.000'."""
        teks = "{:,}".format(abs(int(angka))).replace(",", ".")
        return ("-Rp" if angka < 0 else "Rp") + teks

    def update_hud():
        store.rp_now = rp(store.duid)

    def kurangi(jumlah):
        store.duid -= jumlah
        update_hud()
        renpy.notify("Saldo -" + rp(jumlah))

init:
    style location_text:
        color "#FFFFFF"
        outlines [(2, "#00000099", 0, 0)]

    style day_text:
        color "#FFFFFF"
        size 44
        outlines [(3, "#000000CC", 0, 0)]


screen location_title(day, location):
    vbox:
        xalign 0.5
        yalign 0.5
        spacing 5

        text day style "day_text" xalign 0.5
        text location style "location_text" xalign 0.5

## ------------------------------------------------------------
##  HUD SALDO
## ------------------------------------------------------------
screen hud_keuangan():
    zorder 100
    frame:
        align (1.0, 0.0)
        xoffset -20
        yoffset 20
        padding (18, 12)
        background Solid("#000000aa")
        vbox:
            spacing 4
            text "Saldo: [rp_now]" size 26 color ("#ff5c5c" if duid < SALDO_NEUTRAL else "#ffffff")
            text "Hemat: [hemat]   Validasi: [validasi]" size 18 color "#dddddd"

## Dijalankan otomatis setiap kali pemain selesai memuat save file
label after_load:

    ## Hentikan musik menu utama saja, jangan musik lain
    if renpy.music.get_playing() == config.main_menu_music:
        stop music fadeout 1.5

        play music MUSIK_MAIN fadein 1.0

    return

## ============================================================
##  MULAI GAME
## ============================================================
label start:

    stop music fadeout 2.5

    $ duid = SAKU_AWAL
    $ hemat = 0
    $ validasi = 0
    $ boros_cnt = 0
    $ pinjol = False
    $ cur_exp = {}
    $ update_hud()

    pause 3.0

    show screen hud_keuangan

    n "Darren, mahasiswa perantau Ilmu Komputer UPI dari sebuah desa terpencil."
    n "Ia membawa satu tekad: mengangkat derajat dan mengharumkan nama keluarganya."
    n "Uang makan dan minumnya hanya Rp1.000.000 untuk satu bulan penuh."
    n "Bertahanlah selama 7 hari pertama. Setiap pilihanmu menentukan nasib dompet Darren."

    play music MUSIK_MAIN fadein 1.5

    jump hari_senin


## ============================================================
##  PROLOG + HARI SENIN
## ============================================================
label hari_senin:

    scene bg kantin with fade

    show screen location_title(
        "SENIN",
        "10.20 WIB - Kantin JICA Gedung A, UPI"
    )
    pause 2.0

    hide screen location_title

    $ tampil("az", "smile")
    $ tampil("bz", "neutral")
    $ tampil("cz", "smile")
    $ tampil("dz", "smile")
    with dissolve

    n "Pukul 10.20 WIB. Suasana Kantin JICA Gedung A UPI tampak begitu riuh. Di antara kepulan asap gorengan dan aroma kopi kantin, Darren duduk bersama ketiga temannya: Jubariah, Mukidi, dan Keane."
    n "Darren, seorang mahasiswa perantau dari desa terpencil, membawa beban harapan yang besar. Niatnya satu: menimba ilmu di Prodi Ilmu Komputer UPI demi mengangkat derajat keluarganya di kampung halaman."

    $ eks("az", "hmm")
    az_hati "Uang saku satu juta rupiah dari orang tua di kampung untuk bertahan hidup sebulan... Nominal yang harusnya kupegang dengan penuh kehati-hatian. Tapi di Bandung, godaannya luar biasa."

    # (CG: Darren menunjukkan layar QRIS)
    $ eks("az", "smile")
    az "Mbak, es kopi susunya satu ya. Extra topping boba sama keju. Pakai QRIS ya, Mbak."
    mm "Siap, A! Langsung scan aja ya."

    n "Bagi Darren, dompet tebal berisi uang tunai sudah ketinggalan zaman. Tinggal scan, beep, beres. Belum lagi langganan aplikasi digital yang otomatis autodebet: Potipai Premium, Utupz Premium, sampai WangZup Premium."
    n "Tanpa repot menghitung kembalian, hidup terasa sangat mudah."
    n "Selesai memesan, pesanan datang. Saatnya membayar transaksi pertama di minggu ini."

    menu:
        "Mentraktir teman-teman menggunakan promo cashback QRIS.":
            $ kurangi(150000)
            $ boros_cnt += 1
            $ validasi += 2

            $ eks("dz", "smile")
            dz "Nah, ini baru temen kita! Next time traktir kita lagi yah, Darren."
            $ eks("cz", "smile")
            cz "Aishh, banyak duit nih si Darren! Makasih banyak, bro, sering-sering ya traktir kita."
            $ eks("az", "smile")
            az "Apasih, biasa aja kali. Dikira aku Ayah kalian?"
            dz "Hahaha, mantap!"
            cz "Hahaha!"
            $ eks("bz", "sweet")
            bz "Makasih ya, Darren. Wah, sering-sering nih..."
            az "Sama-sama, Jubariah."
            n "Saldo Darren berkurang cukup drastis untuk Senin pertama. Namun rasa bangga dan tawa teman-temannya membuat Darren merasa keputusannya tidak salah."

        "Hanya membayar pesanan sendiri.":
            $ kurangi(35000)
            $ hemat += 2

            $ eks("az", "smile")
            az "Udah ya, ini punya aku sendiri aja. Kalian bayar masing-masing ya."
            $ eks("cz", "oof")
            cz "Dih, pelit amat sekarang si Darren. Padahal kan lagi ada promo cashback QRIS tuh."
            $ eks("dz", "oof")
            dz "Iya nih, tumben banget perhitungan. Kurang seru ah, Darren."
            $ eks("bz", "sweet")
            bz "Enggak apa-apa sih, bagus juga buat jaga-jaga dompet akhir bulan nanti."
            $ eks("az", "sweet")
            az "Hehe, lagi ingin hemat aja. Dompet mulai menipis nih."
            n "Saldo Darren aman terkendali. Meskipun Mukidi dan Keane sempat melirik sinis karena menganggap Darren kurang asyik, Jubariah justru menatapnya dengan pandangan menghargai."

    jump hari_selasa


## ============================================================
##  HARI SELASA
## ============================================================
label hari_selasa:

    scene bg fmipa with fade

    show screen location_title(
        "SELASA",
        "Godaan Flash Sale & Jam Kosong"
    )
    pause 2.0

    hide screen location_title

    $ tampil("az", "hmm")
    $ tampil("bz", "neutral")
    $ tampil("cz", "smile")
    $ tampil("dz", "oof")
    with dissolve

    n "Pukul 13.00 WIB. Jam kosong melanda. Darren duduk di tangga gedung kuliah FPMIPA sambil memainkan ponselnya. Notifikasi flash sale tanggal kembar terus bermunculan di layar."

    cz "Eh, Darren! Lagi ada diskon 50%% nih di aplikasi antar makanan. Patungan ongkir yuk, gue mau pesan ayam geprek mozza sama boba."
    bz "Jangan boros-boros, Mukidi. Minggu baru jalan dua hari. Mending makan di kantin biasa atau bawa bekal."
    dz "Iya sih, tapi laper juga ya... Ikut Mukidi deh kalau pesannya enak."

    menu:
        "Ikut memesan makanan mahal lewat aplikasi + minuman kekinian.":
            $ kurangi(70000)
            $ boros_cnt += 1
            $ validasi += 1

            $ eks("az", "smile")
            az "Wah, menarik tuh! Ikut deh, pesenin satu ya, Mukidi. Pakai akun aku aja, biar dapet cashback."
            $ eks("cz", "standsmile")
            cz "Nah, gitu dong! Mantap jiwa si Darren!"
            $ eks("bz", "oof")
            bz "Hadeuh, mulai deh..."
            n "Saldo Darren kembali terkikis cukup besar untuk makan siang yang sebenarnya bisa dibeli jauh lebih murah di kantin."

        "Menolak ajakan dan makan di kantin biasa.":
            $ kurangi(20000)
            $ hemat += 2

            $ eks("az", "oof")
            az "Duh, pass dulu deh kalian. Lagi ingin hemat, mau makan di kantin biasa aja."
            $ eks("cz", "oof")
            cz "Ih, kurang seru amat. Yaudah deh, kita berdua aja."
            $ eks("bz", "sweet")
            bz "Pilihan bagus, Darren. Lanjutkan prinsip hematnya."
            n "Darren menikmati makanan kantin dengan porsi pas dan dompet tetap aman."

    jump hari_rabu


## ============================================================
##  HARI RABU
## ============================================================
label hari_rabu:

    scene bg space52 with fade

    show screen location_title(
        "RABU",
        "Tugas Kelompok & Space 52"
    )
    pause 2.0

    hide screen location_title

    $ tampil("az", "smile")
    $ tampil("bz", "neutral")
    $ tampil("cz", "oof")
    $ tampil("dz", "smile")
    with dissolve

    n "Rabu sore, kelompok tugas coding berkumpul di Space 52 Gegerkalong. Secangkir kopi menemani diskusi mereka."

    bz "Web-nya udah jadi total nih, tinggal dicek ulang aja. Oh ya, patungan kas buat langganan hosting server tugas kelompok kita kena Rp25.000 per orang ya."
    cz "Duh, kas lagi? Mending buat beli skin game gak sih?"
    $ eks("dz", "oof")
    dz "Ya mau gimana lagi, wajib kan dari dosen."

    menu:
        "Bayar kas, lalu impulsif jajan rokok dan snack impor demi gaya.":
            $ kurangi(75000)
            $ boros_cnt += 1
            $ validasi += 1

            $ eks("az", "smile")
            az "Nih uang kasnya. Eh, Mbak, bungkusin rokok sama snack impor ini juga ya satu!"
            $ eks("dz", "smile")
            dz "Wih, gaya bener anak bos satu ini."
            az "Biar otak encer, bro!"
            n "Pengeluaran tak terduga membengkak akibat menuruti gengsi sesaat."

        "Bayar kas wajib saja dan pesan teh hangat standar.":
            $ kurangi(30000)
            $ hemat += 2

            $ eks("az", "sweet")
            az "Nih uang kasnya, pas ya Rp25.000. Pesan es teh manis aja satu."
            $ eks("bz", "sweet")
            bz "Mantap, pas dan transparan pengeluarannya."
            n "Kewajiban terpenuhi tanpa merusak alokasi anggaran bulanan."

    jump hari_kamis


## ============================================================
##  HARI KAMIS
## ============================================================
label hari_kamis:

    scene bg parkir with fade

    show screen location_title(
        "KAMIS",
        "Kebutuhan Mendadak & Jebakan QRIS"
    )
    pause 2.0

    hide screen location_title

    $ tampil("az", "oof")
    with dissolve

    n "Kamis pagi cuaca mendung. Saat hendak berangkat kuliah, ban motor Darren terasa agak kempes dan butuh isi angin berbayar."

    ## Pindah ke malam hari - tempat nongkrong
    scene bg nongkrong with fade
    $ tampil("az", "hmm")
    $ tampil("bz", "neutral")
    $ tampil("cz", "smile")
    $ tampil("dz", "smile")
    with dissolve

    n "Malam harinya, ajakan nongkrong datang."

    dz "Darren, nanti malam anak-anak ngajak ngopi di kafe estetik daerah Gegerkalong. Ikut ya? Biar hits."

    menu:
        "Ikut nongkrong dan mentraktir sebagian pesanan pakai QRIS.":
            $ kurangi(90000)
            $ boros_cnt += 1
            $ validasi += 2

            $ eks("az", "smile")
            az "Aman, malam ini aku ikut! Biar aku yang scan QRIS buat pesanan kopi kalian ya."
            $ eks("cz", "standsmile")
            cz "Gila, sultan emang! Makasih, Darren!"
            n "Saldo Darren semakin menipis, mendekati zona merah."

        "Menolak dengan halus karena ada tugas kuliah.":
            $ kurangi(15000)
            $ hemat += 2

            $ eks("az", "oof")
            az "Maaf banget guys, malam ini aku harus selesain laporan coding dulu, takut keteteran."
            $ eks("bz", "sweet")
            bz "Bener banget, tugas harus diutamakan. Semangat ya, Darren!"
            n "Darren menghemat pengeluaran nongkrong malam dan fokus pada studinya. Makan malamnya cukup semangkuk mi di kosan."

    jump hari_jumat


## ============================================================
##  HARI JUMAT
## ============================================================
label hari_jumat:

    scene bg mpool with fade

    show screen location_title(
        "JUMAT",
        "Ujian Mental & Warung Nasi M'pool"
    )
    pause 2.0

    hide screen location_title

    $ tampil("az", "smile")
    $ tampil("cz", "standsmile")
    with dissolve

    n "Jumat siang. Aroma menggugah selera mengepul dari Warung Nasi Legendaris M'pool di dekat Masjid Daarut Tauhiid."

    pj "Mau makan apa, A? Langsung ambil di situ aja."
    cz "Wah, gila wangi banget! Sikat, Darren, kita makan besar hari ini!"

    menu:
        "Ambil lauk banyak dan mahal pakai QRIS, lalu mampir beli Haus! di seberang.":
            $ kurangi(60000)
            $ boros_cnt += 1
            $ validasi += 1

            az "Pak, pakai ini, itu, terus ditambah ini ya Pak, terus dikasih yang itu juga!"
            pj "Siap, A, mantap jiwa porsinya!"
            n "Perut kenyang, namun saldo rekening langsung menjerit."

        "Makan dengan porsi yang sesuai.":
            $ kurangi(25000)
            $ hemat += 2

            $ eks("az", "sweet")
            az "Pak, pakai ini itu seperti biasanya ya."
            pj "Siap, A! Pas buat tenaga kuliah sore!"
            n "Makan nikmat tanpa bikin dompet sekarat."

    jump hari_sabtu


## ============================================================
##  HARI SABTU - Cek m-banking
## ============================================================
label hari_sabtu:

    scene bg kosan with fade

    show screen location_title(
        "SABTU",
        "Weekend & Tekanan Finansial Memuncak"
    )
    pause 2.0

    hide screen location_title

    $ tampil("az", "hmm")
    with dissolve

    n "Sabtu malam. Darren mengecek aplikasi m-banking di ponselnya."

    $ saldo_txt = rp(duid)
    n "Saldo terakhir: {b}[saldo_txt]{/b}."

    stop music fadeout 1.5

    ## Jatah sehat: sisa uang harus cukup untuk 23 hari ke depan.
    if duid < SALDO_NEUTRAL:

        $ pinjol = True
        $ duid += DANA_PINJOL
        $ update_hud()

        $ eks("az", "oof")
        n "Darren mengambil jalan pintas instan menggunakan layanan Pinjaman Online (Pinjol) kilat untuk mendapatkan uang."
        az "Duh, saldo kurang banget buat sisa bulan ini, apalagi langganan autodebet masih jalan terus. Pinjol kilat aja deh sebentar, kan gampang, tinggal foto pakai KTP."
        n "Dana cair cepat, tapi bunga tinggi mulai mengintai."

    else:

        $ eks("az", "sweet")
        az "Alhamdulillah masih ada sisa, harus hati-hati sama pengeluaran..."
        n "Darren masih bisa bertahan hidup hingga beberapa hari ke depan."

    jump hari_minggu


## ============================================================
##  HARI MINGGU - Penentuan ending
## ============================================================
label hari_minggu:

    scene bg kosan_pg with fade

    show screen location_title(
        "MINGGU",
        "Hari Penentuan"
    )
    pause 2.0

    hide screen location_title

    $ tampil("az", "hmm")
    with dissolve

    n "Hari ke-7. Kalkulasi keuangan otomatis keluar di layar ponsel Darren berdasarkan seluruh pilihannya."

    if pinjol:
        $ pengeluaran = SAKU_AWAL - (duid - DANA_PINJOL)
    else:
        $ pengeluaran = SAKU_AWAL - duid
    $ pengeluaran_txt = rp(pengeluaran)
    $ saldo_txt = rp(duid)

    n "Total pengeluaran 7 hari: [pengeluaran_txt]."

    if pinjol:
        jump ending_bad
    elif duid >= SALDO_GOOD:
        jump ending_good
    else:
        jump ending_neutral


## ------------------------------------------------------------
##  BAD ENDING
## ------------------------------------------------------------
label ending_bad:

    scene bg kosan with dissolve
    play music MUSIK_BAD fadein 1.5

    $ pinjol_txt = rp(DANA_PINJOL)
    $ tampil("az", "oof")
    with dissolve

    centered "{size=40}{color=#ff4d4d}BAD ENDING{/color}{/size}\nJeratan Lingkaran Merah"

    az "Sial... uang bulanan sudah ludes duluan. Gara-gara gengsi traktir teman dan terjebak pinjol kilat, sekarang aku pusing dikejar debt collector..."
    n "Pinjol sebesar [pinjol_txt] kini beranak-pinak bersama bunganya. Notifikasi penagihan membanjiri ponsel Darren siang dan malam."
    n "Harapan keluarga di kampung halaman terasa semakin jauh. Darren baru sadar: validasi sosial sesaat tidak pernah sebanding dengan masa depan."

    centered "{b}TAMAT{/b}\nPelajaran: gengsi itu mahal, pinjol jauh lebih mahal."

    jump akhir_game


## ------------------------------------------------------------
##  NEUTRAL ENDING
## ------------------------------------------------------------
label ending_neutral:

    scene bg kosan with dissolve
    play music MUSIK_NEUTRAL fadein 1.5

    $ tampil("az", "hmm")
    with dissolve

    centered "{size=40}{color=#f2c94c}NEUTRAL ENDING{/color}{/size}\nBertahan di Ujung Tanduk"

    $ eks("az", "oof")
    az "Fiuh... untung saldonya masih [saldo_txt]. Cukup buat makan mi instan sampai akhir bulan, tapi nabung? Jauh dari kata mungkin."
    $ eks("az", "smile")
    az "Bulan depan harus lebih disiplin!"
    n "Darren selamat tanpa pinjol, namun harus menjalani hari-hari penuh mi instan dan tanpa tabungan sepeser pun."

    centered "{b}TAMAT{/b}\nSelamat, tapi masih bisa lebih baik."

    jump akhir_game


## ------------------------------------------------------------
##  GOOD ENDING
## ------------------------------------------------------------
label ending_good:

    scene bg kosan_pg with dissolve
    play music MUSIK_GOOD fadein 1.5

    $ tabungan = max(0, duid - SALDO_TABUNG)
    $ tabungan_txt = rp(tabungan)

    $ tampil("az", "sweet")
    $ tampil("bz", "sweet")
    with dissolve

    centered "{size=40}{color=#5fd38d}GOOD ENDING{/color}{/size}\nMahasiswa Teladan & Finansial Sehat"

    bz "Hebat juga kamu, Darren. Dari awal minggu sampai hari ke-7 tetap santai dan gak pernah pusing masalah uang."
    az "Hehehe, kuncinya cuma satu, Jubariah: jangan kalah sama gengsi dan pintar atur skala prioritas!"
    n "Saldo Darren masih [saldo_txt]. Setelah disisihkan untuk kebutuhan sampai akhir bulan, ia bisa menabung sekitar {b}[tabungan_txt]{/b}."
    $ eks("az", "hmm")
    az_hati "Tabungan ini bisa kupakai buat meringankan beban Ibu dan Bapak di desa. Sedikit demi sedikit, aku pasti bisa mengangkat derajat keluarga."

    centered "{b}TAMAT{/b}\nKamu berhasil mengelola keuangan dengan bijak!"

    jump akhir_game


## ------------------------------------------------------------
##  CREDITS (menggulir dari bawah ke atas)
## ------------------------------------------------------------
transform gulir_kredit(durasi):
    yanchor 0.0
    ypos 1.0
    linear durasi yanchor 1.0 ypos 0.0

style kredit_judul is default:
    size 60
    bold True
    color "#ffd166"
    xalign 0.5
    textalign 0.5

style kredit_header is default:
    size 38
    bold True
    color "#ffd166"
    xalign 0.5
    textalign 0.5

style kredit_jabatan is default:
    size 26
    color "#9aa7bd"
    xalign 0.5
    textalign 0.5

style kredit_isi is default:
    size 30
    color "#e8edf5"
    xalign 0.5
    textalign 0.5

style kredit_pemisah is default:
    size 28
    color "#555d6e"
    xalign 0.5
    textalign 0.5

screen kredit(durasi=60.0):
    add Solid("#000000")

    vbox:
        at gulir_kredit(durasi)
        xalign 0.5
        spacing 10

        text _("CREDIT SCENE") style "kredit_judul"

        null height 30
        text _("==================================") style "kredit_pemisah"
        null height 30

        ## ---------------- PENULISAN & NARASI ----------------
        text _("- PENULISAN & NARASI -") style "kredit_header"
        null height 20

        text _("Scenario Writer / Scriptwriter") style "kredit_jabatan"
        text _("Reyfan Raharjo") style "kredit_isi"
        null height 14

        text _("Editor / Proofreader") style "kredit_jabatan"
        text _("Reyfan Raharjo") style "kredit_isi"

        null height 30
        text _("==================================") style "kredit_pemisah"
        null height 30

        ## ---------------- DESAIN & SENI VISUAL ----------------
        text _("- DESAIN & SENI VISUAL -") style "kredit_header"
        null height 20

        text _("Character Designer") style "kredit_jabatan"
        text _("Reyfan Raharjo") style "kredit_isi"
        null height 14

        text _("Sprite Artist") style "kredit_jabatan"
        text _("Reyfan Raharjo") style "kredit_isi"
        null height 14

        text _("Background Generation") style "kredit_jabatan"
        text _("Gemini AI") style "kredit_isi"
        null height 14

        text _("UI/UX Generation") style "kredit_jabatan"
        text _("Claude AI") style "kredit_isi"
        null height 14

        text _("Title Designer") style "kredit_jabatan"
        text _("Alfriza Akhmad Rahadi") style "kredit_isi"

        null height 30
        text _("==================================") style "kredit_pemisah"
        null height 30

        ## ---------------- MUSIK & AUDIO ----------------
        text _("- MUSIK & AUDIO -") style "kredit_header"
        null height 20

        text _("Background Music") style "kredit_jabatan"
        text _("\"Two, Alone\" by dai") style "kredit_isi"
        text _("\"Daijoubu!\" by Dan Salvato") style "kredit_isi"
        text _("\"Athena Cykes ~ Courtroom Révolutionnaire\" by Noriyuki Iwadare") style "kredit_isi"
        text _("\"Silence\" by Higurashi Visual Novel BGM") style "kredit_isi"
        text _("\"Sayo-nara\" by Dan Salvato") style "kredit_isi"

        null height 30
        text _("==================================") style "kredit_pemisah"
        null height 30

        ## ---------------- PEMROGRAMAN & TEKNIS ----------------
        text _("- PEMROGRAMAN & TEKNIS -") style "kredit_header"
        null height 20

        text _("Lead Programmer") style "kredit_jabatan"
        text _("Alfriza Akhmad Rahadi") style "kredit_isi"
        null height 14

        text _("Scripting / Implementation") style "kredit_jabatan"
        text _("Alfriza Akhmad Rahadi") style "kredit_isi"
        null height 14

        text _("UI Programmer") style "kredit_jabatan"
        text _("Alfriza Akhmad Rahadi") style "kredit_isi"
        null height 14

        text _("Programming Assistance") style "kredit_jabatan"
        text _("Assisted by Claude AI, Chat GPT") style "kredit_isi"

        null height 30
        text _("==================================") style "kredit_pemisah"
        null height 30

        text _("Made with Ren'Py") style "kredit_header"

        null height 30
        text _("==================================") style "kredit_pemisah"
        null height 30

        ## ---------------- SPECIAL THANKS ----------------
        text _("- SPECIAL THANKS -") style "kredit_header"
        null height 20

        text _("Nandha Najmi Ihsani") style "kredit_isi"
        text _("Rifo Rijal Al Hakim") style "kredit_isi"
        text _("Gemini AI") style "kredit_isi"
        text _("Claude AI") style "kredit_isi"
        text _("ChatGPT") style "kredit_isi"
        text _("Itch.io") style "kredit_isi"

        null height 40
        text _("© 2026 KELOMPOK 10") style "kredit_jabatan"

        null height 200

label akhir_game:

    hide screen hud_keuangan
    $ sembunyi()
    $ quick_menu = False
    scene black with fade

    ## Credits (klik untuk melewati)
    show screen kredit(60.0)
    pause 61.0
    hide screen kredit
    with fade

    centered "Terima kasih sudah bermain!"

    $ quick_menu = True
    stop music fadeout 3.0
    return