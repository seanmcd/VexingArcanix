""" Persistent data about Pokemon CCG and cards. We persist decks so that we
    can provide the "remember my decks" feature at the core of the premium user
    experience, while we persist cards so that we can know about them without
    going and scraping SERPs for them every time we need to know about them or
    assemble data about them.
"""

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

Base = declarative_base()

class PokemonDeckModel(Base):
    __tablename__ = 'pokemon_decks'

    # User's name for their deck.
    deck_name = Column(Text, primary_key=True)
    # Foreign key into Users, which doesn't exist yet.
    user_id = Column(Text, primary_key=True)
    # Foreign key into PokemonCardModel in this module.
    card_count = Column(Integer)
    card_id = Column(Text, primary_key=True)

    def __init__(self, deck_name, user_id, card_id, card_count):
        self.deck_name = deck_name
        self.user_id = user_id
        self.card_id = card_id
        self.card_count = card_count


class PokemonCardModel(Base):
    __tablename__ = 'pokemon_cards'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)

    # Pokemon has slightly overloaded "type," because it means both card type
    # and Pokemon energy type.
    card_type = Column(Text, nullable=False)

    pokemon_type = Column(Text, nullable=True)
    evolution_stage = Column(Text, nullable=True)
    hitpoints = Column(Integer, nullable=True)

    def __init__(self, name, card_type, **card_data):
        self.name = name
        self.card_type = card_type
        self.pokemon_type = card_data.get('pokemon_type', None)

        if 'card_type' == 'pokemon':
            self._validate_pokemon(card_data)

    def _validate_pokemon(self, **card_data):
        return True
