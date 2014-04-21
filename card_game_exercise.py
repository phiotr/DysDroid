# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#  

from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty
from kivy.clock import Clock

from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

from datetime import datetime as dt
from random import shuffle

from cardspair import CardsPair
from cardswidgets import FlippCard
from core import CH_SCREEN, EX_SCREEN
from database import DataBase
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


class ClockLabel(Label):
    """Zegarek cyfrowy"""
    
    # Wartości wyświetlane na zegarze
    c_min = NumericProperty(0)  # minuty
    c_sec = NumericProperty(0)  # sekundy

    # pełna godzina uruchomienia zegara
    start_time = None

    def start_clock(self):
        """Rozpoczęcie odmierzania czasu"""
        self.start_time = dt.now()
        Clock.schedule_interval(self._tick, 1.0 / 4)

    def stop_clock(self):
        """Zatrzymanie zegara"""
        Clock.unschedule(self._tick)
        self.start_time = None

    def _tick(self, t):
        """Tyknięcie zegara"""
        tick = dt.now()

        # ilość sekund od momentu uruchomienia zegara
        snd = (tick - self.start_time).seconds

        self.c_min = snd // 60
        self.c_sec = snd % 60

    def is_running(self):
        """Odpytanie o stan zegara. True - zegar jest uruchomiony, False - zegar jest zatrzymany"""
        return self.start_time is not None

    def get_time(self):
        """Pobranie odmierzonego czasu na zegarze (w sekundach)"""
        return self.c_min * 60 + self.c_sec

    def reset_clock(self):
        """Całkowite zresetowanie zegara"""
        # Jeśli zegar jest aktualnie uruchomiony, to zatrzymaj
        if self.is_running():
            self.stop_clock()

        # Wyzerowanie liczników
        self.c_min = 0
        self.c_sec = 0


class Toast(Label):
    """Znikająca etykietka. Wyświetla tekst tylko przez pewien podany czas"""

    hint_msg = StringProperty("")
    hint_timeout = NumericProperty(0)

    def __init__(self, *args, **kwargs):
        Label.__init__(self, *args, **kwargs)

        # Skracanie co 1s dlugosci czasu wyswietlania wiadomosci
        Clock.schedule_interval(self._tick, 1.0)

    def set_msg(self, msg, time):
        self.hint_msg = msg
        self.hint_timeout = time

    def _tick(self, dt):
        self.hint_timeout = (self.hint_timeout -1) if (self.hint_timeout > 0) else 0

    def disable(self):
        Clock.unschedule(self._tick)


