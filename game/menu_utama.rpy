## ============================================================
##  MENU UTAMA - "Yang Hemat Ya"
##  Taruh file ini di folder  game/  (sejajar dengan script.rpy).
##
##  Screen ini menggantikan  screen main_menu()  bawaan di screens.rpy.
##  (init offset = 1 membuat file ini dimuat belakangan, jadi
##   otomatis menimpa versi lama.)
## ============================================================

init offset = 1

## ------------------------------------------------------------
##  PENGATURAN CEPAT
## ------------------------------------------------------------
define mm_judul    = "Yang Hemat Ya"
define mm_subjudul = "Kisah mahasiswa perantau dan uang sebulan"
define mm_aksen    = "#ffd166"      # warna aksen (kuning emas)
define mm_latar    = "bg kosan"     # nama image latar menu utama
define mm_sprite   = "az idle_smile"  # sprite yang tampil di sisi kanan


## ------------------------------------------------------------
##  ANIMASI
## ------------------------------------------------------------
## Muncul pelan dari kiri
transform mm_masuk(delay=0.0):
    alpha 0.0
    xoffset -40
    pause delay
    ease 0.7 alpha 1.0 xoffset 0

## Sprite melayang naik-turun pelan + muncul dari kanan
transform mm_melayang:
    xalign 0.9
    yalign -1.0
    alpha 0.0
    xoffset 60
    ease 0.9 alpha 1.0 xoffset 0
    block:
        ease 2.2 yoffset -10
        ease 2.2 yoffset 0
        repeat


## ------------------------------------------------------------
##  LAYAR MENU UTAMA
## ------------------------------------------------------------
screen main_menu():

    ## Ini memastikan layar menu yang lain telah ditimpa
    tag menu

    style_prefix "mm"

    ## Latar + sedikit penggelap supaya tulisan mudah dibaca
    add mm_latar
    add Solid("#00000055")

    ## Panel gelap di sisi kiri + garis aksen di tepinya
    add Solid("#000000b8") xsize 640
    add Solid(mm_aksen) xpos 640 xsize 5

    ## Sprite karakter utama di sisi kanan
    add mm_sprite at mm_melayang

    ## Judul & subjudul
    vbox:
        at mm_masuk(0.1)
        xpos 70
        ypos 110
        spacing 10
        xmaximum 540

        text mm_judul style "mm_judul"
        text mm_subjudul style "mm_subjudul"

    ## Tombol-tombol menu
    vbox:
        at mm_masuk(0.4)
        xpos 40
        ypos 430
        spacing 6

        textbutton _("Mulai")   action Start()
        textbutton _("Muat")    action ShowMenu("load")
        textbutton _("Setting") action ShowMenu("preferences")
        textbutton _("Tentang") action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton _("Bantuan") action ShowMenu("help")

        if renpy.variant("pc"):
            textbutton _("Keluar") action Quit(confirm=False)

    ## Footer: versi game
    text "v[config.version]  |  Dibuat dengan Ren'Py" style "mm_footer":
        xpos 70
        yalign 0.98


## ------------------------------------------------------------
##  GAYA (STYLE)
## ------------------------------------------------------------
style mm_button is default:
    xsize 520
    ysize 64
    left_padding 30
    background None
    hover_background Solid("#ffffff22")
    insensitive_background None

style mm_button_text is default:
    size 34
    idle_color "#d9dee8"
    hover_color mm_aksen
    insensitive_color "#777777"
    yalign 0.5
    hover_outlines [(0, "#00000000", 0, 0)]

style mm_judul is default:
    size 64
    bold True
    color "#ffffff"
    outlines [(4, "#00000099", 0, 3)]

style mm_subjudul is default:
    size 24
    color mm_aksen
    italic True

style mm_footer is default:
    size 16
    color "#9aa3b2"
