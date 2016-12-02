import logging
import requests
import json
from helpme_app import ask
from clockwork import clockwork

from flask import render_template
from flask_ask import Ask, statement, question, session

api = clockwork.API('API_KEY_GOES_HERE')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def start_helpme_app():
    what_do_you_need = render_template('what_do_you_need')

    return question(what_do_you_need)


@ask.intent("HelpMeFriendIntent", convert={'helpmefriend': str})
def get_help_from_friend():
    #message person that has been selected from contact list
    message = clockwork.SMS(
    to = '00447960207329',
    message = 'Please help such n such! - test message')

    response = api.send(message)

    if response.success:
        statement = render_template('get_help_from_friend', helpmefriend = helpmefriend)
    else:
        statement = render_template('unable_to_contact')

    return statement(statement)


@ask.intent("HelpMeIntent")
def get_help():
    #contacting all for help
    statement = render_template('get_help')

    return statement(statement)


@ask.session_ended
def session_ended():
    return "", 200
