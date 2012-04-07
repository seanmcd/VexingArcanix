""" Deck, Card, and Question classes for working with the board game "Race for
    the Galaxy". Fixed deck list, mostly singletons. The MVP version of this
    particular functionality: ask questions about how likely you are to get a
    given 6-point Development.

    Tricky things about this game: the six-pitch-two starting hands, the
    two-pitch-one start worlds. When constructing a game state for a question,
    keep those in mind.
"""

from vexingarcanix.lib.abstracts import Deck, Card, Question

class RFTGDeck(Deck):
    """deck"""
    def __init__(self, decklist):
        self.decklist = decklist
        self.short_game_name = "citow"
        self.opening_hand = 6

    game_name = u"Race for the Galaxy"


class RFTGCard(Card):
    """card"""
    def __init__(self, name, count, **hints):
        # Later we'll use the **hints dict to help disambiguate cards.
        super(RFTGCard, self).__init__(name, count)


class RFTGQuestion(Question):
    """question"""
    pass
