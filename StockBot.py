import json
import smtplib
import urllib.request
from datetime import datetime
from bs4 import BeautifulSoup
from email.message import EmailMessage

# Global variable to store log messages
log = ""

def check_availability(url, phrase):
    # Function to check if a product is in stock by looking for an out-of-stock phrase
    global log
    try:
        # Fetch and parse the webpage
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, features='html.parser')
        # Check if the out-of-stock phrase exists on the page
        if phrase in soup.text:
            return False
        return True
    except:
        log += "Error parsing site"

def main():
    global log

    # Configuration variables
    url = "https://insertyourproducturlhere.com"
    phrase = "Availability: 0 left in stock"

    # Check current availability
    available = check_availability(url, phrase)

    # Open log file to check if we've already found the product in stock
    logfile = open('log.txt', 'r+')
    
    # Check if we've already logged that the product is in stock
    successmessage = "Product in stock!"
    if successmessage in logfile.read():
        print("Product has been found in stock. ")
        return

    if available:
        # Product is available - prepare to send notification
        log += successmessage
        try:
            # Load email configuration from config.json
            with open('config.json') as file:
                config = json.load(file)
                username = config['username']
                password = config['password']
                fromAddress = config['fromAddress']
                toAddress = config['toAddress']
        except:
            log += "Error with credentials "

        # Prepare email message
        msg = EmailMessage()
        msg['Subject'] = "Product in stock "
        msg['From'] = fromAddress
        msg['To'] = toAddress
        msg.set_content("The product you've been watching has been found in stock! " + url)
        
        # Attempt to send email notification
        try:
            # Connect to SMTP server - Add your email domain after 'smtp.(_____)'
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls() # Enable TLS encryption
            server.login(username, password)

            # Send email and close connection
            server.send_message(msg)
            server.quit()
            log += "Message sent "
        except:
            log += "Error sending message "
    
    else:
        # Product is not available
        log += "Product not available. "

    # Log the result with timestamp
    logfile.write(str(datetime.now()) + " " + log + "\n")
    logfile.close()
        
if __name__ == '__main__':
    main()

    