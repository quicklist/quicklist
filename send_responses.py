from datetime import datetime
from query_twilio import twilio_send_list
from quicklist import UserAccount,Quicklist

"""
    process commands and other messages
"""

def respond_with_list(message ,user_db, quicklist_db, live):
    print("Sending live is set to:",bool(live))
    if live:
        twilio_send_list(message.from_,quicklist_db[user_db[message.from_[1:]].current_list].list_as_str())
    else:
        print quicklist_db[user_db[message.from_[1:]].current_list].list_as_str()
        
