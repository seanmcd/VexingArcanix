"""
Everything needed for the Minimum Viable Product version of Vexing Arcanix goes
in here, architecture be damned. It needs to all be in one file so that I'll
actually write it instead of doing digital nest-feathering. I will write things
with nicely organized classes and methods, but I will write them all in this
file for now, because it's important to actually write them.
"""

import itertools, math, numpy, random, re
from scipy.stats import hypergeom

class Card(object):
    """Cards have names and text. Cards for specific games subclass from this
    and have more specific attributes."""
    pass

class MTGCard(Card):
    """Cards for Magic: the Gathering may have supertypes, types, subtypes, etc."""
    def __init__(**kwargs):
        # For each argument in **kwargs, set the attribute of the card equal to
        # the value of the kwarg, if we have an attribute with that name.
        pass

class Deck(object):
    """Decks have attached dictionaries of the form

    {$cardname: ($cardname, $count), $cardname: ($cardname, $count), ... }

    and will later have other properties as well, possibly defined by
    subclassing (e.g. an MTGDeck should know the {super-,sub-,}types of the
    cards in it, and a deck for a given game should be able to tell you whether
    it's a legal deck for a given format in that game.
    """
    pass

def generate_question(current_deck):
    """
    Okay, this is interesting and tricky. To generate a question, we need to
    know what kind of deck we're being asked about, to know the contents of the
    deck, and (LATER) to know a question difficulty level.

    This therefore takes a Deck object as an argument, and spits out a
    dictionary that wait this is hard okay. The answers need to stay on the
    server. So generating a question, generates a DB row? That leads to having
    a DB table that expands without bound. D: Yikes! Maybe we can avoid
    that. But in the long term, we'd like to collect some data about which
    questions are actually hard for people to answer vs. which are easy, so
    we'll have to keep that in mind.

    Big-picture wise, this might be a reasonable place for a key-value store,
    because we just need a yes or a no from the DB when we send it an "is this
    the answer?" query. That's also something to keep in mind.

    However, we're in MVP-ville! And that means that we just shove it into a
    SQLite database and worry about learning MongoDB or whatever later.

    So: this function takes a Deck object as an argument, investigates the
    deck, figures out what kinds of questions are legal and desired, generates
    one, and returns the question-answer pair, from which some other method
    will generate the incorrect answers and take care of persistence, etc.

    Or we might just call that function and return a (question, answer, wrong)
    tuple. That'd work too.
    """
    # Currently we expect to get a list of ($number, $card) tuples. We'll have
    # to coerce $number to a float from string.

    deck_struct = []
    for k in current_deck:
        deck_struct.append({'name': k[1], 'count': int(k[0]),})

    # Going to do this in the naive brute-force way because the expected input
    # for the program is deck lists of <300 cards. Derp. Running up against
    # problems with this already.
    weighted_list = []
    for card in deck_struct:
        for n in range(0, card['count']):
            weighted_list.append(card['name'])

    chosen_card = random.choice(weighted_list)
    chosen_card = [x for x in deck_struct if x['name'] == chosen_card][0]

    possible_questions = {
        'easy': "How many copies of {card} are in your deck?",
        'medium': "How likely is it that at least one copy of {card} will be in your opening hand?",
        # 'hard': "How likely is it that a copy of {card} is in the top &#123;number&#125; cards of your deck?",
        }

    chosen_difficulty = random.choice(possible_questions.keys())

    def _easy_question(card):
        copies = card['count']
        answers = {
            'correct': copies,
            'answer_list': [ x for x in range(copies - 2, copies + 3)],
            # Would like to do something to make answers harder to guess. ^^;; Later!
            'suffix': "copies",
            }
        return answers

    def _medium_question(card, deck_struct):
        copies = card['count']
        deck_size = sum([ x['count'] for x in deck_struct ])
        hand_size = 7
        opening_hand_chance = hypergeom.sf(1, deck_size, copies, hand_size)
        opening_hand_chance = round(opening_hand_chance, 4) * 100

        if chosen_difficulty == 'medium':
            print "Chance of a copy of {} in opening hand: {}".format(card['name'], str(opening_hand_chance))

        gen_wrong = generate_wrong_float_answer
        wrongs = [ round(gen_wrong(2, x), 2) for x in [1.2, 2.0, 6.0, 16.0] ]
        answer_list = wrongs + [opening_hand_chance]
        random.shuffle(answer_list)
        return {'correct': opening_hand_chance,
                'answer_list': answer_list,
                'suffix': "percent"}

    answer_dict = {
        'easy': _easy_question(chosen_card),
        'medium': _medium_question(chosen_card, deck_struct),
        'hard': {'correct': 1, 'answer_list': [2, 3, 4, 5]},
        }

    chosen_question = possible_questions[chosen_difficulty].format(card=chosen_card['name'])
    return chosen_card, chosen_question, answer_dict[chosen_difficulty]

def parse_deck(text_blob):
    """Take a blob of text, tries to turn it into a deck list and a Deck
    object."""

    regex = r'^([0-9]+)[\sx]+?[\'"]?([\w][\w\s\-\']+[\w])[\'"$]?'
    # Note that this assumes that we split the input on newlines.
    # This should give us the card name in \2, and the number of copies in \1.
    # Regex note: watch out for pluralizing cards whose name is singular -
    # e.g. 'Mountains' for 'Mountain'. Is there a reasonable way to solve that?

    original_lines = []
    parsed_lines = []

    for s in text_blob.splitlines():
        original_lines.append("Current line: {}".format(s))
        r = re.search(regex, s)
        if r:
            parsed_lines.append(r.groups())

    return original_lines, parsed_lines

def generate_wrong_float_answer(correct, variance):
    """
    Expects floats `correct` and `variance`. Returns a float, rounded to
    two (three? make sure that tweaking this later won't break things)
    digits, that is guaranteed to not be equal to `correct`, and whose
    magnitude will be between 0.00 and `variance` times `correct`.

    Clunky name. :( But we might also need to generate a wrong string, which is
    different enough that it shouldn't be an if-branch. If a function consists
    of a big if-else block, it probably shouldn't be just one function.

    So, easy way to get four wrong answers:

    [ gen_wrong(2, x) for x in [1.2, 2.0, 6.0, 16.0] ]

    - which should generate a pleasingly varying spread of randomness. Hmm. I
    should have Crypto look at this. There _is_ that quip about the generation
    of random numbers being too important to be left to chance.
    """
    wrong = round(random.uniform(0, round(correct*variance, 4)), 4)
    while wrong > 1:
        wrong /= 10.0
    wrong = wrong * 100
    if wrong == round(correct, 2):
        return generate_wrong_numeric_answer(correct, variance)
    return wrong
