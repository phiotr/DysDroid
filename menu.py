# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#  

from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import SlideTransition

# Nazwa ekranu głównego MENU
from core import MENU_SCREEN_NAME as MENU
from exercise import Exercise


class MenuItem(Screen):
    """Ekran wyświetlany w menu jako element wyboru ćwiczenia"""

    icon = StringProperty("")
    desc = StringProperty("")

    def __init__(self, name, desc, icon, **kwargs):

        self.icon = icon
        self.desc = desc

        kwargs['name'] = name

        super(MenuItem, self).__init__(**kwargs)


class MenuScreen(Screen):
    """Główny ekran aplikacji - menu wyboru ćwiczeń"""

    # ScreenManager odpowiedzialny za wybór ćwiczenia (pierścieniowy przełącznik)
    menu_sm = ObjectProperty(None)

    # Strzałki do przewijania listy
    prev_exercise_bt = ObjectProperty(None)
    next_exercise_bt = ObjectProperty(None)

    # Przycisk otwarcia zadania
    goto_exercise_bt = ObjectProperty(None)

    # Animacje przejść ekranów
    prev_transition = SlideTransition(direction="right")
    next_transition = SlideTransition(direction="left")
    goto_transition = SlideTransition(direction="down", duration=0.4)

    ex_count = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        Builder.load_file("kv/menu.kv")

        super(MenuScreen, self).__init__(*args, **kwargs)

        self.prev_exercise_bt.bind(on_release=lambda bt: self.scroll_to_prev())
        self.next_exercise_bt.bind(on_release=lambda bt: self.scroll_to_next())

        self.goto_exercise_bt.bind(on_release=lambda bt: self.goto_exercise())

    def scroll_to_next(self):
        """Przesuniecie na nastepne cwiczenie"""

        if self.ex_count > 1:
            self.menu_sm.transition.stop()
            self.menu_sm.transition = self.next_transition
            self.menu_sm.current = self.menu_sm.next()

        else:
            print "* nie ma co przewijac"

    def scroll_to_prev(self):
        """Przesuniecie na poprzednie cwiczenie"""

        if self.ex_count > 1:
            self.menu_sm.transition.stop()
            self.menu_sm.transition = self.prev_transition
            self.menu_sm.current = self.menu_sm.previous()

        else:
            print "* nie ma co przewijac"

    def goto_exercise(self):
        """Przejście do wybranego ćwiczenia"""
        try:
            # ustawienie trybu przejścia
            self.manager.transition = self.goto_transition

            # Przejście do okna z zadaniem
            # (ta sama nazwa zadania jest zarejestrowana w najwyższym SM, jak i na pierścieniowym przełączniku)
            self.manager.current = self.menu_sm.current

        except Exception as e:
            print e.message

    def add_exercise(self, exercise):
        """Zarejestrowanie ćwiczenia w głównym menu"""

        if isinstance(exercise, Exercise) :

            self.manager.add_widget(exercise)

            self.menu_sm.add_widget(MenuItem(name=exercise.name, desc=exercise.desc, icon=exercise.icon))

            self.ex_count += 1

        else:
            print "Error: `{}` nie jest poprawnym obiektem ćwiczenia.".format(exercise)
