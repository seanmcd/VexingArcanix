from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from .models import (
    DBSession,
    MyModel,
    )

from vexingarcanix.lib import mvp

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
    raw, parsed = mvp.parse_deck(request.POST.get('deck_list_area'))
    request.session['current_deck'] = parsed
    return {'form_data': raw, 'parsed_data': parsed, }

@view_config(route_name='show_question', renderer='questions.mako')
def generate_question(request):
    # Generate a question and answer, display the question, store the answer to
    # the current question in the session object.
    this_answer = request.session.get('given_answer', None)
    last_was_correct = request.session.get('correctness', None)
    try:
        this_card, this_question, this_answer_set = mvp.generate_question(request.session['current_deck'])
        request.session['correct_answer'] = this_answer_set.get('correct', None)
        this_answer_set['last_answer'] = request.session.get('answer_to_last_question', None)
        print "correct answer: {}".format(this_answer_set['correct'])
        return {'question': this_question,
                'card': this_card,
                'correctness': last_was_correct,
                'given_answer': this_answer,
                'answer_set': this_answer_set,}
    except KeyError:
        return HTTPFound('/')

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
