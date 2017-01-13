import logging
import requests
import json
from twilio.rest import TwilioRestClient
from helpme_app import ask, app

from flask import render_template
from flask_ask import Ask, statement, question, session

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

account_sid = app.config['ACCOUNT_SID']
auth_token = app.config['AUTH_TOKEN']


# Initial launch of the helpme app
@ask.launch
def start_helpme_app():
    what_do_you_need = render_template('what_do_you_need')

    return question(what_do_you_need)


# The initial question to when someone wants to add a contact, they are asked for the name
@ask.intent("AddNewContactIntent")
def supply_contact_name():
    please_supply_name = render_template('please_supply_name')

    return question(please_supply_name)


# When the user adds a name it is saved in the session, so it is kept until we also have the contact
# number, which we ask for next
@ask.intent("AddContactNameIntent", convert={"contact": str})
def add_contact_name(contact):
    session.attributes['contact'] = contact

    what_is_contact_number = render_template('what_is_contact_number')

    return question(what_is_contact_number)


# After the user provides the number, this is also then saved to a session variable.  This is then
# to be saved in the database.
@ask.intent("AddContactNumberIntent", convert={"contact_number": int})
def add_contact_number(contact_number):
    session.attributes['contact_number'] = contact_number

    contact_added = render_template('contact_added',
                                                name = session.attributes['contact'],
                                                number = session.attributes['contact_number'])
    print(session.attributes['contact'])
    print(session.attributes['contact_number'])
    # The too session variables will also be saved with the amazon user id so that they can then
    # be accessed via name at a later time.

    # When the contact is added successfully then the user is informed with a statement.  This
    # effectively ends the session.
    return statement(contact_added)


# A person asks to contact someone by supplying the contact name, currently hardcoded to one person,
# this will soon request help from someone stored in the database
@ask.intent("HelpMeFriendIntent", convert={'helpmefriend': str})
def get_help_from_friend(helpmefriend):

    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(body="Hello from Python",
        to="07960207329",    # Replace with your phone number
        from_="441772367243") # Current Twilio number, will replace with env var soonish

    print(message.sid)

    if message:
        statement_msg = render_template('get_help_from_friend', helpmefriend = helpmefriend)
    else:
        statement_msg = render_template('unable_to_contact_person', helpmefriend = helpmefriend)

    return statement(statement_msg)


@ask.intent("HelpMeIntent")
def get_help():
    #contacting all for help
    statement_msg = render_template('get_help')

    return statement(statement_msg)


@ask.session_ended
def session_ended():
    return "", 200
