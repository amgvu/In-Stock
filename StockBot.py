import json
import smtplib
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
from email.message import EmailMessage

log = ""

def check_availability(url, phrase):
    global log
    try:
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, features='html.parser')
        if phrase in soup.text:
            return False
        return True
    except:
        log += "Error parsing site"


def main():
    global log
    url = "https://fakeitem.com"
    phrase = "Availability: 0 left in stock"
    available = check_availability(url, phrase)

    logfile = open('log.txt', 'r+')
    
    successmessage = "PRODUCT IN STOCK"
    if successmessage in logfile.read():
        print("PRODUCT ALREADY FOUND IN STOCK ")
        return

    if available:
        log += successmessage
        try:
            with open('config.json') as file:
                config = json.load(file)
                username = config['username']
                password = config['password']
                fromAddress = config['fromAddress']
                toAddress = config['toAddress']
        except:
            log += "Error with credentials "


        msg = EmailMessage()
        msg['Subject'] = "PRODUCT IS IN STOCK "
        msg['From'] = fromAddress
        msg['To'] = toAddress
        msg.set_content("It's back in stock. If you're reading this after an hour. My condolences." + url)
        
        try:
            server = smtplib.SMTP('smtp.', 587)
            server.ehlo()
            server.starttls()
            server.login(username, password)

            server.send_message(msg)
            server.quit()
            log += "Message sent "
        except:
            log += "Error sending message "
    
    else:
        log += "No products are available "
    logfile.write(str(datetime.now()) + " " + log + "\n")
    logfile.close()
        

if __name__ == '__main__':
    main()

    