# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#

# nazwa ekranu z menu
MENU_SCREEN_NAME = "MainMenu"

# nazwy ekranów w grach karciankach
CH_SCREEN = 'choose'
EX_SCREEN = 'level'

COLOR_MAP = {
    '/rz#': "[color=#ff0000]rz[/color]",
    '/Rz#': "[color=#ff0000]Rz[/color]",
    '/r#': "[color=#ff0000]r[/color]",

    '/ż#': "[color=#ffc000]ż[/color]",
    '/Ż#': "[color=#ffc000]Ż[/color]",
    '/g#': "[color=#ffc000]g[/color]",
    '/dz#': "[color=#ffc000]dz[/color]",

    '/u#': "[color=#00cd00]u[/color]",
    '/U#': "[color=#00cd00]U[/color]",

    '/ó#': "[color=#00a2ff]ó[/color]",
    '/Ó#': "[color=#00a2ff]Ó[/color]",
    '/o#': "[color=#00a2ff]o[/color]",
    '/O#': "[color=#00a2ff]O[/color]",
    '/a#': "[color=#00a2ff]a[/color]",
    '/e#': "[color=#00a2ff]e[/color]",

    '/sz#': "[color=#6000ff]sz[/color]",
    '/Sz#': "[color=#6000ff]Sz[/color]",
    '/h#': "[color=#d800ff]h[/color]",
    '/H#': "[color=#d800ff]H[/color]",
    '/ch#': "[color=#0012ff]ch[/color]",
    '/Ch#': "[color=#0012ff]Ch[/color]",
    '/ą#': "[color=#f6ff00]ą[/color]",
    '/om#': "[color=#b50051]om[/color]",
    '/ę#': "[color=#878787]ę[/color]",
    '/em#': "[color=#67773c]em[/color]",

    '/dż#': "[color=#C0D727]dż[/color]",
    '/Dż#': "[color=#C0D727]Dż[/color]",
    }


def parse_word(word):
    """Metoda która zamienia znaczniki w napisie /(_)# ma kolor przypisany do tego tagu"""
    word = word.replace('\n', '').replace('\r', '')

    for tag, color in COLOR_MAP.iteritems():
        word = word.replace(tag, color)

    return word


# Tablice wyrazów odpowiedzialnych za jedności/nastki/dziesiątki/setki
jede = [u'', u' jeden', u' dwa', u' trzy', u' cztery', u' pięć', u' sześć', u' siedem', u' osiem', u' dziewięć']
nasc = [u' dziesięć', u' jedenaście', u' dwanaście', u' trzynaście', u' czternaście', u' piętnaście', u' szesnaście', u' siedemnaście', u' osiemnaście', u' dziewiętnaście']
dzie = [u'', u' dziesięć', u' dwadzieścia', u' trzydzieści', u' czterdzieści', u' piećdziesiąt', u' sześćdziesiąt', u' siedemdziesiąt', u' osiemdziesiąt', u' dziewięćdziesiąt']
setk = [u'', u'sto', u'dwieście', u'trzysta', u'czterysta', u'pięćset', u'sześćset', u'siedemset', u'osiemset', u'dziewięćset']


def number_2_word(n):
    """Procedura zamiany liczby @n w jej zapis słowny"""

    in_words = u''

    # Renderowanie liczby
    if n == 0:
        in_words = u"zero"
    else:
        j = 1
        while n > 0:

            k = (n % 10)
            n //= 10

            if j == 3:
                in_words = setk[k] + in_words
                j = 0

            if j == 2:
                in_words = dzie[k] + in_words

            if j == 1:

                if n % 10 == 1:
                    in_words = nasc[k] + in_words
                    n //= 10
                    j += 1
                else:
                    in_words = jede[k] + in_words
            j+=1

    return " ".join(in_words.split()).encode('utf-8', errors='ignore')





