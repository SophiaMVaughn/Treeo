# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from users_acc import models
from django.utils import timezone
import datetime
from twilio.twiml.voice_response import VoiceResponse, Say

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = 'ACd7bc48747087d5cf69476e8e4cd73851'
auth_token = 'd72c441bc1d3f031a75224a9eefac411'
client = Client(account_sid, auth_token)


def tfa_call(phone_no, token):
    if phone_no is not None:
        print(phone_no.as_e164)
        #to change the speed of the calls requires
        message='<Response><Say voice="Polly.Joanna" loop="3">Hello,<break strength="x-weak" time="100ms"/>' \
                '<emphasis level="moderate">Your Two Factor Authentication Code is</emphasis>' \
                '<prosody rate="50%" > '
        for i in str(token):
            message+=i+'    '
        message+='</prosody><s>This Code will expire in 5 minuites. </s>' \
                '</Say></Response>'


        call = client.calls.create(twiml=message,
                            from_='+16085808427',
                            to=f'{phone_no.as_e164}',
                        )
        print(call.sid)
    else:
        print("No Phone")