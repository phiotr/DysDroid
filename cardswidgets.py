# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#  

from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty
from kivy.uix.button import Button

from core import parse_word

class GenericCardWidget(Button):
    """
    Obiekt zaznaczalnej karty z obrazkiem
    //GUI//
    """

    # Czy karta jest zasłonięta
    flliped = BooleanProperty(False)

    # Czy dana karta z pary jest odsłonięta
    guessed = BooleanProperty(False)

    # Nazwy graficzek (przodu i tylu)
    cover = StringProperty("")
    front = StringProperty("")

    # ID pary kart
    cid = None
    # Dodatkowy opis kart
    dsc = None

    def __init__(self, cid, dsc, **kwargs):
        """
            @cid - id karty
            @dsc - opis karty pojawiajacy sie w dymku
        """
        Button.__init__(self, **kwargs)

        self.cid = cid
        self.dsc = dsc

    def toggle(self):
        """Odwrocenie karty"""
        self.flliped = not self.flliped


class FlippCard(GenericCardWidget):
    """
    Domylsnie zakryta karta zawierajaca jakis obrazek
    //GUI//
    """

    def __init__(self, cid, dsc, content, **kwargs):
        """
            @content - obrazek znajdujacy sie na przedzie karty
        """
        
        GenericCardWidget.__init__(self, cid, dsc, **kwargs)

        self.front = content
        self.cover = "res/cards/cover.png"

        self.flliped = True


class FlippTextCard(GenericCardWidget):
    """
    Domyslnie zakryta karta zawierajaca jakis napis
    //GUI//
    """

    def __init__(self, cid, dsc, content, **kwargs):
        """
            @content - tekst znajdujacy sie na przedzie karty
        """
        
        GenericCardWidget.__init__(self, cid, dsc, **kwargs)

        self.front = parse_word(content)
        self.cover = "res/cards/cover.png"

        self.flliped = True


class TicCard(GenericCardWidget):
    """
    Domyslnie odkyta karta zawierajaca jakis obrazek
    //GUI//
    """

    def __init__(self, cid, dsc, content, **kwargs):
        GenericCardWidget.__init__(self, cid, dsc, **kwargs)

        self.front = "res/cards/ok.png"
        self.cover = content

        self.flliped = False


class TicTextCard(GenericCardWidget):
    """
    Domyslnie odkyta karta zawierajaca jakis napis
    //GUI//
    """

    def __init__(self, cid, dsc, content, **kwargs):
        GenericCardWidget.__init__(self, cid, dsc, **kwargs)

        self.front = "res/cards/ok.png"
        self.cover = parse_word(content)

        self.flliped = False
