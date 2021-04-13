
from django.shortcuts import render, redirect, get_object_or_404

from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from patient_log.models import *
from Treeo import email_info
from users_acc import models
# import zoom
from .utils import generate_zoom


# zoom_link = generate_zoom(request=1)


def scheduled_mail_both(apt):

    subject = "Appointment Scheduled"
    message = "Your appointment with the patient has been scheduled. Please review and approve " \
              "the appointment at your earliest convenience."
    send_mail(
        subject,
        message,
        email_info.EMAIL_HOST_USER,
        [apt.provider.user.email],
        fail_silently=False,
    )

    message = "Your appointment with the Treeo provider has been scheduled." \
              " You will be notified once it is approved by the provider."
    send_mail(
        subject,
        message,
        email_info.EMAIL_HOST_USER,
        [apt.patient.user.email],
        fail_silently=False,
    )


def approved_mail_both(apt,patient_pwd):


    subject = "Appointment Confirmed"
    message = f"You approved the meeting with your patient. Use this Zoom link to start the meeting {apt.meeturlprovider}"

    send_mail(
        subject,
        message,
        email_info.EMAIL_HOST_USER,
        [apt.provider.user.email],
        fail_silently=False,
    )
    message = f"Your appointment has been approved by the provider. " \
              f"The password for your Zoom appointment is: '{patient_pwd}'. Use this link to enter the meeting: " + apt.meeturlpatient
    send_mail(
        subject,
        message,
        email_info.EMAIL_HOST_USER,
        [apt.patient.user.email],
        fail_silently=False,
    )

    print("Email succesfully delivered")


def reject_mail_both(apt):

    subject = "Appointment Cancelled"
    message_for_patient = f"Your appointment with the Treeo provider " \
                          f"has been cancelled. " \
                          f"You will receive a message from your provider shortly. "
    message_for_provider = f"You cancelled your appointment with the patient." \
                           f" Please notify your patient."
    send_mail(
        subject,
        message_for_provider,
        email_info.EMAIL_HOST_USER,
        [apt.provider.user.email],
        fail_silently=False,
    )
    send_mail(
        subject,
        message_for_patient,
        email_info.EMAIL_HOST_USER,
        [apt.patient.user.email],
        fail_silently=False,
    )

    print("Email succesfully delivered")
