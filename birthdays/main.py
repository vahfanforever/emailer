import gspread
import smtplib
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# Define the credentials file and the sheet name
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/vahfanforever/source/emailer/birthdays/credentials.json', scope)
sheet_name = "birthdays"

with open("/home/vahfanforever/source/emailer/birthdays/email_credentials.json", 'r') as file:
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
    date = row['Date']
    name = row['Name']
    
    # Parse the date string and compare to today's date
    date = datetime.strptime(date, '%d-%m').date()
    date = date.replace(year=2023)
    today = datetime.now().date()
    difference = date - today
    
    # If the difference is equal to 7, send an email
    if difference <= timedelta(days=14):
        info = {}
        info["date"] = date
        info["time_until"] = difference
        birthdays[name] = info

if birthdays:
    message = [f"oi u fat fuck it's {name}'s birthday on: {info['date']} -- that's in {info['time_until']} days!!!" for name, info in birthdays.items()]
    connection = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    connection.login(email, password)
    connection.sendmail(from_addr=email, to_addrs=email, msg='\n'.join(message))
    connection.close()