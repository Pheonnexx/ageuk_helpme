import logging
import requests
import json
from helpme_app import ask, app
from clockwork import clockwork

from flask import render_template
from flask_ask import Ask, statement, question, session

api = clockwork.API(app.config['CLOCKWORK_API_KEY'])
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def start_helpme_app():
    what_do_you_need = render_template('what_do_you_need')

    return question(what_do_you_need)


@ask.intent("HelpMeFriendIntent", convert={'helpmefriend': str})
def get_help_from_friend(helpmefriend):
    #message person that has been selected from contact list
    message = clockwork.SMS(
    to = '00447960207329',
    message = 'Please help such n such! - test message')

    response = api.send(message)

    if response.success:
        msg = render_template('get_help_from_friend', helpmefriend = helpmefriend)
    else:
        msg = render_template('unable_to_contact_person', helpmefriend = helpmefriend)

    return statement(msg)


@ask.intent("HelpMeIntent")
def get_help():
    #contacting all for help
    statement = render_template('get_help')

    return statement(statement)


@ask.session_ended
def session_ended():
    return "", 200
