# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#

import sqlite3
import datetime
from kivy.logger import Logger

DB_FILE = "db/scores.sqlite"

CARDS_EXERCISE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE DEFAULT CURRENT_TIMESTAMP,
        level INTEGER NOT NULL,
        score INTEGER NOT NULL
    )
"""

INSERT_SCORE_OF_CARDS_GAME_SQL = "INSERT INTO {table} (date, level, score) VALUES ('{date}', {level}, {score})"

GET_BEST_SQL = "SELECT date, min(score) FROM {t} WHERE level={l}"

GET_RECENT_SQL = "SELECT date, score FROM {t} WHERE level={l} ORDER BY date DESC LIMIT {c}"


class ResultEntry():
    """Klasa reprezentująca pojedyńczy wpis wyniku z tabeli"""

    NO_RESULT = "---"

    def __init__(self, dt, sc):
        """
            dt - data i czas
            sc - wynik w sekundach
            valid - flaga, czy poprzednie dane są prawdziwe. Jeśli False, wszystkie pola wyniku zostaną ustawione na NO_RESULT
        """
        if dt is None:
            self.date = self.NO_RESULT
            self.time = self.NO_RESULT
        else:
            # Przetworzenie daty
            dtime = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

            # Wyłuskanie potrzebnych pól
            self.date = dtime.date().isoformat()
            self.time = dtime.time().strftime("%H:%M")

        if sc is None:
            self.score = self.NO_RESULT

        else:
            self.score = self._convert_to_clock(sc)

    def _convert_to_clock(self, sc):
        """Konwersja liczby sekund do takiego napisu, jaki się wyświetla na zegarku cyfrowym"""
        return "{m:>02}:{s:>02}".format(m=sc // 60, s=sc % 60)


class DataBase():
    """Obsługa bazy danych"""

    @classmethod
    def create_card_game_table(self, table):
        """Wstawienie tabeli do bazy, o ile jeszcze jej nie było"""

        try:
            # Nawiązanie połączenia
            conn = sqlite3.connect(DB_FILE)

            c = conn.cursor()
            c.execute(CARDS_EXERCISE_TABLE_SQL.format(table_name=table))

            conn.commit()
            conn.close()

        except Exception as e:
            Logger.debug(e.message)

    @classmethod
    def insert_score(self, table, level, score):
        """
        Umieszczenie wyniku w bazie

        Parametry:
            @table - nazwa tabeli do której nastąpi wstawianie wyniku
            @level - numer poziomu na którym odbyła się gra (1, 2 lub 3)
            @score - wynik uzyskany z gry
        """

        try:
            # Nawiązanie połączenia
            conn = sqlite3.connect(DB_FILE)

            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            c = conn.cursor()
            c.execute(INSERT_SCORE_OF_CARDS_GAME_SQL.format(table=table, date=now, level=level, score=score))

            conn.commit()
            conn.close()

        except Exception as e:
            Logger.debug(e.message)

    @classmethod
    def get_best_score(self, table, lvl):
        """Pobranie z bazy najlepszych wyników dla każdego lewelu"""

        # Nawiązanie połączenia
        conn = sqlite3.connect(DB_FILE)

        c = conn.cursor()

        # Pobranie rezultatu z bazy
        b = c.execute(GET_BEST_SQL.format(t=table, l=lvl)).fetchone()

        conn.close()

        # Zwrocenie wyników
        return ResultEntry(b[0], b[1])

    @classmethod
    def get_recent_scores(self, table, lvl, count):
        """
        Pobranie kilku ostatnich wynikow gry na zadanym poziomie

        Parametry
            @table - tabela z danymi z danej gry
            @lvl - poziom trudnosci gry
            @count - liczba ostatnich wpisow
        """

        # Nawiązanie połączenia
        conn = sqlite3.connect(DB_FILE)

        c = conn.cursor()

        # Odpytanie bazy
        r = c.execute(GET_RECENT_SQL.format(t=table, l=lvl, c=count)).fetchall()

        conn.close()

        # Zwrocenie wynikow, rozdmuchanych jeśli trzeba do odpowiedniej długości
        return [ResultEntry(r[0], r[1]) for r in r] + [ResultEntry(None, None) for i in range(count - len(r))]

