""" Deck, Card, and Question classes for the CCG "Legend of the Five Rings".
    As with Magic and Pokemon, users hand us deck lists, but the wrinkle this
    time is that they have two deck lists - Fate Deck and Dynasty Deck. So
    we'll definitely have to be clever in the Deck.is_legal() method to cope
    with that.
"""

from vexingarcanix.games.base import Deck, Card, Question

class L5RDeck(Deck):
    """deck"""

    game_name = u"Legend of the Five Rings"
    short_game_name = "l5r"
    max_copies = 3
    opening_hand = 7

    def __init__(self, decklist):
        self.decklist = decklist

    # Remember when we implement a validate_deck() method that we'll have to
    # take Unique cards into account, and deal with the having-two-decks deal.

class L5RCard(Card):
    """card"""
    def __init__(self, name, count, **hints):
        # Later we'll use the **hints dict to help disambiguate cards.
        super(L5RCard, self).__init__(name, count)


class L5RQuestion(Question):
    """question"""
    pass
