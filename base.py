from datetime import datetime
from quicklist import UserAccount,Quicklist
from load_accounts import get_account_list, init_accounts
from load_messages import get_message_list, read_messages
from send_responses import process_command_list
from query_twilio import twilio_read_all_today
import time
"""
    Brief description:
        This program reads short messages from source
        and creates unique lists that can be read and appended
        by others.
    Business case:
        Two people are responsible for shopping for groceries.
        The needs are constantly growing throughout the week.
        Each person texts an item to be saved on the list. The
        program stores the request. The full list is available
        to each users at any time using command.
        When shopping is complete either user can clear the list
        using a command. Commands are reserved words that are not
        included on list.
    Class structure is defined in quicklist.py
        user_db is a dict of string and UserAccount object
        quicklist_db is a dict of string name and Quicklist object
        TwilioList is an object simulating a query from twilio.
"""
def main(user_db, quicklist_db, marker_sid, default_name):
    #read all messages to from account
    #determine account list, unique list of from_ numbers
    #find sid of latest message
    twilio_messages = twilio_read_all_today()
    account_list, last_message_sid = get_account_list(twilio_messages)
    print("_________new message:"+ str(last_message_sid != marker_sid))
    if last_message_sid != marker_sid:
        #add new accounts
        user_db=(init_accounts(user_db, account_list, default_name))
        #get the list of new incoming message
        message_db = get_message_list(twilio_messages, marker_sid)
        message_db.reverse()
        print("start reading messages len:", len(message_db))
        i=0
        for message in message_db:
            for account in user_db.keys():
                if user_db[account].current_list not in quicklist_db.keys():
                    quicklist_db[user_db[account].current_list] = Quicklist(user_db[account].current_list,[])
            i+=1
            print("body:",str(message.body),i)
            user_db, quicklist_db, marker_sid = read_messages(message, user_db, quicklist_db)

    return user_db, quicklist_db, marker_sid


    
user_db = {}
quicklist_db={}
commandlist_db={}
default_name = "shop"
marker_sid=None

for i in range(2000):
    time.sleep(15)
    print("run:"+str(i))
    for account in user_db.keys():
        print("BEFORE"),user_db[account].show_account_info()
    user_db, quicklist_db, marker_sid = main(user_db, quicklist_db, marker_sid, default_name)
    for account in user_db.keys():
        print("AFTER"),user_db[account].show_account_info()
    for quicklist,m in quicklist_db.items():
        print("final list of lists:",quicklist)
        m.print_body()
    i+=1
