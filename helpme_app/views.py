import logging
import requests
import json
from helpme_app import ask

from flask import render_template
from flask_ask import Ask, statement, question, session

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def start_helpme_app():
    what_do_you_need = render_template('what_do_you_need')

    return question(what_do_you_need)


@ask.intent("HelpMeFriendIntent", convert={'helpme': str})
def get_help_from_friend():
    #message person that has been selected from contact list
    message = clockwork.SMS(
    to = '00447960207329',
    message = 'This is a test message.')

    response = api.send(message)

    if response.success:
        statement = render_template('get_help_from_friend', helpme = helpme)
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
