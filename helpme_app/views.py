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
    import pdb; pdb.set_trace()
    print('\nThe following information was returned as a Message object:\n')
    print('  id                : %s' % msg.id)
    print('  href              : %s' % msg.href)
    print('  direction         : %s' % msg.direction)
    print('  type              : %s' % msg.type)
    print('  originator        : %s' % msg.originator)
    print('  body              : %s' % msg.body)
    print('  reference         : %s' % msg.reference)
    print('  validity          : %s' % msg.validity)
    print('  gateway           : %s' % msg.gateway)
    print('  typeDetails       : %s' % msg.typeDetails)
    print('  datacoding        : %s' % msg.datacoding)
    print('  mclass            : %s' % msg.mclass)
    print('  scheduledDatetime : %s' % msg.scheduledDatetime)
    print('  createdDatetime   : %s' % msg.createdDatetime)
    print('  recipients        : %s\n' % msg.recipients.items.recipient)
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
