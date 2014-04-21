# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#  

# 

from card_game_exercise import CardGameExercise
from cardswidgets import TicCard, TicTextCard, FlippCard, FlippTextCard


ORTOMEMO_SET = "index/img_img_obrazki.txt"
Ortomemo = CardGameExercise(
    name=u"Ortomemo",
    desc=u"Połącz jednakowe obrazki w pary.",
    icon="res/icons/menu/ortomemo.png",
    table_name="ortomemo",
    level1_set=ORTOMEMO_SET,
    level2_set=ORTOMEMO_SET,
    level3_set=ORTOMEMO_SET,
)

ANTONYMS_SET="index/txt_txt_antonimy.txt"
Antonimy = CardGameExercise(
    name=u"Antonimy",
    desc=u"Wśród podanych wyrazów odszukaj pary wyrazów o przeciwnym znaczeniu.",
    icon="res/icons/menu/antonimy.png",
    table_name="antonimy",
    level1_set=ANTONYMS_SET,
    level2_set=ANTONYMS_SET,
    level3_set=ANTONYMS_SET,
    game_options={'Engine1': TicTextCard, 'Engine2': TicTextCard, 'auto_play': True, 'allow_unselecting': True},
)

ORTOGRAFIKI_SET="index/img_txt_obrazki.txt"
Ortografiki = CardGameExercise(
    name=u"Ortografiki",
    desc=u"Połącz w pary obrazki i opisujące je słowa.",
    icon="res/icons/menu/ortografy.png",
    table_name="ortografiki",
    level1_set=ORTOGRAFIKI_SET,
    level2_set=ORTOGRAFIKI_SET,
    level3_set=ORTOGRAFIKI_SET,
    game_options={'Engine1': FlippCard, 'Engine2': FlippTextCard},
)

Liczebniki = CardGameExercise(
    name=u"Liczebniki",
    desc=u"Połącz w pary liczby i odpowiadające im liczebniki główne.",
    icon="res/icons/menu/liczebniki.png",
    table_name="liczebniki",
    level1_set=xrange(1, 31),
    level2_set=xrange(20,101),
    level3_set=xrange(80,1000),
    game_options={'Engine1': TicTextCard, 'Engine2': TicTextCard, 'n_and_w': True, 'auto_play': True, 'allow_unselecting': True},
)

VARIETY_SET="index/txt_txt_odmiana.txt"
Odmiana = CardGameExercise(
    name=u"ó wymienne",
    desc=u"Połącz w pary wyrazy pokrewne.",
    icon="res/icons/menu/o_wymienne.png",
    table_name="odmiana",
    level1_set=VARIETY_SET,
    level2_set=VARIETY_SET,
    level3_set=VARIETY_SET,
    game_options={'Engine1': FlippTextCard, 'Engine2': FlippTextCard},
)

# Pelna lista zadan
EXERCISES_LIST = [Ortomemo, Antonimy, Ortografiki, Liczebniki, Odmiana, ]
