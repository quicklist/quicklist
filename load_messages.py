from datetime import datetime
from quicklist import UserAccount, Quicklist, TwilioList
from send_responses import respond_with_list
"""
    read one account and append the quicklist
"""
def get_message_list(twilio_messages, marker_sid):
    message_db=[]
    for message in twilio_messages:
        if message.sid != marker_sid:
            if message.status == 'received':
                message_db.append(TwilioList(message.sid, message.from_, message.body, message.status))
        else:
            return message_db
    return message_db

def read_messages(message, user_db, quicklist_db):
    date_created = datetime.utcnow().strftime("%Y-%m-%d")
    date_modified = date_created
    current_list = user_db[message.from_[1:]].current_list
    if message.body[:2]!="//" and len(message.body) > 2:
        quicklist_db[current_list].add_items([message.body.strip()])
    elif message.body[2:].split()[0]=="clear":
        quicklist_db[current_list].clear_list()
    elif message.body[2:].split()[0]=="swap" and len(message.body.split())>1:
        print(user_db[message.from_[1:]]).current_list
        user_db[message.from_[1:]].swap_list(message.body.split()[1])
        print(user_db[message.from_[1:]]).current_list
    elif message.body[2:].split()[0]=="ls":
        if len(message.body)>0:
            respond_with_list(message, user_db, quicklist_db, 1)
    elif message.body[:2]=="//":
        print("found unk command:"+message.body)#test
    else:
        pass #message ignored
    return user_db, quicklist_db, message.sid



