"""
This module is responsible for taking a blob of text that we've gotten from a
site visitor, turning it into a list of cards, and identifying what game these
cards are from.
"""
import re

def find_cards(text_blob):
    """ Takes a blob of text as an argument and tries to turn it into a list of
    (cardname, count) tuples. """

    regex = r'^([0-9]+)[\sx]+?[\'"]?([\w][\w\s\-\']+[\w])[\'"$]?'
    # Note that this assumes that we split the input on newlines.
    # This should give us the card name in \2, and the number of copies in \1.
    # Regex note: watch out for pluralizing cards whose name is singular -
    # e.g. 'Mountains' for 'Mountain'. Is there a reasonable way to solve that?

    found_cards = []
    unknown_cards = []
    for s in text_blob.splitlines():
        # original_lines.append("Current line: {}".format(s))
        r = re.search(regex, s)
        if r:
            found_cards.append(r.groups())
            print "Found card: {}".format(r.groups())
        else:
            unknown_cards.append(s)
    return found_cards, unknown_cards

registered_games = []

def register_game(game):
    registered_games.append(game)
    return game

def find_game(cards):
    """Takes a list of cards and tries to figure out which game they could be a
    deck for."""
    # FUTURE: These will be database calls, not just matching a list. However,
    # for now - list! Get it working first. Still in MVP mode.
    is_game = None
    if not registered_games:
        print "No games registered to check against."
    for game in registered_games:
        is_game = game(cards)
        if is_game:
            print "Survey says ... {}!".format(is_game)
            return is_game
    if not is_game:
        # We'll work out later what to do if we don't know what game it is.
        return "Unknown Game"

@register_game
def _is_pokemon_deck(cards):
    """A rough check to see whether this is a Pokemon deck."""
    pokemon_unique = ['darkness energy', 'fighting energy', 'fire energy', 'grass energy', 'lightning energy', 'metal energy', 'psychic energy', 'water energy', 'arceus']
    for card in cards:
        if card.lower() in pokemon_unique:
            return "pokemon"
    return False

@register_game
def _is_magic_deck(cards):
    """A rough check to see whether this is a Magic deck."""
    magic_unique = ['plains', 'island', 'swamp', 'mountain', 'forest', 'snow-covered plains', 'snow-covered island', 'snow-covered swamp', 'snow-covered mountain', 'snow-covered forest', 'relentless rats']
    for card in cards:
        if card.lower() in magic_unique:
            return "magicthegathering"
    return False

@register_game
def _is_l5r_deck(cards):
    l5r_unique = ['gifts and favors', 'a favor returned', 'copper mine', 'iron mine', 'gold mine', 'obsidian mine', 'kobune port', 'geisha house', 'marketplace', 'silver mine', 'silk works', 'stables', 'treasure hoard']
    for card in cards:
        if card.lower() in l5r_unique:
            return "l5r"
    return False
