import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os


async def send_mail(receiver: str, subject: str, content: str, filename: str, sentfilename: str):
    msg = MIMEMultipart()
    password = os.getenv("EMAIL_PASSWORD")
    sender_adr = os.getenv("EMAIL_ADRESS")
    msg['to'] = receiver
    msg['subject'] = subject
    body = MIMEText(content, 'plain')
    msg.attach(body)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    with open(filename, 'rb') as f:
        attachement = MIMEApplication(f.read())
        attachement['content-disposition'] = 'attachement;filename="{}"'.format(
            os.path.basename(sentfilename))
    msg.attach(attachement)
    server.login(sender_adr, password)
    server.send_message(
        msg)
