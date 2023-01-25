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

    #"url" should contain the product page url of your product of choice
    #"phrase" should be a word for word copy of the product page's 0 stock text label

    global log
    url = "https://insertyourproducturlhere.com"
    phrase = "Availability: 0 left in stock"
    available = check_availability(url, phrase)

    # After an availability check, log.txt will be filled by an inventory status output given the entered values above
    # If a product is in stock, and email will be sent to credentials given in config.json - Note that gmail requires app passwords instead of your original password for the bot to properly sign in

    logfile = open('log.txt', 'r+')
    
    successmessage = "Product in stock!"
    if successmessage in logfile.read():
        print("Product has been found in stock. ")
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
        msg['Subject'] = "Product in stock "
        msg['From'] = fromAddress
        msg['To'] = toAddress
        msg.set_content("The product you've been watching has been found in stock! " + url)
        
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
        log += "Product not available. "
    logfile.write(str(datetime.now()) + " " + log + "\n")
    logfile.close()
        

if __name__ == '__main__':
    main()

    