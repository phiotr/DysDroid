# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#

from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import FadeTransition, SlideTransition

from database import DataBase


class Exercise(Screen):
    """
    Generyczny ekran (wyswietlany w menu aplikacji) reprezentujacy pojedyncze cwiczenie.
    """
    
    # Cechy zadanka:
    desc = StringProperty("")
    icon = StringProperty("")

    # Wewnętrzny ScreenManager odpowiedzialny za przełączanie ekranów wewnątrz zadania
    sm = ObjectProperty(None)

    # Okienko dialogowe statystyk
    stats = ObjectProperty(None)

    # Animacja powrotu do głownego menu
    back_transiton = SlideTransition(direction="up")

    # Blokada przełącznika ekranu
    lock = BooleanProperty(False)

    def __init__(self, name, desc, icon, table_name, *args, **kwargs):
        """
            @name - nazwa cwiczenia
            @desc - dlugi opis cwiczenia/polecenie/tresc zadania
            @icon - logo zadania widoczne w menu
            @table_name - nazwa tabeli w bazie przechowujaca rezultaty tego cwiczenia
            
            @args, @kwargs - dodatkowe parametry klasy kivy.uix.screenmanager.Screen
        """

        kwargs['name'] = name
        Screen.__init__(self, *args, **kwargs)

        # Konfiguracja ekrnau wyboru zadania
        self.icon = icon
        self.name = name
        self.desc = desc
        self.table_name = table_name

        self.sm = ScreenManager(transition=FadeTransition())
        self.add_widget(self.sm)

        # Przygotowanie tabeli w bazie
        DataBase.create_card_game_table(table_name)

    def back_to_menu(self):
        """Obsługa powrotu do menu głównego"""

        # Ukrycie okienka dialogowego statystyk, jeśli istnieje
        if self.stats:
            self.stats.dismiss()

        if not self.lock:
            self.lock = True

            self.manager.transition = self.back_transiton
            self.manager.current = MENU

            self.lock = False
        else:
            return

    def back_to_top_exercise_screen(self):
        """Obsługa wyjścia z ćwiczenia i powrotu do głównego ekranu zadania (np. wyboru poziomu)"""
        pass
