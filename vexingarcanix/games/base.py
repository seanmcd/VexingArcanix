""" This module holds abstract classes that game-specific classes will inherit
    from: Deck, Card, and Question. These objects are not, strictly speaking,
    abstract, because you can instantiate them and they'll function, but
    they're what our game-specific classes inherit from so that they can ask
    questions that are about a specific game, not just about a list of generic
    cards.
"""

import random, re
from scipy.stats import hypergeom
# import itertools, math, numpy


class Deck(object):
    """ A Deck object represents the set of cards that the application is
        currently thinking about. Feed Deck objects to instances of Question to
        give the Question instance the information it needs to generate a question
        about that deck.
    """

    def __init__(self, decklist):
        """ Need to pass a list of Card objects in. The deck should also know
            what game it's for. That information belongs with the deck since a
            deck will be made up of cards from just one game.

            Also, a deck for a given game should be able to tell you whether
            it's a legal deck for a given format in that game - however, this
            is for subclasses to implement.
        """
        self.decklist = decklist
        # Since Card implements __str__(), `print self.decklist` is a
        # good-enough string representation of the deck.  Note that decks
        # should assert that count > 0 for all cards in the full deck. What
        # kind of validation do we want to do?
        self.short_game_name = None
        self.game_max_copies = 0
        self.game_max_copies_exempt = []

    game_name = None

    def size(self):
        # How many cards are in the deck? (usually 60)
        return sum([ card.count for card in self.decklist ])

    def unique_cards(self, decklist):
        # How many *distinct* cards in the deck? Remember special cases like
        # DFCs/werewolves in Magic, same-name-different-abilities Pokemon
        # cards, and Soul Of in L5R! This can be tricky, so just `return
        # len(decklist)` isn't good enough.
        raise NotImplementedError

    def is_legal(self, format):
        # Various formats, various games, but we should be able to determine
        # this with a few DB queries. Unique by game.
        raise NotImplementedError


class Card(object):
    """Each *distinct* card in a deck is represented by a Card object - how
    many copies of that card are in the deck, is stored in the `count` property
    of the Card instance. Cards have a .count property because we're not
    interested in them outside the context of a deck. (?) """
    def __init__(self, name, count):
        self.name = name
        self.count = int(count)

    def __str__(self):
        """A basic representation of the card."""
        return "{} copies of a card named {}".format(self.count, self.name)

    def canonical_name(self, name):
        """Use this to do things like strip off EX at the end of the name, turn
        'Bob' into 'Dark Confidant', etc. """
        raise NotImplementedError

    def rules_text(self, name):
        raise NotImplementedError


class Question(object):
    """ A class that generates questions when we don't know any of the
        semantics of the game, and which indicates that the deck we're
        currently working with is for a game we don't know. Individual games
        subclass Question so they can grind out questions specific to that
        game. The superclass also holds the methods that let a Question
        instance introspect on itself and generate a question for the user to
        answer. Ideally we'd use a registery/decorator for this so that there's
        a list that automatically gets populated with questions, but
        implementing that would be very time-consuming - so we're doing it the
        dumb way for now.
    """

    def __init__(self):
        self.generic_questions = [
            'copies_in_full_deck',
            'copies_in_opening_hand',
            # 'copies_in_top_five',
            # 'draws_until_copy',
            ]
        self.question_list = [] + self.generic_questions

    def choose_question(self):
        question = random.choice(self.question_list)
        return getattr(self, question)

    def copies_in_full_deck(self, deck):
        # FUTURE: give it the ability to pick a card that's _not_ in your deck
        # so '0' is the right answer. Maybe make that a separate question.
        question_string = "How many copies of {card} are in your deck?"
        answer_suffix = "copies"
        chosen_card = random.choice(deck.decklist)
        correct = count = chosen_card.count
        if count < 5:
            possible = range(0, 5)
        else:
            possible = [ x for x in range(count - 2, count + 3)]
        # Possibly it should be:
        # correct, possible = self.gen_wrong(chosen_card.count, 'int')
        # ... but we're still in MVP mode.
        return question_string.format(card=chosen_card.name), correct, possible, answer_suffix, chosen_card

    def copies_in_opening_hand(self, deck):
        question_string = "How likely is it that at least one copy of {card} will be in your opening hand?"
        answer_suffix = 'percent'
        chosen_card = random.choice(deck.decklist)
        copies = chosen_card.count
        deck_size = sum([ c.count for c in deck.decklist ])
        hand_size = 7

        opening_hand_chance = hypergeom.sf(1, deck_size, copies, hand_size)
        correct = opening_hand_chance = round(opening_hand_chance, 4) * 100
        # Consult docs or Stack Overflow: what's that first parameter mean
        # again? Thank goodness I gave the rest meaningful variable names.
        # http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypergeom.html

        wrongs = [ round(self.gen_wrong(x, 'float', variance=2.0), 2) for x in [1.2, 2.0, 6.0, 16.0] ]
        possible = wrongs + [opening_hand_chance]
        random.shuffle(possible)

        print "Chance of a copy of {} in opening hand: {}".format(chosen_card.name, str(opening_hand_chance))
        return question_string.format(card=chosen_card.name), correct, possible, answer_suffix, chosen_card

    def average_draws_until_copy(self, deck):
        """ Our new flagbearer hard question.
        """
        question_string = "If your opening hand contains zero copies of {card}, how many cards do you have to draw in order to have at least a 90 percent chance that a copy of {card} is among them?"
        chosen_card = random.choice(deck.decklist)
        answer_suffix = 'cards'
        raise NotImplementedError

    def copies_in_top_five(self, deck):
        """ Another difficult question - but also somewhat difficult to code,
            since it requires that we pick a bunch of cards that have already
            left the deck. Well, it would require that for the serious
            version. For this version - just use a scalar!
        """
        question_string = "After drawing your opening hand with one copy of {card}, how likely is it that another copy of {card} is in the top five cards of your deck?"
        # That's another reason why we don't choose a card earlier: we might be
        # interested in a card with a specific quality.
        chosen_card = random.choice([ card for cards in deck.decklist if card.count > 1 ])
        remaining_copies = chosen_card.count - 1
        remaining_deck = sum([c.count for c in deck.decklist]) - 7

        in_top_five_cards_chance = hypergeom.sf(1, remaining_deck, remaining_copies, 5)
        raise NotImplementedError

    def gen_wrong(self, correct, flavor, **kwargs):
        """ For example, 'how many copies of this card are left in your deck?'
            needs to give different wrong answers than 'what are the odds that
            this card is in the top 2 cards of your deck?', and neither is
            quite the same as 'how likely is it that two copies of this card
            start the game as Prizes?'
        """
        if flavor is 'int':
            pass
        if flavor is 'float':
            return self._gen_wrong_float(correct, kwargs.get('variance', 2.0))
        if flavor is 'string':
            pass
        raise NotImplementedError

    def _gen_wrong_float(self, correct, variance=2.0):
        """ Expects floats `correct` and `variance`. Returns a float, rounded
            to two digits, that is guaranteed to not be equal to `correct`, and
            whose magnitude will be between 0.00 and `variance` times
            `correct`.
        """
        wrong = round(random.uniform(0, round(correct*variance, 4)), 4)
        while wrong > 1:
            wrong /= 10.0
        wrong = wrong * 100
        if wrong == round(correct, 2):
            wrong = self._gen_wrong_float(correct, variance)
        return wrong
