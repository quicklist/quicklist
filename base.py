from datetime import datetime
from quicklist import UserAccount,Quicklist
from load_accounts import get_account_list, init_accounts
from load_messages import get_message_list, read_messages
from query_twilio import twilio_read_all_today
import time
"""
    Brief description:
        This program reads short text messages from source (twilio)
        and creates unique lists that can be shared and edited
        by others.
    Business case:
        Two people are responsible for shopping for groceries.
        The needs are constantly growing throughout the period.
        Each person texts an item to be saved on the list. The
        program stores the string to a logical list.
        The user can create and swap between lists
        The full list is available to each user at any time using
        command.
        When shopping is complete either user can clear the list
        using a command. Commands are messages starting with "//"
        valid commands are processed and invalid commands ignored.
        Command are not stored on the list.
    Classes: (structure is defined in quicklist.py)
        user_db is a dict of string and UserAccount object
        quicklist_db is a dict of string name and Quicklist object
        TwilioList is an object similar to a query from twilio.
    Updates:
        2sep2014 initial beta (bugs: twilio ResponseNotReady)
        18sep2014 fixed ResponseNotReady, added feature to ignore
            old commands after a restart, added list name to head
            each outgoing response from list command
"""
def main(user_db, quicklist_db, marker_sid, default_name):
    #read all messages to from account
    twilio_messages, twilio_result = twilio_read_all_today()
    #twilio commonly throws exception ResponseNotReady
    #if exception return and allow to run next cycle
    if not twilio_result:
        return user_db, quicklist_db, marker_sid, twilio_result
    #determine account list; i.e. unique list of from_ numbers
    #find sid of latest message
    account_list, last_message_sid = get_account_list(twilio_messages)
    print("_________new message:"+ str(last_message_sid != marker_sid))
    if last_message_sid != marker_sid:
        #check for restart, user_db is empty at start
        #after restart avoid sending aged responses like list
        if len(user_db.keys())==0:
            restart_detected=True
        else:
            restart_detected=False
        #add new accounts to user_db
        user_db=(init_accounts(user_db, account_list, default_name))
        #parse the list of new incoming sms to message_db
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
            user_db, quicklist_db, marker_sid = read_messages(message, user_db, quicklist_db, restart_detected)

    return user_db, quicklist_db, marker_sid, twilio_result


    
user_db = {}
quicklist_db={}
commandlist_db={}
default_name = "shop"
marker_sid=None

for i in range(2000):
    time.sleep(20)
    print("run:"+str(i))
    for account in user_db.keys():
        print("BEFORE"),user_db[account].show_account_info()
    user_db, quicklist_db, marker_sid, result = main(user_db, quicklist_db, marker_sid, default_name)
    if result:
        for account in user_db.keys():
            print("AFTER"),user_db[account].show_account_info()
        for quicklist,m in quicklist_db.items():
            print("final list of lists:",quicklist)
            m.print_body()
    i+=1
