# -*- coding: utf-8 -*-
#
#  Copyright 2014 Piotr Skonieczka <skoczek@mat.umk.pl>
#

from kivy.logger import Logger
from random import sample
from core import parse_word, number_2_word


class CardsPair():
    """Podstawowa definicja pary kart"""

    def __init__(self, cid, fst, snd, dsc=None):
        """
            @cid - identyfikator pary
            @fst - element znajdujacy sie na przedzie karty
            @snd - element znajdujacy sie na odwrocie
            @dsc - opcjonalny komunikat, ktory bedzie wyswietlany w dymku po dopasowaniu pary
        """
        self.cid = cid
        self.fst = fst
        self.snd = snd
        self.dsc = parse_word(dsc)

    @staticmethod
    def get_random_pairs(count, index_file):
        """
        Procedura zwraca określoną ilość losowo wybranych obeiktów typu CardsPair z kolekcji znajdującej się
        w pliku @index_file
            @count - oczekiwana liczba losowych kart
            @index_file - plik zawierajacy parametry kart
        """

        try:
            with open(index_file, "r") as index:

                # Wczytanie i zainicjowanie listy wszystkich znanych par kart
                cards = [CardsPair(i, *line.split(';')) for i, line in enumerate(index.readlines())]

                # Wybranie losowo `count` elementow
                return sample(cards, count)

        # Jesli z jakis powodow nie udalo sie wygenreowac odpowiedniej ilosci par, to zwracamy - nic
        except Exception as e:
            Logger.debug(e.message)
            return []

    @staticmethod
    def get_random_numbers_as_pairs(count, nrange):
        """
        Procedura zwraca określoną ilość losowo wybranych liczb z podanego zakresu i tworzy z nich obiekty CardsPair
        zawierające te właśnie liczby oraz ich reprezentację słowną
            @count - zadana liczba losowych kart
            @nrange - zakres losowania
        """

        # Wylosowanie zadanej liczby przykladow
        samples = sample(nrange, count)

        # Zwrocenie ich w postaci CardsPair
        return [CardsPair(i, str(i), number_2_word(i), "") for i in samples]
