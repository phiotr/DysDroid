# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#  

from kivy.adapters.dictadapter import DictAdapter
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, StringProperty

from kivy.uix.listview import CompositeListItem, ListView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.utils import get_color_from_hex

from database import DataBase, ResultEntry


RECENT_COUNT = 15
DEFAULT_FONT = "DroidSans"


class InfoLabel(Label):
    pass


class HeaderLabel(Label):
    """Naglowek tabeli"""
    pass


class RowLabel(Label):
    """Wiersz tabeli"""

    # Numer wiersza
    i = NumericProperty(1)

    def __init__(self, i, **kwargs):
        super(RowLabel, self).__init__(**kwargs)
        self.i = i


class BestScoreLabel(Label):
    """Etykieta najelszego uzyskanego wyniku dla danego stopnia trudnosci"""
    date = StringProperty()
    time = StringProperty()
    score = StringProperty()

    def __init__(self, best, **kwargs):
        Label.__init__(self, **kwargs)

        self.date = best.date
        self.time = best.time
        self.score = best.score


class LevelTab(TabbedPanelItem):
    """Jedna zakladka - jeden stopien trudnosci"""
    
    def __init__(self, nr, table, **kwargs):
        TabbedPanelItem.__init__(self, **kwargs)

        self.text = "Poziom {n}".format(n=nr)

        # Layout
        box = BoxLayout(orientation="vertical")
        self.add_widget(box)

        # Elementy
        box.add_widget(InfoLabel(text="Najlepszy wynik:", size_hint_y=0.1, font_name=DEFAULT_FONT))
        box.add_widget(BestScoreLabel(best=DataBase.get_best_score(table, nr), size_hint_y=0.3))
        box.add_widget(InfoLabel(text="Ostatnich {c}:".format(c=RECENT_COUNT), size_hint_y=0.1, font_name=DEFAULT_FONT))

        th = BoxLayout(orientation="horizontal", size_hint_y=0.15, spacing=1)

        th.add_widget(HeaderLabel(text="Data", size_hint_x=0.3))
        th.add_widget(HeaderLabel(text="Godzina", size_hint_x=0.3))
        th.add_widget(HeaderLabel(text="Uzyskany wynik"))

        box.add_widget(th)

        converter = lambda row_index, row: {
                    'size_hint_y': None,
                    'height': 40,
                    'cls_dicts': [
                        {'cls': RowLabel, 'kwargs': {'i': row_index, 'text': row.date, 'size_hint_x': 0.3} },
                        {'cls': RowLabel, 'kwargs': {'i': row_index, 'text': row.time, 'size_hint_x': 0.3} },
                        {'cls': RowLabel, 'kwargs': {'i': row_index, 'text': row.score, 'font_size': 20} },
                    ]
                }
        adapter = DictAdapter(
                    sorted_keys=range(RECENT_COUNT + 1),
                    args_converter=converter,
                    data={i: r for i, r in enumerate(DataBase.get_recent_scores(table, nr, RECENT_COUNT))},
                    cls=CompositeListItem
                    )

        box.add_widget(ListView(adapter=adapter))


class ScoresPopupContent(BoxLayout):
    """Element `content` dla obiektu Popup"""
    
    close_bt = ObjectProperty(None)
    tab_area = ObjectProperty(None)

    def __init__(self, table_name, **kwargs):

        Builder.load_file("kv/stats.kv")

        BoxLayout.__init__(self, **kwargs)
        self.orientation = "vertical"

        # Zbudowanie obszaru zakładek
        self.level1 = LevelTab(nr=1, table=table_name)
        self.level2 = LevelTab(nr=2, table=table_name)
        self.level3 = LevelTab(nr=3, table=table_name)

        self.tab_area = TabbedPanel(default_tab=self.level1, do_default_tab=False, tab_pos="top_mid", tab_height=50, tab_width=Window.width * 0.8 // 3 - 10)

        self.tab_area.add_widget(self.level1)
        self.tab_area.add_widget(self.level2)
        self.tab_area.add_widget(self.level3)

        self.close_bt = Button(text="Zamknij", size_hint_y=0.1)

        self.add_widget(self.tab_area)
        self.add_widget(self.close_bt)
