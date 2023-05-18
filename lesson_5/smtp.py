import smtplib, os
from email.message import EmailMessage
import re

def check_len(message: str, limit: int) -> bool:
    if len(message) > limit or len(message) == 0:
        return False
    else:
        return True


def is_email(adress: str) -> bool:
    result = re.findall(r'^[a-zA-Z0-9._-]+@[a-zA-Z-]+\.[a-zA-Z-]+$', adress)
    if len(result) == 1:
        return True
    else:
        return False


def send_mail(message: str, subject: str, to_email: str) -> bool:
    sender = os.environ.get('SMTP_EMAIL')
    password = os.environ.get('SMTP_PASSWORD')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email
    try:
        server.login(sender, password)
        server.send_message(msg)
        return True
    except Exception as error:
        print(f'Error: {error}')
        return False
