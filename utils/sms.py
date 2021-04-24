# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
from users_acc import models
from django.utils import timezone
import datetime
# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure

account_sid = 'ACd7bc48747087d5cf69476e8e4cd73851'
auth_token = 'd72c441bc1d3f031a75224a9eefac411'
client = Client(account_sid, auth_token)




	#Author: Giorgi Nozadze
	#This method checks sends text message notifying appointment scheduling to both parties. sms is sent using twilio API, 
   # account information (if different is used) must be provided using line 9 and 10, if sms feature breaks it's most likely,
   # due to wrong auth_token or account_sid. entire feature depends on those 2 things so make sure they are correct

def send_message(aptobj):
    if aptobj.patient.user.phone_no is not None:
        print(aptobj.patient.user.phone_no.as_e164)
        message = client.messages \
            .create(
                # body="Your Appointment On " + apptDate + " at " + apptHour + " has been scheduled ",
                body=f"Your appointment On {aptobj.meetingDate.strftime('%A %B %d')} at {aptobj.meetingDate.strftime('%I:%M %p')} has been scheduled."
                f" We will notify you when it's confirmed by the provider."
                f" You will receive the Zoom link when provider confirms your appointment. "
                f"(Reply STOP to unsubscribe from Treeo Alerts. Msg&Data Rates May Apply.)",
                from_='+16085808427',
                to=f'{aptobj.patient.user.phone_no.as_e164}'
            )

        print(message.sid)
    else:
        print("No Phone")
    if aptobj.provider.user.phone_no is not None:
        print(aptobj.provider.user.phone_no.as_e164)
        message = client.messages \
            .create(
                # body="Your Appointment On " + apptDate + " at " + apptHour + " has been scheduled ",
                body=f"Your Appointment On {aptobj.meetingDate.strftime('%A %B %d')} at {aptobj.meetingDate.strftime('%I:%M %p')} has been scheduled."
                f" We will notify you when it's confirmed by the provider."
                f" You will receive the Zoom link when provider confirms your appointment. "
                f"(Reply STOP to unsubscribe from Treeo Alerts. Msg&Data Rates May Apply.)",
                from_='+16085808427',
                to=f'{aptobj.provider.user.phone_no.as_e164}'
            )

        print(message.sid)
    else:
        print("No Phone")

	#Author: Giorgi Nozadze
	#This method sends approval message via user provided phone numbers after the provider clicks approve message, sms is sent to both parties


def approve_message(aptobj):
    if aptobj.patient.user.phone_no is not None:
        print(aptobj.patient.user.phone_no.as_e164)
        message = client.messages \
                        .create(
                            # body="Your Appointment On " + apptDate + " at " + apptHour + " has been scheduled ",
                            body=f"Your Appointment On {aptobj.meetingDate.strftime('%A %B %d')} with your Treeo provider has been approved. You will receive "
                            f"a Zoom link shortly.",
                            from_='+16085808427',
                            to=f'{aptobj.patient.user.phone_no.as_e164}'
                        )

        print(message.sid)
    else:
        print("No Phone")

       
	#Author: Giorgi Nozadze
	#This method sends notification about rejction if provider doesn't approve the appointment


def reject_message(aptobj):
    if aptobj.patient.user.phone_no is not None:
        print(aptobj.patient.user.phone_no.as_e164)
        message = client.messages \
                        .create(
                            # body="Your Appointment On " + apptDate + " at " + apptHour + " has been scheduled ",
                            body=f"Your Appointment On {aptobj.meetingDate.strftime('%A %B %d')} with your Treeo provider has been cancelled. The provider will contact "
                            f"you shortly.",
                            from_='+16085808427',
                            to=f'{aptobj.patient.user.phone_no.as_e164}'
                        )

        print(message.sid)
    else:
        print("No Phone")


def target_time_print(apt):

    t = apt.meetingDate
    print(t)
    print(t.timestamp())
    time_left = t.timestamp() - timezone.now().timestamp()
    time_left = time_left - 10000
    print("time left until appointment")
    print(time_left)
    # t.strftime('%M/%d/%Y')
    # target_datetime = datetime.strptime(ApptTable.meetingDate, '%M/%d/%Y')
    # current_datetime = datetime.now() # No need to convert it to string
    # time_left = target_datetime - current_datetime # return `timedelta` object
    # print("#@*&#@*#&@*#&*@&#*@&#*@&#*#@")
    # # print(time_left.total_seconds())
    # print(ApptTable.meetingDate.total_seconds())
    #


# returns total seconds
