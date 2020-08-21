"""Sends an email when a result hits"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from helpers import get_default

PASSWORD = get_default('email_password')
SRC_EMAIL = get_default('source_email')
DEST_EMAIL = get_default('dest_email')


def send_email(body=None):
    """Sends an email using a gmail email"""
    sender_address = SRC_EMAIL
    sender_pass = PASSWORD
    receiver_address = DEST_EMAIL

    message = MIMEMultipart()
    message.attach(MIMEText(body, 'plain'))
    message = message.as_string()

    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_address, sender_pass)
    session.sendmail(sender_address, receiver_address, message)
    session.quit()
    print(f'mail sent to {DEST_EMAIL} - {body}')
