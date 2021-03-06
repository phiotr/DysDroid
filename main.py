#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#
__version__ = '1.2.2'

from kivy.utils import platform

# Ręczne ustawienie FullScreen dla systemu Linux
if platform == 'linux':
    from kivy.config import Config
    Config.set('graphics', 'width', '1280')
    Config.set('graphics', 'height', '752')
    Config.set('graphics', 'fullscreen', 'True')

from kivy.app import App
from kivy.base import EventLoop
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition

from menu import MenuScreen, MENU
from list_of_exercises import EXERCISES_LIST


# Klasa uruchamianej aplikacji
class DysDroidApp(App):

    title = "DysDroid"

    def build(self):
        Logger.info("Building application")
        # Najwyższy SM, odpowiedzialny za faktyczne przełączania zadań i menu
        root = ScreenManager()

        # Menu wyboru zadań
        menu = MenuScreen(name=MENU)
        # dodanie wypełnionego Menu do aplikacji
        root.add_widget(menu)

        # Dodanie listy ćwiczeń
        for e in EXERCISES_LIST:
            menu.add_exercise(e)

        EventLoop.window.bind(on_keyboard=self.on_back_button)        

        return root

    def on_pause(self):
        if self and self.root:
            Logger.debug("** Pause **")
            return True
        else:
            Logger.debug("Pause and no root")
            return False

    def on_resume(self):
        if self and self.root:
            Logger.debug("** Resume **")
            return True
        else:
            Logger.debug("Resume and no root")
            return False
    
    def on_stop(self):
        Logger.debug("Stoping...")
        return True

    def on_back_button(self, window, key, *largs):

        # Kod przycisku powrotu - 27 (Esc)
        if key == 27:

            # Jesli jestesmy w menu, zamykamy aplkacje
            if self.root.current == MENU:
                import sys
                sys.exit(0)

            # Jestescy w jakims zadanku
            else:
                exercise = self.root.get_screen(self.root.current)
                exercise.back_to_top_exercise_screen()

            return True


if __name__ == '__main__':
    DysDroidApp(kv_directory="./kv").run()
