""" Deck, Card, and Question classes for the CCG "Legend of the Five Rings".
    As with Magic and Pokemon, users hand us deck lists, but the wrinkle this
    time is that they have two deck lists - Fate Deck and Dynasty Deck. So
    we'll definitely have to be clever in the Deck.is_legal() method to cope
    with that.
"""

from vexingarcanix.lib.abstracts import Deck, Card, Question

class L5RDeck(Deck):
    """deck"""
    def __init__(self, decklist):
        self.decklist = decklist
        self.short_game_name = "l5r"
        self.max_copies = 3
        self.opening_hand = 7

    game_name = u"Legend of the Five Rings"


class L5RCard(Card):
    """card"""
    def __init__(self, name, count, **hints):
        # Later we'll use the **hints dict to help disambiguate cards.
        super(L5RCard, self).__init__(name, count)


class L5RQuestion(Question):
    """question"""
    pass
