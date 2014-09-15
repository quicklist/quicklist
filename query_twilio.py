from twilio import rest
from twilio.rest import resources
from datetime import datetime, timedelta
"""

"""
def twilio_read_all_today():
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "ACe8d4e2f063204af810112a83eca781f7"
    auth_token  = "5b43e658f8d01a0fa8298d3064fc63db"
    client = rest.TwilioRestClient(account_sid, auth_token)
     
    #read all messages with today's date
    utc_time = datetime.utcnow() - timedelta(days=1)
    utc_time_str = utc_time.strftime("%Y-%m-%d")
    #Messages takes four arguments from_=None, before=None, after=None, date_sent=None
    messages = client.messages.list(after=utc_time_str)
    return messages

def twilio_send_list(to_number, message):
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "ACe8d4e2f063204af810112a83eca781f7"
    auth_token  = "5b43e658f8d01a0fa8298d3064fc63db"
    client = rest.TwilioRestClient(account_sid, auth_token)
    #message_string = '\n'.join(message_list)
    message = client.messages.create(body=message,
        to=to_number,    # Replace with your phone number
        from_="+13393685588") # Replace with your Twilio number
