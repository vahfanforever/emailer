from datetime import datetime, time
import json
import smtplib

from email.message import EmailMessage
import emoji

email_time_start = time(21, 0)
email_time_end = time(22, 0)
email_day = 1

today = datetime.now()
if (
    today.weekday() == email_day
    and today.time() > email_time_start
    and today.time() < email_time_end
):
    with open("/home/vahfanforever/source/emailer/email_credentials.json", "r") as file:
        data = json.load(file)

    email = data["address"]
    password = data["password"]
    msg = EmailMessage()
    msg.set_content(emoji.emojize("take out the rubbish queen :sparkling_heart:"))
    msg["Subject"] = emoji.emojize(":wastebasket: :warning:")
    msg["From"] = email
    msg["To"] = email

    connection = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    connection.login(email, password)
    connection.send_message(msg)
    connection.close()
