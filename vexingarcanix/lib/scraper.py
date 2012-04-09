""" A module that goes out and scrapes magiccards.info, the Pokemon.com card
    search site, l5rsearch.com, and other sources, to find the text of cards
    that aren't in our database yet and add them. Bit of a tedious thing.
"""

class Scraper(object):
    """ Create an instance of Scraper first, telling it what game you want to
        investigate, then use the find_card method to actually go fetch a SERP
        (search engine results page) and analyze it. Since it's reasonably
        likely that we'll need to search for more than one card at a time,
        we're trying to make that use case easy: instantiate the class once,
        invoke its primary method as many times as needed.
    """

    def __init__(self, game):
        """ Short canonical list of games that we know how to search for.
        """
        self.game = game
        if game not in ['magicthegathering', 'pokemon', 'l5r']:
            raise NotImplementedError

    def scrape(self, card_name):
        """ Take a card name, introspect to see what kind of game this scraper
            object is for, go retrieve search pages for the appropriate card
            and game, analyze the pages, return card information.
        """
        raise NotImplementedError
