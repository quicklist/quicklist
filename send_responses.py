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
        
def process_command_list(account, user_db, command_list, quick_list):
    message_string=''
    for command_body,command_sid in command_list.items():
        print("mycommandlist to compare:")
        print user_db[account].command_sids
        print("mynewcommand:")
        print command_body,command_sid
        if not command_sid in user_db[account].command_sids:
            if command_body.split()[0] == "//list":
                print("//executing:"+command_body)
                for message in quick_list.list_obj:
                    message_string += '\n' + message.body
                to_number = user_db[account].phone_number
                print("***SENDINGLIVE***"+to_number)
                twilio_send_list(to_number, message_string)
                print message_string
            elif command_body.split()[0] == "//swp" and len(command_body.split())>1:
                print("//executing:"+command_body)
                user_db[account].swap_list(command_body.split()[1])
            else:
                print("//notFound:"+command_body)
            user_db[account].update_commands(command_sid)
        else:
            print("//skipping:"+command_body)

    print("mycommandlist final:")
    print user_db[account].command_sids
    return user_db

###############
#testingsection
class testmessage():
    def __init__(self, body, sid):
        self.body=body
        self.sid = sid
  
def testsetup():
    sentmessages={"one":"awertyui","two":"bASDFGHJKL","three":"cASDFGHJKL",
                       "four":"dQRTYUIOP"}
    messagelist=[]
    for body, sid in sentmessages.items():
        messagelist.append(testmessage(body, sid))
        
    quick_list=Quicklist("19705450436shop", messagelist,
                         "2014-01-01","2014-01-01")
    account=UserAccount("+19705450436","19705450436shop",
                         "2014-01-01","2014-01-01")
    command_list={"//list":"b09sd7f9a0sd7f","//clear":"a09sd7f9a0sd7f"}
    return account, command_list, quick_list

def testgo(account, command_list, quick_list):
    account=process_command_list(account, command_list, quick_list)

def runtest():
    account, command_list, quick_list = testsetup()
    for i in range(2):
        testgo(account, command_list, quick_list)
        i+=1