class ResultInfoPopup(Popup):
    """Okienko dialogowe informujące o zakończeniu zadania i wyświetlające czas rozwiązania"""

    def __init__(self, score, **kwargs):

        self.title = "Koniec zadania"
        self.size_hint = (None, None)
        self.size = (550, 400)

        Popup.__init__(self, **kwargs)

        # Przygotowanie treści komunikatu
        box = BoxLayout(orientation="vertical")

        color = "#00EE00"
        time = "[color={c}]{s}[/color] sekund".format(s=score, c=color) if score < 60 else "[color={c}]{m:>02}:{s:>02}[/color] minuty".format(m=score // 60, s=score % 60, c=color)

        l = Label(text=u"[size=45][b]G r a t u l a c j e![/b][/size]\n\nZadanie zostało ukończone w czasie\n\n{time}.".format(time=time), markup=True, font_size=30, halign="center")
        b = Button(text="Ok", size_hint=(1.0, 0.2), on_release=self.dismiss)

        box.add_widget(l)
        box.add_widget(b)

        self.content = box


class GenericCardGame(Screen):
    """Uniwersalna klasa posiadająca całą potrzebną mechanikę do gier polegających na odkrywaniu kart"""
    card_grid = ObjectProperty(None)

    card_grid_rows = NumericProperty(1)
    card_grid_cols = NumericProperty(1)

    pairs_total = NumericProperty(0)
    pairs_guessed = NumericProperty(0)

    current_selected = list()
    level_icon = StringProperty("")

    timer = ObjectProperty(None)
    notify = ObjectProperty(None)
    notify_timeout = NumericProperty(0)

    def __init__(self, level_number, rows, cols, cards_set, level_icon, table_name, Engine1=FlippCard, Engine2=FlippCard, notify_timeout=2, auto_play=False, allow_unselecting=False, n_and_w=False, **kwargs):
        """
        Parametry:
            @rows - liczba wierszy
            @cols - liczba kolumn
            @cards_set - plik ze zbiorem kart do rozlosowania
            @level_icon - ikona trudności poziomu
            @CardEngine - pochodna klasy CardsWidget definiująca wygląd i zachowanie kart po kliknięciu
            @notify_timeout - czas widoczności dynku (w sekundach)
            @play - Czy zegar ma zostać uruchomiony zaraz po otwarciu okna
            @allow_unselecting - Zezwalanie na odznaczenie karty po ponownym naduszeniu
            @n_and_w - Jeśli ustawione na True, zostanie użyty pewien specjalny tryb losowania przykładów wyłącznie z pośród liczb, a nie z pliku jak w każdym innym przypadku
        """

        #Builder.load_file("kv/cards.kv")

        Screen.__init__(self, **kwargs)

        self.level_number = level_number
        self.level_icon = level_icon
        self.table_name = table_name
        self.allow_unselecting = allow_unselecting

        # Ustawienia siatki kart
        self.card_grid_rows = rows
        self.card_grid_cols = cols

        # Określenie liczby par kart
        self.pairs_total = rows * cols // 2

        # Przygotowanie przykładów
        self._create_examples(self.pairs_total, cards_set, Engine1, Engine2, n_and_w)

        # Przygotowanie zegara
        self.timer.reset_clock()
        if auto_play:
            self.timer.start_clock()

        # Przygotowanie dymku z wiadomoscia
        self.notify_timeout = notify_timeout

    def _create_examples(self, count, cards_set, Engine1, Engine2, numbers_and_words):
        """Wygenerowanie i umieszczenie przykładów do zadania"""

        # Losowe pary karty z zestawu
        if numbers_and_words:
            pairs = CardsPair.get_random_numbers_as_pairs(count, cards_set)
        else:
            pairs = CardsPair.get_random_pairs(count, cards_set)

        # Przygotowanie obiektow kart do zaznaczania
        cards = list(sum([(Engine1(p.cid, p.dsc, p.fst), Engine2(p.cid, p.dsc, p.snd)) for p in pairs], ()))

        # Pomieszanie kart
        shuffle(cards)

        # Dodanie kart do siatki
        for c in cards:
            c.bind(on_release=self.select_card)
            self.card_grid.add_widget(c)

    def select_card(self, card):
        """Obsługa zdarzenia zaznaczenia jakiejś karty"""

        # Sprawdzenie czy zegar był uruchomiony, jeśli nie, to go uruchomienie
        if (self.pairs_guessed < self.pairs_total) and (not self.timer.is_running()):
            self.timer.start_clock()

        # Czy karta znajduje się na liście zaznaczonych?
        if self.allow_unselecting and card in self.current_selected:
            # Odznaczamy ją
            self.current_selected.remove(card)
            card.toggle()

            return

        # Jesli karat była już odgadnięta (albo nie wolno jej odznaczyć)
        if card.guessed or card in self.current_selected:
            return

        else:
            # Odwracam kartę
            card.toggle()

            # Ile już kart siedzi na kupce?
            selected = len(self.current_selected)

            # Jeśli nic nie było, to dodaj
            if selected == 0:
                self.current_selected.append(card)

            # Jeśli była jedna
            elif selected == 1:
                prev = self.current_selected.pop(0)

                # i taka sama jak wcześniej, to oznacz jako odgadnięte i usuń
                if (card.cid == prev.cid) and (card is not prev):
                    card.guessed = True
                    prev.guessed = True

                    # Jenda para więcej
                    self.pairs_guessed += 1
                    # Wyświetlenie balonika
                    self.notify.set_msg(card.dsc, self.notify_timeout)

                else:
                    self.current_selected.append(card)
                    self.current_selected.append(prev)

            # Jeśli były już dwie zaznaczone, to je wywal i dodaj aktualną
            else:

                for c in self.current_selected:
                    c.toggle()

                self.current_selected = [card,]

    def on_pairs_guessed(self, obj, val):
        """Zdarzenie polegające na zmianie ilości odgadniętych par kart"""

        # Jeśli to już wszystkie karty
        if val == self.pairs_total:

            # Zatrzymanie zegara
            self.timer.stop_clock()

            # Pobranie wyniku
            result = self.timer.get_time()

            # Zapis wyniku
            self.save_score(result)

            # Komunikat o zakończeniu gry
            p = ResultInfoPopup(score=result)
            p.bind(on_dismiss=lambda pp: self.back_to_level_choose())

            Clock.schedule_once(lambda dt: p.open(), 1.0)

    def back_to_level_choose(self):
        """Zakończenie zadania i powrót do ekranu wyboru poziomów"""
        self.manager.current = CH_SCREEN

    def save_score(self, res):
        """Zapis zdobytego wyniku do bazy danych"""

        DataBase.insert_score(self.table_name, self.level_number, res)


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
        """
        Uruchomienie cwiczenia na wskazanym poziomie
            
            @options - konfiguracja zadania
                level_number - poziom trudnosci
                rows - liczba wierszy kraty
                cols - liczba kolumn kraty
                cards_set - zbior kart do gry
                level_icon - mala ikonka obrazujaca wybrany poziom trudnosci
                *game_options - inne opcje przyjmowane przez klase `GenericCardGame`
        """

        # Jeśli operacja nie jest zablokowana przez inne przejście SM
        if not self.lock:
            # Blkada
            self.lock = True

            # Jesli było już zadanko to je usuwamy
            if self.exercise and self.sm.has_screen(EX_SCREEN):
                self.sm.remove_widget(self.exercise)

            # <--------------- Tworzymy nowe cwiczenie -----------------
            self.exercise = GenericCardGame(name=EX_SCREEN, **options)

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
        """Reakcja na klawisz ESC wcisniety podczas gry"""
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
        from stats import ScoresPopupContent

        st = Popup(title=u"{t} - Wyniki".format(t=self.name), content=ScoresPopupContent(table_name=self.table_name), size_hint_x=0.8)
        st.open()
        st.content.close_bt.bind(on_release=st.dismiss)
