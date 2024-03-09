from celery import shared_task
from django.core.mail import EmailMessage


@shared_task(name="Send Email Notification")
def send_email_notification(
        emails, 
        subject, 
        body, 
        bcc=None, 
        connection=None, 
        attachments=None, 
        headers=None,
        cc=None,
        reply_to=None,
    ):
    email = EmailMessage(
        subject=subject,
        body=body,
        to=emails,
        bcc=bcc,
        connection=connection,
        attachments=attachments,
        headers=headers,
        cc=cc,
        reply_to=reply_to,
    )
    email.send()
