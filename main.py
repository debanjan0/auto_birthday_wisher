
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymongo
import schedule


today = datetime.date.today() 

current_year = today.year
current_month = today.month
current_day = today.day
myclient = pymongo.MongoClient("<connection url>")
mydb = myclient["DoB"]
bdate = mydb["Birthdays"]
inputs = ["name", "dob(dd-mm-yyyy)", "mail"]

body = '''Thinking of you on your birthday, and wishing you all the best!
I hope it is as fantastic as you are!😊'''
sender = '<your mail>'
password = '<your app password from google>'

def add_dates():
    l = {}
    for i in inputs:
        val = input(i+" : ")
        l[i] = val
    x = bdate.insert_one(l)

    print(x.acknowledged)


def birth_dates():
    dates = []
    val = bdate.find({},{"_id": 0})
    for i in val:
        dates.append((i['dob(dd-mm-yyyy)'],i["name"],i["mail"]))
    
    return dates


def mail_invoice(receiver,name):
    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = receiver
    message['Subject'] = 'Happy Birthday '+ name
    message.attach(MIMEText(body, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender, password)
    text = message.as_string()
    session.sendmail(sender, receiver, text)
    session.quit()
    print('Mail Sent')


def main():
    dates = birth_dates()

    for i in dates:
        d,m,y = i[0].split('-')
        if int(d) == current_day and int(m) == current_month:
            print("Happy Birthday "+i[1])
            mail_invoice(i[2],i[1])
            print("main sent")
            print("\n")

    


if __name__ == "__main__":
    schedule.every().day.at("09:00").do(main) # This will check and every day at 9am and send mail if any birthday is there
    add_dates() # To add dates in the database
    
