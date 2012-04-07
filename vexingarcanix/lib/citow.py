""" Deck, Card, and Question clases for working with Chaos in the Old World
    games. Fixed deck lists, but there are several of them because there are
    several player roles. The MVP version of this particular functionality:
    pick a deck, then ask how likely it is that you get _zero_ copies of a
    given card in your opening hand.

    Tricky thing: drawing two cards at once is the normal draw-for-turn, except
    for Tzeentch, who draws 'til there are five in hand and may pitch a card
    before drawing.
"""

from vexingarcanix.lib.abstracts import Deck, Card, Question

class CITOWDeck(Deck):
    """deck"""
    def __init__(self, decklist):
        self.decklist = decklist
        self.short_game_name = "citow"
        self.opening_hand = 5

    game_name = u"Legend of the Five Rings"


class CITOWCard(Card):
    """card"""
    def __init__(self, name, count, **hints):
        # Later we'll use the **hints dict to help disambiguate cards.
        super(CITOWCard, self).__init__(name, count)


class CITOWQuestion(Question):
    """question"""
    pass
