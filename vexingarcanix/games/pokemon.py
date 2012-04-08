""" A module that holds code specific to the Pokemon CCG. Variable decks,
    user-entered, lots of special cases with funky names. Annoying
    canonicalization issues - there's a card whose canonical name is a single
    letter (N), and cards whose canonical name starts with a lower case delta
    (i.e. backslash-u 03b4).
"""

import re
from vexingarcanix.games.base import Deck, Card, Question

class PokemonDeck(Deck):
    def __init__(self, decklist, **kwargs):
        super().__init__(decklist)
        self.short_game_name = "pokemon"
        self.max_copies = 4
        self.opening_hand = 7
        self.max_copies_exempt = ['Darkness Energy','Fighting Energy','Fire Energy','Grass Energy','Lightning Energy','Metal Energy','Psychic Energy', 'Water Energy', 'Arceus']

    game_name = u"Pok\xe9mon"

    def is_legal(self, format='standard'):
        """Should only be mildly tricky."""
        formats = ['standard', 'unlimited', ]


class PokemonCard(Card):
    def __init__(self, name, count, **hints):
        # Later we'll use the **hints dict to help disambiguate cards.
        super(PokemonCard, self).__init__(name, count)
        # self.is_energy = None

    def canonical_name(self, name):
        # Make sure the name that we're using is the name that the official
        # game knows, not the string the user typed in - we scrutinize the
        # latter to pick the former from our existing list.
        pass

    def _is_energy(self, name):
        oddball_energy = [r'Double Rainbow Energy', r'Dark Metal Energy', r'Holon Energy [A-Z]{1,2}',]
        # What the fuck Pokemon, you have serious canonicalization issues.
        delta_energy = [u'\u03b4 .+ Energy',]
        generic_energy = r'[a-zA-Z]+ Energy'
        re.match(name, '')

    def _is_basic_energy(self, name):
        basics = ['Darkness Energy','Fighting Energy','Fire Energy','Grass Energy','Lightning Energy','Metal Energy','Psychic Energy', 'Water Energy',]
        if name in basics:
            return True
        return False

    def _is_basic_pokemon(self, name):
        pass

    def _is_trainer(self, name):
        pass

    def _is_supporter(self, name):
        pass


class PokemonQuestion(Question):
    def __init__(self):
        super(PokemonQuestion, self).__init__()
        self.question_list = self.generic_questions

    def basic_energy_in_opening(self, deck):
        """ On average, how many basic Energy cards will be in your opening
            hand?"""
        raise NotImplementedError

    def this_basic_alone(self, deck):
        """ How likely is it that you'll get $basic as the only Pokemon in your
            starting hand? (including multiple copies of it?)  Alternative
            phrasing: How likely is it that the only basics in your opening
            hand will be one or more copies of $basic?"""
        raise NotImplementedError
