# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#  


from core import CH_SCREEN, EX_SCREEN
from exercise import Exercise



class GenericLevelChooser(Screen):
    """
    Uniwersalny ekran wyboru poziomów do gier karcianych
    //GUI//
    """

    # Przycisk powrotu do menu
    back_bt = ObjectProperty(None)

    # Przyciski wyboru poziomu
    level_1_bt = ObjectProperty(None)
    level_2_bt = ObjectProperty(None)
    level_3_bt = ObjectProperty(None)

    stats_bt = ObjectProperty(None)

    title = StringProperty("")

    def __init__(self, title, *args, **kwargs):
        """
            @title - tytul (nazwa) cwiczenia
        """
        
        Builder.load_file("kv/genericlevels.kv")
        Screen.__init__(self, *args, **kwargs)
        self.title = title


#class CardGameScreen(





# .:: ------- GAME ENGINE ------- ::. #

class CardGameExercise(Exercise):
    """
    Ogólna klasa definijuąca kompletne ćwiczenie przy użyciu kart.
    
    Spójnik łączący elementy menu z właściwymi ekranami zadań.
    """

    # Ekran właściwego zadania
    #game_screen = None
    exercise = None

    def __init__(self, name, desc, icon, table_name, level1_set, level2_set, level3_set, game_options={}, **kwargs):
        """
        Parametry:
            @name - nazwa zadania
            @desc - opis zadania (do wyświetlenia w menu)
            @icon - ikonka zadania (do wyświetlenia w menu)

            @level1_set - plik zawierający listę możliwych kart do rozlosowania na 1 poziomie
            @level2_set - plik zawierający listę możliwych kart do rozlosowania na 2 poziomie
            @level3_set - plik zawierający listę możliwych kart do rozlosowania na 3 poziomie

            @game_options - dodatkowe parametry gry (np. tryb zaznaczania kart, długoś czasu wyświetlania chmurki z wyrazem, itp)
        """
        Exercise.__init__(self, name=name, desc=desc, icon=icon, table_name=table_name, **kwargs)

        # Level Chooser
        lc = GenericLevelChooser(name=CH_SCREEN, title=name)

        lc.back_bt.bind(on_release=lambda bt: self.back_to_menu())

        game_options['table_name'] = table_name

        lc.level_1_bt.bind(on_release=lambda bt: self.launch_level(level_number=1, rows=3, cols=4, cards_set=level1_set, level_icon="res/icons/star1.png", **game_options))
        lc.level_2_bt.bind(on_release=lambda bt: self.launch_level(level_number=2, rows=4, cols=5, cards_set=level2_set, level_icon="res/icons/star2.png", **game_options))
        lc.level_3_bt.bind(on_release=lambda bt: self.launch_level(level_number=3, rows=5, cols=6, cards_set=level3_set, level_icon="res/icons/star3.png", **game_options))

        lc.stats_bt.bind(on_release=lambda bt: self.open_statistics())

        self.sm.add_widget(lc)

    def launch_level(self, **options):

        # Jeśli operacja nie jest zablokowana przez inne przejście SM
        if not self.lock:
            # Blkada
            self.lock = True

            # Jesli było już zadanko to je usuwamy
            if self.exercise and self.sm.has_screen(EX_SCREEN):
                self.sm.remove_widget(self.exercise)

            # <--------------- Tworzymy nowe --------------------------
            self.exercise = GenericCardsGame(name=EX_SCREEN, **options)

            # i dodajemy do okna
            self.sm.add_widget(self.exercise)
            self.sm.current = EX_SCREEN

            # Odblokowanie
            self.lock = False
        else:
            return

    def back_to_level_choose(self):
        """Powrót do wyboru poziomów trudności"""
        self.sm.current = CH_SCREEN

    def back_to_top_exercise_screen(self):
        current = self.sm.current

        # Jesli przycisnieto guzik wstecz będąc na ekranie poziomów trudności
        if current == CH_SCREEN:
            # to powrót do głównego menu
            self.back_to_menu()
        # wpw, powrót do wyboru poziomów
        else:
            self.sm.current = CH_SCREEN

    def open_statistics(self):
        """Utworzenie i wyświetlenie okienka zawierającego najlepszy i kilka ostatnich wyników z danego ćwiczenia"""

        self.stats = Popup(title=u"{t} - Wyniki".format(t=self.name), content=ExerciseScoresContent(table_name=self.table_name), size_hint_x=0.8)
        self.stats.open()
        self.stats.content.close_bt.bind(on_release=self.stats.dismiss)
