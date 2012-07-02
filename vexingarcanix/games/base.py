# -*- coding: utf-8 -*-
""" This module holds base classes that game-specific classes will inherit
    from: Deck, Card, and Question. These objects are 'base' instead of
    'abstract' because you can instantiate them and they'll function as
    representations of a generic game using decks of cards. Their main purpose
    is to give our game-specific classes a starting point from which they build
    game-specific data structures and questions.
"""

import copy, operator, random, re
from scipy.stats import hypergeom, mode
from numpy import median

class Deck(object):
    """ A Deck object represents the set of cards that the application is
        currently thinking about. Feed Deck objects to instances of Question to
        give the Question instance the information it needs to generate a question
        about that deck.
    """

    def __init__(self, decklist):
        """ To initialize, caller needs to pass a list of Card objects. The
            deck should also know what game it's for. That information belongs
            with the deck since a deck will be made up of cards from just one
            game. A deck for a given game should be able to tell you whether
            it's a legal deck for a given format in that game - however, that
            function is strictly for subclasses to implement.
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

    def mode_copies(self):
        # The mode of a list of numbers is the number most frequently
        # occurring in that list. Note that SciPy's mode() returns the
        # smallest such number in the case of a tie.
        return int(mode([ card.count for card in self.decklist ])[0][0])

    def median_copies(self):
        return int(median([ card.count for card in self.decklist ]))

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

        Question-generating methods should take as arguments only a Deck object
        and **kwargs, and should return a tuple of the form (string
        representation of question, correct answer, list of answers to choose
        from, a string to append to answers, Card object for the primary card
        that the question is about). Later we may want to modify or change that
        last item to a string, because we'll be asking about things like "basic
        lands" or "Psychic Pokemon" instead of a specific card.
    """

    def __init__(self):
        self.generic_questions = [
            'copies_in_full_deck',
            'copies_in_opening_hand',
            'copies_in_top_five',
            'most_likely_top_card',
            # 'draws_until_copy',
            ]
        self.question_list = [] + self.generic_questions

    def choose_question(self):
        question = random.choice(self.question_list)
        print "chosen question: {}".format(question)
        return getattr(self, question)

    def copies_in_full_deck(self, deck):
        # FUTURE: For specific games, the hard version of this question will
        # have the ability to pick a card that's _not_ in your deck, leading to
        # a situation where '0' is the correct answer.
        question_string = "How many copies of {card} are in your deck?"
        answer_suffix = "copies"
        chosen_card = random.choice(deck.decklist)
        correct = chosen_card.count
        possible = self.gen_wrong(correct, 'int', 4, mode=deck.mode_copies(), median=deck.median_copies())
        possible.append(correct)
        random.shuffle(possible)
        return question_string.format(card=chosen_card.name), correct, possible, answer_suffix, chosen_card

    def copies_in_opening_hand(self, deck, hand_size=7):
        question_string = ("How likely is it that at least one copy of {card} "
                           "will be in your opening hand?")
        answer_suffix = 'percent'
        chosen_card = random.choice(deck.decklist)
        copies = chosen_card.count
        # TODO: replace with Deck object's .size property.
        deck_size = sum([ c.count for c in deck.decklist ])

        opening_hand_chance = hypergeom.sf(1, deck_size, copies, hand_size)
        # Consult docs or Stack Overflow: what's that first parameter mean
        # again? Thank goodness I gave the rest meaningful variable names.
        # http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.hypergeom.html
        # See also: http://stackoverflow.com/q/11286430/244494

        opening_hand_chance = opening_hand_chance * 100
        correct_string = "{:.2f}".format(opening_hand_chance)

        wrongs = self.gen_wrong(opening_hand_chance, 'percent', 4)
        possible = wrongs + [correct_string]
        random.shuffle(possible)

        print "Chance of a copy of {} in opening hand: {}".format(chosen_card.name, correct_string)
        return question_string.format(card=chosen_card.name), correct_string, possible, answer_suffix, chosen_card

    def copies_in_top_five(self, deck):
        """ Another difficult question - but also somewhat difficult to code,
            since it requires that we pick a bunch of cards that have already
            left the deck. Well, it would require that for the serious
            version. For this version - just use a scalar! "copies in top N"
            can come later.
        """
        question_string = ("After drawing your 7-card opening hand with one "
                           "copy of {card}, how likely is it that at least "
                           "one more copy of {card} is in the top five cards "
                           "of your deck?")
        answer_suffix = 'percent'
        chosen_card = random.choice([ card for card in deck.decklist if card.count > 1 ])
        remaining_copies = chosen_card.count - 1
        remaining_deck = sum([c.count for c in deck.decklist]) - 7
        in_top_five_chance = hypergeom.sf(1, remaining_deck, remaining_copies, 5)
        in_top_five_chance = in_top_five_chance * 100
        correct_string = "{:.2f}".format(in_top_five_chance)
        wrongs = self.gen_wrong(in_top_five_chance, 'percent', 4)
        possible = wrongs + [correct_string]
        random.shuffle(possible)

        print "Chance of a copy of {} in the next five cards: {}".format(chosen_card.name, correct_string)
        return question_string.format(card=chosen_card.name), correct_string, possible, answer_suffix, chosen_card

    def average_draws_until_copy(self, deck, opening_hand=7):
        """ This will, once implemented, be our new flagbearer hard question -
            it's also the one that requires the most semantic deck knowledge of the
            generic questions. Which is to say, "any."
        """
        question_string = ("If your opening hand contains zero copies of "
                           "{card}, how many cards do you have to draw in order "
                           "to have at least a 90 percent chance that a copy of "
                           "{card} is among them?")
        chosen_card = random.choice(deck.decklist)
        answer_suffix = 'cards'
        raise NotImplementedError

    def most_likely_top_card(self, deck):
        """ A medium-difficulty question - removes 10-20 random cards from your
            deck, then asks which of four options the top card of your deck is
            most likely to be. Should be useful to most games, and it's easy to
            implement in a game-agnostic way, so it's here instead of in
            game-specific code.

            KNOWN BUG: will break on decks with too few unique cards or where
            too few cards have at least 2 copies in the deck. However, still
            works on 95% of MTG/Pokemon decks.
        """
        question_string = ("If {}have been removed from your deck, which of "
                           "the following cards is most likely to be the top "
                           "card of your deck?")
        answer_suffix = "is most likely to be the top card"
        reduced_deck = copy.deepcopy(deck)

        cards_to_remove = random.choice(range(10,21))
        print "Chose to remove {} cards".format(cards_to_remove)
        removed_cards = {}
        # TODO: Many questions are going to want to remove cards from the deck:
        #       this chunk should probably be pulled out into its own function
        #       so it can be easily re-used.
        while sum([ removed_cards[key] for key in removed_cards.keys() ]) < cards_to_remove:
            drawn_card = random.choice([ card for card in reduced_deck.decklist if card.count > 1 ])
            print "Removed a copy of {} from the deck.".format(drawn_card.name)
            drawn_card.count -= 1
            print "{} cards remain in the deck.".format(sum([ card.count for card in reduced_deck.decklist ]))
            # if the card is in the group we've already removed, just
            # increment, otherwise add to that set.
            if drawn_card.name in [ c for c in removed_cards.keys()]:
                removed_cards[drawn_card.name] += 1
            else:
                removed_cards[drawn_card.name] = 1
        print "Removed: {}".format(removed_cards)
        # TODO: replace with Deck object's .size property.
        reduced_deck_size = sum([ card.count for card in reduced_deck.decklist ])

        removed_cards_string = ""
        for key in removed_cards.keys():
            c = removed_cards.pop(key)
            copy_plural = "copies" if c > 1 else "copy"
            if len(removed_cards.keys()) == 0:
                removed_cards_string += "and "
            removed_cards_string += "{0} {1} of {2}, ".format(c, copy_plural, key)
        print removed_cards_string
        print question_string.format(removed_cards_string)

        choices = 4
        chosen_cards = []
        print "The deck is now: {}".format(reduced_deck.decklist)
        while len(chosen_cards) < choices:
            # TODO: Rewrite this with list.pop() so that we don't just pull the
            # same thing over and over?
            this_card = random.choice(reduced_deck.decklist)
            print "Chose: {}".format(this_card.name)
            # Second test is so that we don't have to deal with ties - however,
            # now we just have to make sure that there are at least 4 different
            # card counts remaining in the deck, which should be the norm - but
            # it's not guaranteed!
            if (this_card not in chosen_cards) and (this_card.count not in [ card.count for card in chosen_cards ]):
                chosen_cards.append(this_card)
                print "List now contains: {}".format([ card.name for card in chosen_cards ])

        card_odds_pairings = []
        for card in chosen_cards:
            # top_card_odds = hypergeom.sf(1, reduced_deck_size, card.count, 1)
            top_card_odds = card.count / float(reduced_deck_size)
            card_odds_pairings.append((top_card_odds, card.name))
        sorted_odds_pairings = sorted(card_odds_pairings, key=operator.itemgetter(0))
        print "Cards with odds: {}".format(sorted_odds_pairings)

        question_string = question_string.format(removed_cards_string)
        correct = sorted_odds_pairings[-1][1]
        # No need to shuffle: this list is already in a random order!
        possible = [ card[1] for card in card_odds_pairings]

        return question_string, correct, possible, answer_suffix, "the top card of your deck"

    def gen_wrong(self, correct, flavor, count=1, **kwargs):
        """ A function that generates wrong answers for methods of Question
            objects. This is a wrapper function that abstracts out the
            operation of functions that generate specific flavors of wrong
            answer. Requires as arguments:

            * The correct answer
            * The type of wrong answer desired (int or percent)
            * How many wrong answers the caller needs
            * The largest plausible answer to the question
            * Keyword arguments to be passed to the specific function

            It returns a list of wrong (i.e. guaranteed to not be equal to the
            correct answer) answers that meet the caller's criteria.

            This function exists so that question-asking methods can have a
            uniform sort of interface, but actually generate the appropriate
            kind of wrong answers for the semantic content of the question. For
            example, 'how many copies of this card are left in your deck?'
            needs to give different wrong answers than 'what are the odds that
            this card is in the top 2 cards of your deck?', and neither is
            quite the same as 'how likely is it that two copies of this card
            start the game as Prizes?'
        """
        wrongness_validator = None
        wrongness_generator = None
        if flavor is 'percent':
            wrongness_generator = self._gen_wrong_percent
            wrongness_validator = self._validate_wrong_percent
        if flavor is 'int':
            wrongness_generator = self._gen_wrong_int
            wrongness_validator = self._validate_wrong_int
        if not wrongness_validator or not wrongness_generator:
            raise NotImplementedError

        generated_answers = []
        while len(generated_answers) < count:
            candidate = wrongness_generator(correct, **kwargs)
            viable = wrongness_validator(candidate, correct, **kwargs)
            if viable and (candidate not in generated_answers):
                generated_answers.append(viable)
        return generated_answers

    def _gen_wrong_percent(self, correct, **kwargs):
        """ Generate a wrong answer for "how likely is it" questions, which
            need a 0-100 percentage as an answer. This function requires that
            the 'correct' parameter already be a float in the 0-100 range."""
        # Lower variance will make the question harder - it's a kwarg instead
        # of a required parameter so that it's easier on our callers.
        variance = kwargs.get('variance', 3.0)
        # If the correct answer is a very small percentage or a very large one,
        # the 'variance' parameter doesn't work right, so we constrain the
        # possibility space a bit.
        top = max(correct * variance, 10.0)
        bottom = max(correct / variance, 1.0)
        candidate = random.uniform(bottom, top)
        return candidate

    def _validate_wrong_percent(self, candidate, correct, **kwargs):
        """ Scrutinize a wrong answer and return its string representation if
            it's acceptable, or None if it's unacceptable. String
            representation truncates to 2 decimal places so that it's
            human-readable (and avoids problems with the limits of
            floating-point precision). """
        if candidate > 100.0 or candidate < 0.01:
            return None
        # Eliminate wrong answers that make the question too hard.
        if (candidate > correct - 1.0) and (candidate < correct + 1.0):
            # This also covers the candidate == correct case.
            return None
        return "{:.2f}".format(candidate)

    def _gen_wrong_int(self, correct, **kwargs):
        # This function should know that if you pass a 'mode' argument, that
        # the mode is relevant - how does it use that information? Should it be
        # 'biased' towards picking something close to the mode?
        mode = kwargs.get('mode', None)
        variance = kwargs.get('variance', 2)
        answer_ceiling = kwargs.get('answer_ceiling', None)
        if answer_ceiling:
            top = max(correct * variance, answer_ceiling)
        else:
            top = correct * variance
        bottom = max(1, correct / variance)
        candidate = random.choice(range(bottom, top))
        return candidate

    def _validate_wrong_int(self, candidate, correct, **kwargs):
        """ Takes a wrong answer, considers whether it's suitable, returns the
            string representation of the 'candidate' parameter if so, otherwise
            returns None."""
        if candidate == correct:
            return None
        answer_ceiling = kwargs.get('answer_ceiling', None)
        if answer_ceiling and (candidate > answer_ceiling):
            return None
        return candidate
