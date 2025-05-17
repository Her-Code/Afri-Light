from threading import Thread
from flask_mail import Message
from flask import current_app
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, body):
    app = current_app._get_current_object()
    msg = Message(subject=subject, recipients=recipients, body=body)
    Thread(target=send_async_email, args=(app, msg)).start()
