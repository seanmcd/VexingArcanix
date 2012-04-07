from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from .models import (
    DBSession,
    MyModel,
    )

from vexingarcanix.lib import abstracts, identifier
import random

@view_config(route_name='give_deck', renderer='frontpage.mako')
def deck_ingest(request):
    # Send the user a page that asks them for a deck, start up a session for them.
    for key in ['current_deck_object', 'last_given_answer', 'game_confirmed']:
        request.session[key] = None
    return {"foo": "bar"}

@view_config(route_name='check_deck', renderer='confirm_deck.mako')
def parse_deck(request):
    # FUTURE: Reject the input if it's > 5KB of text.
    raw_card_list = request.POST.get('deck_list_area')
    identified_cards, unknown_cards = identifier.find_cards(raw_card_list)

    DeckClass, CardClass, QuestionClass = identifier.find_game([card[1] for card in identified_cards])
    if DeckClass.game_name:
        request.session['game_guess'] = getattr(DeckClass, 'game_name')
        print "Our guess: a {} deck".format(getattr(DeckClass, 'game_name'))
    else:
        request.session['game_guess'] = "Unknown Game"
    request.session['game_classes'] = { 'deck'     : DeckClass,
                                        'card'     : CardClass,
                                        'question' : QuestionClass,
                                        }

    card_object_list = [ abstracts.Card(card[1], card[0]) for card in identified_cards ]
    deck_object = abstracts.Deck(card_object_list)
    request.session['current_deck_object'] = deck_object

    return {'deck': deck_object,
            'game_guess': request.session['game_guess'],
            'unknown_cards': unknown_cards,
            }

@view_config(route_name='show_question', renderer='questions.mako')
def generate_question(request):
    # Generate a question and answer, display the question, store the answer to
    # the current question in the session object.
    current_deck = request.session.get('current_deck_object', None)
    if not current_deck:
        return HTTPFound('/')

    # Create Cards, a Deck, and a Question for the appropriate game if this is
    # the first question after deck confirmation. Only create them if we don't
    # have them already: DB queries are expensive.
    if (not current_deck.game_name) and (request.session.get('game_guess', None) != "Unknown Game"):
        # Oy. "If the current deck has no name and if our guess for the game is
        # something other than 'Unknown Game', enter this branch." I feel like
        # this could be better.
        try:
            # If we're missing any of these, something is wrong.
            DeckClass = request.session['game_classes']['deck']
            CardClass = request.session['game_classes']['card']
            QuestionClass = request.session['game_classes']['question']
        except KeyError:
            requestion.session['error_flash'] = "Something broke while trying to get our game-specific classes!"
            return HTTPFound('/')
        new_decklist = []
        print "Constructing a {} deck ...".format(DeckClass.game_name)
        for card in current_deck.decklist:
            new_decklist.append(CardClass(card.name, card.count))
        new_deck = DeckClass(new_decklist)
        current_deck = request.session['current_deck_object'] = new_deck

    # Set up a Question instance.
    if not request.session.get('question_generator', None):
        if not current_deck.game_name:
            question_generator = abstracts.Question()
        else:
            question_generator = QuestionClass()
        request.session['question_generator'] = question_generator

    # Record information about the last question.
    last_given_answer = request.session.get('last_given_answer', None)
    last_correct_answer = request.session.get('last_correct_answer', None)
    last_was_correct = request.session.get('last_was_correct', None)

    # Generate a new question.
    current_question = request.session['question_generator'].choose_question()
    question_string, correct, possible_answers, answer_suffix, chosen_card = current_question(current_deck)
    request.session['correct_answer'] = correct
    print "Correct answer: {}".format(correct)
    print "Other answers: {}".format(possible_answers)

    # Bundle it up and ship it out.
    return {'question': question_string,
            'possible_answers': possible_answers,
            'answer_suffix': answer_suffix,
            'card': chosen_card,
            'last_given_answer': last_given_answer,
            'last_correct_answer': last_correct_answer,
            'last_was_correct': last_was_correct,
            }

@view_config(route_name='check_answer', request_method='POST')
def check_answer(request):
    # Look at the answer from POST, compare it to the correct answer in the
    # session object, add an appropriate flash message to the session, redirect
    # to the ask-me-a-question page.
    current_given_answer = request.POST.get('answer', None)
    current_correct_answer = request.session.get('correct_answer', None)
    print "Given answer: {}. Correct answer: {}. Checking ...".format(current_given_answer, current_correct_answer)

    try:
        # TODO: Sense whether the answer is a float, int, or string, and
        # respond appropriately.
        if float(current_given_answer) == float(current_correct_answer):
            request.session['last_was_correct'] = True
        else:
            request.session['last_was_correct'] = False
        request.session['last_given_answer'] = current_given_answer
        request.session['last_correct_answer'] = current_correct_answer
    except TypeError:
        # Remember that this is where we'll end up with answers that are
        # strings, until we fix the above try-block to tell apart different
        # types of answer.
        request.session['last_given_answer'] = None
        request.session['last_correct_answer'] = None
        request.session['last_was_correct'] = None

    return HTTPFound('/ask')
