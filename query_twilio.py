from twilio import rest
from twilio.rest import resources
from datetime import datetime, timedelta
"""

"""
def twilio_read_all_today():
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = ""
    auth_token  = ""
    client = rest.TwilioRestClient(account_sid, auth_token)
     
    #read all messages with today's date
    utc_time = datetime.utcnow() - timedelta(days=1)
    utc_time_str = utc_time.strftime("%Y-%m-%d")
    #Messages takes four arguments from_=None, before=None, after=None, date_sent=None
    try:
        messages = client.messages.list(after=utc_time_str)
    except:
        e = sys.exc_info()[0]
        print("T W I L I O  C L I E N T  E R R O R: ", e)
        return None, False
    return messages, True

def twilio_send_list(to_number, message):
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = ""
    auth_token  = ""
    client = rest.TwilioRestClient(account_sid, auth_token)
    #message_string = '\n'.join(message_list)
    message = client.messages.create(body=message,
        to=to_number,    # Replace with your phone number
        from_="+13393685588") # Replace with your Twilio number
