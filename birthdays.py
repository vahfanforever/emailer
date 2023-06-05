import json
import smtplib

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
from email.message import EmailMessage
import emoji

# Define the credentials file and the sheet name
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "/home/vahfanforever/source/emailer/credentials.json", scope
)
sheet_name = "birthdays"

with open("/home/vahfanforever/source/emailer/email_credentials.json", "r") as file:
    data = json.load(file)

email = data["address"]
password = data["password"]

# Connect to the Google Sheet
gc = gspread.authorize(credentials)
sheet = gc.open(sheet_name).sheet1

# Retrieve the data from the Google Sheet
data = sheet.get_all_records()


birthdays = {}

# Check each row of data for the specified date
for row in data:
    raw_date = row["Date"]
    name = row["Name"]

    # Parse the date string and compare to today's date
    raw_date = datetime.strptime(raw_date, "%d-%m").date()
    bday_date = raw_date.replace(year=2023)
    today = datetime.now().date()
    difference = bday_date - today

    # If the difference is equal to 7, send an email
    if (difference <= timedelta(days=14)) and (difference >= timedelta(days=0)):
        info = {}
        info["month"] = bday_date.strftime("%B")
        info["day"] = bday_date.strftime("%A")
        info["date"] = bday_date.strftime("%d")
        info["time_until"] = difference.days
        birthdays[name] = info

if birthdays:
    for name, info in birthdays.items():
        msg = EmailMessage()
        msg.set_content(
            f"\nOi you fuck it's {name}'s birthday on {info['day']} {info['date']} of {info['month']} which is in {info['time_until']} day(s)"
        )
        msg["Subject"] = emoji.emojize(":warning: birthday reminder :warning:")
        msg["From"] = email
        msg["To"] = email

        connection = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        connection.login(email, password)
        connection.send_message(msg)
        connection.close()
