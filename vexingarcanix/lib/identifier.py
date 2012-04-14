""" This module is responsible for taking a blob of text that we've gotten from
    a site visitor, turning it into a list of cards, and identifying what game
    these cards are from.
"""
import re

def find_cards(text_blob):
    """ Takes a blob of text as an argument and tries to turn it into a list of
        (cardname, count) tuples. This card name is only an approximation: Card
        objects for individual games know how to find their canonical names
        (e.g. to turn 'Mewtwo EX' into "Mewtwo" with the EX flag set, or to
        turn 'Jace TMS' into "Jace, the Mind Sculptor").
    """

    regex = r'^\s*([0-9]+)[\sx]+?[\'"]?(\w[\w\s\'\.-]+\w|\w+)[\'"]?[\s(]*([\w\s-]+)?\)?$'

    # Attempts to match a number followed by a number followed by a card
    # name. This should give us the card name in \2, and the number of copies
    # in \1. Part of why this is so thorny is that it tries to be
    # user-compassionate - it'll allow a parenthetical 'hints' at the end, and
    # allows quoting in various ways, "5 Foo" as well as "5x Foo". Also it has
    # to handle card names with apostrophes (e.g. Ertai's Meddling), with dots
    # (e.g. Pokegear 3.0), and with one-letter length (e.g. N from
    # Pokemon). Eventually it'll also have to handle delta cards from Pokemone
    # because completionist.

    found_cards = []
    unknown_cards = []

    for s in text_blob.splitlines():
        # TODO: Add ability to detect duplicates.
        if re.search(r'^[\s\n]*$', s):
            print "Found a blank line."
            continue
        r = re.search(regex, s)
        if r:
            found_cards.append(r.groups())
            print "Found card: {}".format(r.groups()[0:2])
            try:
                hint = r.groups()[2]
                print "Found a hint: {}".format(hint)
            except IndexError:
                hint = None
                print "Found no hint."
        else:
            print "Couldn't identify: {}".format(s)
            unknown_cards.append(s)
    return found_cards, unknown_cards

registered_games = []

def register_game(game):
    registered_games.append(game)
    return game

def find_game(cards):
    """ Takes a list of cards and tries to figure out which game they could be a
        deck for, then returns the appropriate Deck, Card, and Question classes so
        that the caller can instantiate them later.
    """
    # FUTURE: Query database for the cards to fingerprint a game.
    is_game = None
    if not registered_games:
        print "No games registered to check against."

    for game in registered_games:
        is_game = game(cards)
        if is_game:
            Deck, Card, Question = is_game
            return Deck, Card, Question
    if not is_game:
        from vexingarcanix.games import base
        Deck, Card, Question = base.Deck, base.Card, base.Question
        return Deck, Card, Question

@register_game
def _is_pokemon_deck(cards):
    pokemon_unique = ['darkness energy', 'fighting energy', 'fire energy', 'grass energy', 'lightning energy', 'metal energy', 'psychic energy', 'water energy', 'arceus']
    for card in cards:
        if card.lower() in pokemon_unique:
            from vexingarcanix.games import pokemon as pk
            return pk.PokemonDeck, pk.PokemonCard, pk.PokemonQuestion
    return False

@register_game
def _is_magic_deck(cards):
    magic_unique = ['plains', 'island', 'swamp', 'mountain', 'forest', 'snow-covered plains', 'snow-covered island', 'snow-covered swamp', 'snow-covered mountain', 'snow-covered forest', 'relentless rats']
    for card in cards:
        if card.lower() in magic_unique:
            from vexingarcanix.games import magicthegathering as mtg
            return mtg.MTGDeck, mtg.MTGCard, mtg.MTGQuestion
    return False

@register_game
def _is_l5r_deck(cards):
    l5r_unique = ['gifts and favors', 'a favor returned', 'copper mine', 'iron mine', 'gold mine', 'obsidian mine', 'kobune port', 'geisha house', 'marketplace', 'silver mine', 'silk works', 'stables', 'treasure hoard']
    for card in cards:
        if card.lower() in l5r_unique:
            from vexingarcanix.games import l5r
            return l5r.L5RDeck, l5r.L5RCard, l5r.L5RQuestion
    return False
