import gspread
import smtplib
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta

# Define the credentials file and the sheet name
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/vahfanforever/source/emailer/birthdays/credentials.json', scope)
sheet_name = "birthdays"

# Connect to the Google Sheet
gc = gspread.authorize(credentials)
sheet = gc.open(sheet_name).sheet1

# Retrieve the data from the Google Sheet
data = sheet.get_all_records()

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
    if difference == timedelta(days=7):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("youremail@gmail.com", "yourpassword")
        
        message = "Subject: Reminder\n\nDear {0},\n\nThis is a reminder that your event is coming up in 7 days.\n\nBest"
