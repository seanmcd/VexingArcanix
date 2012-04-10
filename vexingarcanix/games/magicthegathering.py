""" A module that holds code specific to the CCG Magic: the Gathering. Decks
    uploaded by users. This and Pokemon are the pilot program, so they're going
    to be getting the most attention.
"""

from vexingarcanix.games.base import Deck, Card, Question

class MTGDeck(Deck):
    """A Magic: the Gathering deck."""

    game_name = u"Magic: the Gathering"
    short_game_name = "magicthegathering"
    max_copies = 4
    opening_hand = 7
    max_copies_exempt = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest', 'Snow-covered Plains', 'Snow-covered Island', 'Snow-covered Swamp', 'Snow-covered Mountain', 'Snow-covered Forest', 'Relentless Rats']

    def __init__(self, decklist, **hints):
        self.decklist = decklist

    def is_legal(self, decklist, format='standard'):
        """ A method that inspects the current deck and returns a list of
            formats in which it's legal to play. Because this requires an
            ongoing maintenance cost as new sets are released, this is
            definitely a feature for version 2.0, not for the MVP.

            This method *will not*: attempt to tell you if that's a legal
            2-Headed Giant deck.  This method *will*: cheat on discerning
            'block' legality by just checking if all of the cards are from the
            same block. Legality: 'Unglued' is the fall-through - if we don't
            recognize all of the cards or if we affirmatively recognize some of
            them as being from the Un-sets, then the only thing it's legal for
            is Un-sets.
        """
        formats = ['standard', 'modern', 'legacy', 'vintage', 'extended', 'block', 'commander', 'unglued', ]

    def land_count(self):
        """ Counts the number of lands in the deck. Even though this is
            something fairly simple, we're likely to use it a lot, so let's
            make it easy to invoke and put it in one place.
        """
        pass

    def basic_land_count(self):
        """ Counts the number of basic lands in the deck. Even though this is
            something fairly simple, we're likely to use it a lot, so let's
            make it easy to invoke and put it in one place.
        """
        basics = [ card for card in self.decklist if card.is_basic_land() ]
        return sum([ land.count for land in basics ])


class MTGCard(Card):
    """ Cards for Magic: the Gathering may have supertypes, types, subtypes,
        etc. Right now we're not keeping careful track of those properties -
        later we'll do a DB lookup during instantiation and figure out
        properties.
    """

    def __init__(self, name, count, **hints):
        # Later we'll use the **hints dict to help disambiguate cards.
        super(MTGCard, self).__init__(name, count)

    def canonical_name(self):
        pass

    def is_basic_land(self):
        basics = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest', 'Snow-covered Plains', 'Snow-covered Island', 'Snow-covered Swamp', 'Snow-covered Mountain', 'Snow-covered Forest']
        if self.name in basics:
            return True
        else:
            return False

    # Later we'll probably prune out things that can be answered just by
    # looking at the type line. For now we'll use these methods.
    def _is_land(self, name):
        raise NotImplementedError

    def _is_creature(self, name):
        raise NotImplementedError

    def _is_spell(self, name):
        raise NotImplementedError

    def _is_permanent(self, name):
        """ It's a permanent if its type is Creature, Land, Enchantment,
            Planeswalker, or Artifact. We don't care about the oddball cases
            like Vanguard, Plane, and Scheme.
        """
        raise NotImplementedError


class MTGQuestion(Question):
    """Questions are important: without them, answers are meaningless."""
    def __init__(self):
        super(MTGQuestion, self).__init__()
        self.question_list = self.generic_questions
        self.question_list += ['basics_count',
                               #'basic_in_next_n',
                               ]

    def basics_count(self, deck):
        question_string = "How many basic lands are in your deck?"
        answer_suffix = "basic lands"
        correct = count = deck.basic_land_count()
        if count < 5:
            possible = range(0, 5)
        else:
            possible = [ x for x in range(count - 2, count + 3)]
        # Possibly it should be:
        # correct, possible = self.gen_wrong(chosen_card.count, 'int')
        # ... but we're still in MVP mode.
        return question_string, correct, possible, answer_suffix, "basic lands"


    def basic_in_next_n(self, deck, depth=None):
        raise NotImplementedError
