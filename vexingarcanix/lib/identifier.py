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
    for game in registered_games:
        is_game = game(cards)
        if is_game:
            print "Survey says ... {}!".format(is_game)
            return is_game
    if not is_game:
        # We'll work out later what to do if we don't know what game it is.
        return None

@register_game
def _is_pokemon_deck(cards):
    """A rough check to see whether this is a Pokemon deck."""
    pokemon_unique = ['Darkness Energy','Fighting Energy','Fire Energy','Grass Energy','Lightning Energy','Metal Energy','Psychic Energy', 'Water Energy', 'Arceus']
    for card in cards:
        if card in pokemon_unique:
            return "pokemon"
    return False

@register_game
def _is_magic_deck(cards):
    """A rough check to see whether this is a Magic deck."""
    magic_unique = ['Plains', 'Island', 'Swamp', 'Mountain', 'Forest', 'Snow-covered Plains', 'Snow-covered Island', 'Snow-covered Swamp', 'Snow-covered Mountain', 'Snow-covered Forest', 'Relentless Rats']
    for card in cards:
        if card in magic_unique:
            return "magicthegathering"
    return False

@register_game
def _is_l5r_deck(cards):
    l5r_unique = ['Gifts and Favors', 'A Favor Returned', 'Copper Mine', 'Iron Mine', 'Gold Mine', 'Obsidian Mine', 'Kobune Port', 'Geisha House', 'Marketplace', 'Silver Mine', 'Silk Works', 'Stables', 'Treasure Hoard']
    for card in cards:
        if card in l5r_unique:
            return "l5r"
    return False
