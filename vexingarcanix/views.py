from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from .models import (
    DBSession,
    MyModel,
    )

from vexingarcanix.lib import abstracts, identifier, questions

import random

@view_config(route_name='give_deck', renderer='frontpage.mako')
def deck_ingest(request):
    # one = DBSession.query(MyModel).filter(MyModel.name=='one').first()
    # Send the user a page that asks them for a deck, start up a session for them.
    return {"foo": "bar"}

@view_config(route_name='check_deck', renderer='confirm_deck.mako')
def parse_deck(request):
    # FUTURE: Reject the input if it's > 5KB of text.
    raw_card_list = request.POST.get('deck_list_area')
    identified_cards, unknown_cards = identifier.find_cards(raw_card_list)

    card_object_list = [ abstracts.Card(card[1], card[0]) for card in identified_cards ]
    deck_object = abstracts.Deck(card_object_list)
    request.session['current_deck_object'] = deck_object

    game_guess = identifier.find_game([card[1] for card in identified_cards])

    # change 'parsed_data' on below line and in .mako to better name
    return {'deck': deck_object,
            'game_guess': game_guess,
            'unknown_cards': unknown_cards,
            }

@view_config(route_name='show_question', renderer='questions.mako')
def generate_question(request):
    # Generate a question and answer, display the question, store the answer to
    # the current question in the session object.
    deck_object = request.session.get('current_deck_object', None)
    if not deck_object:
        return HTTPFound('/')

    last_given_answer = request.session.get('last_given_answer', None)
    last_correct_answer = request.session.get('last_correct_answer', None)
    last_was_correct = request.session.get('last_was_correct', None)

    question_generator = abstracts.Question()
    current_question = question_generator.choose_question()
    question_string, correct, possible_answers, answer_suffix, chosen_card = current_question(deck_object)

    request.session['correct_answer'] = correct
    print "correct answer: {}".format(correct)

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
        # Remember that this is where we'll end up with answers that are strings!
        request.session['last_given_answer'] = None
        request.session['last_correct_answer'] = None
        request.session['last_was_correct'] = None

    return HTTPFound('/ask')
