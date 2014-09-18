from datetime import datetime

class TwilioList():
    def __init__(self, sid, from_, body, status):
        self.sid = sid
        self.from_ = from_
        self.body = body
        self.status = status

class UserAccount():
    def __init__(self, phone_number, current_list, date_created, date_accessed):
        self.phone_number=phone_number
        self.current_list = current_list
        self.date_created = date_created
        self.date_accessed = date_accessed
        self.command_sids = []

    def update_commands(self, command_sid):
        self.command_sids.append(command_sid)

    def swap_list(self, new_list):
        self.current_list = new_list

    def get_current_list(self):
        print("Current List = "+self.current_list)

    def show_account_info(self):
        print("phone number: "+self.phone_number)
        print("current list:"+self.current_list)
        print("date created: "+self.date_created)
        print("date accessed: "+self.date_accessed)


class Quicklist():
    def __init__(self, list_name, list_obj):
        self.list_name=list_name
        self.list_obj=list_obj
        self.date_created = datetime.utcnow().strftime("%Y-%m-%d")
        self.date_accessed = datetime.utcnow().strftime("%Y-%m-%d")

    def add_items(self, list_new):
        self.list_obj += list_new
        
    def clear_list(self):
        self.list_obj = []

    def list_as_str(self):
        message_string='<' + self.list_name + '>\n'
        for message in self.list_obj:
            message_string += '\n' + message
        return message_string

    #Prints the list, if commands exist they are omitted
    def print_body(self):
        for message in self.list_obj:
            print message

    #Prints all command messages on the list
    def print_commands(self):
        for message in self.list_obj:
            if message.body[:2] == "//":
                print message.body

                
