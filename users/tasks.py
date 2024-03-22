from django.core.mail import send_mail
from goodreads.celery import app

@app.task()
def send_email(subject, message, resipient_list):
    send_mail(
        subject,
        message,
        "j.hojibayev@tuit.uz",
        resipient_list,
    )

