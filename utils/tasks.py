from celery import shared_task
from ReqAppt.models import *
from smtplib import SMTP
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from utils.email import *
from utils.sms import *
# from .views import archive_apt
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(name='Treeo.tasks.send_message_task')
def send_message_task(aptobj_id):
    try:
        aptobj = ApptTable.objects.get(pk=aptobj_id)
        x=send_message(aptobj)
        for i in x:
            logger.info(i)
    except:
        logger.info('Failed to Send SMS Messages for Appointment:'+str(aptobj.id))


@shared_task(name='Treeo.tasks.scheduled_mail_both_task')
def scheduled_mail_both_task(aptobj_id):
    try:
        aptobj = ApptTable.objects.get(pk=aptobj_id)
        x=scheduled_mail_both(aptobj)
        for i in x:
            logger.info(i)
    except:
        logger.info('Failed to Send Email Messages for Appointment:'+str(aptobj.id))

@shared_task(name='Treeo.tasks.send_mail_task')
def send_mail_task(subject,message,site_server,recepient):
    send_mail(
        subject,
        message,
        site_server,
        recepient,
        fail_silently=False,
    )


@shared_task(name='Treeo.tasks.approve_message_task')
def approve_message_task(aptobj_id):
    try:
        aptobj = ApptTable.objects.get(pk=aptobj_id)
        x=approve_message(aptobj)
        for i in x:
            logger.info(i)
    except:
        logger.info('Failed to Send SMS Messages for Appointment Approval:'+str(aptobj_id))

@shared_task(name='Treeo.tasks.reject_message_task')
def reject_message_task(aptobj_id):
    try:
        aptobj = ApptTable.objects.get(pk=aptobj_id)
        x=reject_message(aptobj)
        for i in x:
            logger.info(i)
    except:
        logger.info('Failed to Send SMS Messages for Appointment Rejection:'+str(aptobj_id))

@shared_task(name='Treeo.tasks.approved_mail_both_task')
def approved_mail_both_task(aptobj_id,patients_pwd):
    try:
        aptobj = ApptTable.objects.get(pk=aptobj_id)
        x=approved_mail_both(aptobj,patients_pwd)
        for i in x:
            logger.info(i)
    except:
        logger.info('Failed to Send Email Messages for Appointment Approval:'+str(aptobj_id))

@shared_task(name='Treeo.tasks.delete_mail_both_task')
def reject_mail_both_task(aptobj_id):
    try:
        aptobj = ApptTable.objects.get(pk=aptobj_id)
        x=reject_mail_both(aptobj)
        for i in x:
            logger.info(i)
    except:
        logger.info('Failed to Send Email Messages for Appointment Rejection:'+str(aptobj_id))


@shared_task(name='Treeo.tasks.send_message_task')
def archive_apt_task(aptobj_id):
    try:
        aptobj = ApptTable.objects.get(pk=aptobj_id)
        x=archive_apt(aptobj)
        for i in x:
            logger.info(i)
    except:
        logger.info('Archive Appointment:'+str(aptobj.id))