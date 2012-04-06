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
    # Take a form that the user POSTs to us, turn it into a string, parse that
    # string into a dict that represents their deck.
    # FUTURE: Reject the deck if it's > 5KB of text.
    raw_card_list = request.POST.get('deck_list_area')
    card_list = identifier.find_cards(raw_card_list)
    game_guess = identifier.find_game(card_list)
    request.session['current_deck'] = card_list

    card_object_list = [ abstracts.Card(card[1], card[0]) for card in card_list ]
    deck_object = abstracts.Deck(card_object_list)
    request.session['current_deck_object'] = deck_object

    # change 'parsed_data' on below line and in .mako to better name
    return {'form_data': raw_card_list, 'parsed_data': card_list, }

@view_config(route_name='show_question', renderer='questions.mako')
def generate_question(request):
    # Generate a question and answer, display the question, store the answer to
    # the current question in the session object.
    this_answer = request.session.get('given_answer', None)
    last_was_correct = request.session.get('correctness', None)
    current_deck_object = request.session.get('current_deck_object', None)
    if current_deck_object:
        new_question = abstracts.Question(current_deck_object)
        current_question = new_question.choose_question(new_question.deck)
        question_string, correct, possible_answers, answer_suffix, chosen_card = current_question(new_question.deck)
        request.session['correct_answer'] = correct
        print "correct answer: {}".format(correct)
        return {'question': question_string,
                'card': chosen_card,
                'correctness': last_was_correct,
                'given_answer': this_answer,
                'answer_set': possible_answers,
                'last_answer': request.session.get('answer_to_last_question', None),
                'answer_suffix': answer_suffix,
                }

@view_config(route_name='check_answer', renderer='questions.mako', request_method='POST')
def check_answer(request):
    # Look at the answer from POST, compare it to the correct answer in the
    # session object, add an appropriate flash message to the session, redirect
    # to the ask-me-a-question page.
    request.session['given_answer'] = request.POST.get('answer')
    print "Given answer: {}. Correct answer: {}. Checking ...".format(request.session['given_answer'], request.session['correct_answer'])
    try:
        request.session['answer_to_last_question'] = request.session['correct_answer']
        if float(request.session['given_answer']) == float(request.session['correct_answer']):
            request.session['correctness'] = True
        else:
            request.session['correctness'] = None
        return HTTPFound('/ask')
    except TypeError:
        request.session['correctness'] = None
        request.session['answer_to_last_question'] = None
        return HTTPFound('/ask')
