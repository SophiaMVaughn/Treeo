from celery import shared_task
from ReqAppt.models import *
from .email import *
from .sms import *
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
        logger.info('Failed to Send SMS Messages for Appointment:'+str(aptobj.id))

@shared_task(name='Treeo.tasks.send_mail_task')
def send_mail_task(subject,message,site_server,recepient):
    send_mail(
        subject,
        message,
        site_server,
        recepient,
        fail_silently=False,
    )