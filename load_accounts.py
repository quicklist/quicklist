from datetime import datetime
from quicklist import UserAccount,Quicklist
"""
    read the accounts and initalize the lists
"""
def get_account_list(twilio_messages):
    account_names = []
    date_created = datetime.utcnow().strftime("%Y-%m-%d")
    date_accessed = date_created
    last_message_sid = ''
    for message in twilio_messages:
        if not last_message_sid and message.status=='received':
            last_message_sid = message.sid
        if message.from_ not in account_names and message.status=='received':
            account_names.append(message.from_)
    return account_names, last_message_sid

def init_accounts(user_db, account_names, default_name):
    date_created = datetime.utcnow().strftime("%Y-%m-%d")
    date_accessed = date_created
    
    for account_name in account_names:
        elevendigit = account_name[1:]
        current_list = elevendigit + default_name
        if elevendigit not in user_db.keys():
            new_account = UserAccount(account_name, current_list, date_created, date_accessed)
            user_db[elevendigit] = new_account
    return user_db
