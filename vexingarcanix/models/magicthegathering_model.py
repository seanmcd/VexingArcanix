""" Persistent data about Magic: the Gathering decks and cards. We persist
    decks so that we can provide the "remember my decks" feature at the core of
    the premium user experience, while we persist cards so that we can know
    about them without going and scraping SERPs for them every time we need to
    know about them or assemble data about them.
"""

from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

# from zope.sqlalchemy import ZopeTransactionExtension
# DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Base = declarative_base()

class MTGDeckModel(Base):
    __tablename__ = 'mtg_decks'

    # User's name for their deck.
    deck_name = Column(Text, primary_key=True)
    # Foreign key into Users, which doesn't exist yet.
    user_id = Column(Text, primary_key=True)
    # Foreign key into MTGCardModel in this module.
    card_count = Column(Integer)
    card_id = Column(Text, primary_key=True)

    def __init__(self, deck_name, user_id, card_id, card_count):
        self.deck_name = deck_name
        self.user_id = user_id
        self.card_id = card_id
        self.card_count = card_count


class MTGCardModel(Base):
    __tablename__ = 'mtg_cards'

    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    rules_text = Column(Text, nullable=False)
    colors = Column(Text, nullable=False)

    # We'll use these for the is_legal() method in the future.
    sets = Column(Text)
    blocks = Column(Text)

    # Everything has a type, so you can't null that, but not everything has a
    # super- or sub-type (e.g. not all lands are Basic, not all Artifacts are
    # Equipment), so those can be null. We should consider making these
    # enum-style columns, since the set of all types in MTG is known, finite,
    # and changes at a very predictable interval.
    types = Column(Text, nullable=False)
    super_types = Column(Text, nullable=True)
    sub_types = Column(Text, nullable=True)

    # Creature-specific characteristics.
    creature_power = Column(Integer, nullable=True)
    creature_toughness = Column(Integer, nullable=True)

    def __init__(self, name, types, rules_text, colors, **card_data):
        self.name = name
        self.types = types
        self.rules_text = rules_text
        self.colors = colors
        self.subtype = card_data.get('subtype', None)
        self.supertype = card_data.get('supertype', None)

        typelist = self.types.split(' ')
        if 'creature' in type_list:
            self._validate_creature(card_data)
        if 'planeswalker' in type_list:
            self._validate_planeswalker(card_data)

    # Special cases to watch out for during validation: Dryad Arbor, which is a
    # Creature Land - Forest Dryad; Mistform Ultimus, which is every creature
    # type, the suspend spells with a printed mana cost of (null) from Time
    # Spiral, the Kobolds with a printed mana cost of 0 that used to have rules
    # text that told you what color they were but now have a 'color indicator'
    # ...

    # A collection of validation methods for specific card types. Comp Rules
    # 205.2a: "205.2a The card types are artifact, creature, enchantment,
    # instant, land, plane, planeswalker, scheme, sorcery, tribal, and
    # vanguard." We are not going to handle Vanguards, Schemes, or Planes -
    # those are for variant forms of magic that are not played at the level of
    # competition where people actually use tools like Vexing Arcanix. Tribal
    # is actually a bastard supertype: the existing Tribal cards are all things
    # like Tribal Sorcery or Tribal Enchantment, and in practice it means "a
    # non-creature spell that has a creature type." Instants, sorceries,
    # artifacts, enchantments, and lands have subtypes (e.g. Arcane, Equipment,
    # Aura, Locus), but don't really have more distinct information that *is*
    # mandatory and *is not* rules text. However, creature and planeswalkers do
    # have mandatory extra information, so we have to make sure that we have
    # *something* for that information.

    def _validate_creature(self, **card_data):
        # Must have a creature type.  We _could_ validate against the known
        # list of creature types - the canonical list is Comp Rules section
        # 205.3m - but that's a premature optimization. What's important is
        # that a creature *must have* a subtype: for our purposes it's not
        # really important what the actual subtype is.
        if card_data['subtype'] is None:
            raise ValueError
        # Must have power and toughness.
        if card_data['power'] is None:
            raise ValueError
        if card_data['toughness'] is None:
            raise ValueError
        return True

    def _validate_planeswalker(self, **card_data):
        # Must have a planeswalker type, and it must be a string.
        if card_data['subtype'] is None:
            raise ValueError
        return True
