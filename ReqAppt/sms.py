# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from users_acc import models

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = 'ACd7bc48747087d5cf69476e8e4cd73851'
auth_token = '700d7041460f3648edb6e1c17b2a5083'
client = Client(account_sid, auth_token)




def send_message(apptDate, apptHour):

        field_name = 'phone_no'
        obj = models.User.objects.first()
        field_value = getattr(obj, field_name)
        print(field_value)

        message = client.messages \
                        .create(
                             # body="Your Appointment On " + apptDate + " at " + apptHour + " has been scheduled ",
                             body = f"Your Appointment On , {apptDate} at {apptHour}am has been scheduled"
                                    f" we will notify you when it's confirmed by the provider"
                                    f" you will receive the zoom link when provider confirms your appointment "
                                    f"(Reply STOP to unsubscribe from Treeo Alerts. Msg&Data Rates May Apply.)",
                             from_= '+16085808427',
                             to= f'+1{field_value}'
                        )


        print(message.sid)




def approve_message():
        message = client.messages \
                        .create(
                        # body="Your Appointment On " + apptDate + " at " + apptHour + " has been scheduled ",
                        body=f"Your Appointment with Treeo provider has been approved, you will receive "
                             f"a zoom link shortly",
                        from_='+16085808427',
                        to='+12487787388'
                    )

        print(message.sid)


def reject_message():
        message = client.messages \
                        .create(
                        # body="Your Appointment On " + apptDate + " at " + apptHour + " has been scheduled ",
                        body=f"Your Appointment with Treeo provider has been cancelled, the provider will contact "
                             f"you shortly.",
                        from_='+16085808427',
                        to='+12487787388'
                    )

        print(message.sid)

