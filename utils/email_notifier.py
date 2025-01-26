# utils/email_notifier.py
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


def send_email_notification(subject: str, body: str) -> None:
    msg = MIMEMultipart()
    msg["From"] = os.getenv("SENDER_EMAIL")
    msg["To"] = os.getenv("RECIPIENT_EMAILS")
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(
        os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT", 587))
    ) as server:
        server.starttls()
        server.login(os.getenv("SENDER_EMAIL"), os.getenv("SMTP_PASSWORD"))
        server.send_message(msg)
