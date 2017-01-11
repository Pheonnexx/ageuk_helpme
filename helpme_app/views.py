import logging
import requests
import json
from twilio.rest import TwilioRestClient
from helpme_app import ask, app

from flask import render_template
from flask_ask import Ask, statement, question, session

logging.getLogger("flask_ask").setLevel(logging.DEBUG)
account_sid = "ACe69a7715e0d849e09986dddf5b7466ec" # Your Account SID from www.twilio.com/console
auth_token  = "0281349406c665e16ed332ec68ac185a"  # Your Auth Token from www.twilio.com/console

@ask.launch
def start_helpme_app():
    what_do_you_need = render_template('what_do_you_need')

    return question(what_do_you_need)


@ask.intent("AddNewContactIntent")
def supply_contact_name():
    please_supply_name = render_template('please_supply_name')

    return question(please_supply_name)


@ask.intent("AddContactNameIntent", convert={"contact": str})
def add_contact_name(contact):
    session.attributes['contact'] = contact

    what_is_contact_number = render_template('what_is_contact_number')

    return question(what_is_contact_number)


@ask.intent("AddContactNumberIntent", convert={"contact_number": int})
def add_contact_number(contact_number):
    session.attributes['contact_number'] = contact_number

    contact_added = render_template('contact_added',
                                                name = session.attributes['contact'],
                                                number = session.attributes['contact_number'])
    print(session.attributes['contact'])
    print(session.attributes['contact_number'])

    return statement(contact_added)


@ask.intent("HelpMeFriendIntent", convert={'helpmefriend': str})
def get_help_from_friend(helpmefriend):
    if 'helpmefriend' in convert_errors:
        return question("Can you please repeat the name?")

    #message person that has been selected from contact list
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(body="Hello from Python",
        to="07960207329",    # Replace with your phone number
        from_="441772367243") # Replace with your Twilio number

    print(message.sid)

    if message:
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
