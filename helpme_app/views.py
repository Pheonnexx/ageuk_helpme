import logging
import requests
import json
import messagebird
from helpme_app import ask, app

from flask import render_template
from flask_ask import Ask, statement, question, session

client = messagebird.Client('cUTQcjhDaqfscs0pKHhGQk6aR')
logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def start_helpme_app():
    what_do_you_need = render_template('what_do_you_need')

    return question(what_do_you_need)


@ask.intent("HelpMeFriendIntent", convert={'helpmefriend': str})
def get_help_from_friend(helpmefriend):
    #message person that has been selected from contact list
    msg = client.message_create(
        'HEATHER',
        '+447960207329',
        'This is a test message.',
        { 'reference' : 'Heather' }
    )
    if msg:
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
