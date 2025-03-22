#!/home/mathias/Desktop/scrape-appartment-waitinglist/venv/bin/python3
import os
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time
import urllib3
from dotenv import load_dotenv
urllib3.disable_warnings()
# Load environment variables from .env file
load_dotenv()
import logging
logging.basicConfig(filename='/home/mathias/Desktop/scrape-appartment-waitinglist/scrape.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def send_mail(mail_text, subject="Change Detected on Findbolig.nu!"):
    gmail_account = os.getenv('EMAIL')
    password = os.getenv('EMAIL_PASSWORD')
    
    if not gmail_account or not password:
        logging.info("Error: EMAIL or EMAIL_PASSWORD environment variables not set.")
        return False
    
    msg = MIMEText(mail_text)
    msg['Subject'] = subject
    msg['From'] = gmail_account
    msg['To'] = gmail_account

    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(gmail_account, password)
        server.send_message(msg)
        print(f"Email sent successfully")
        return True
    except Exception as e:
        logging.info(f"Failed to send email: {e}")
        return False
    finally:
        server.quit()

def get_website_content(url):
    try:
        response = requests.get(url, verify=False)  #verify=False
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        signup_text= soup.find_all("div", {"class": "c-article-top__heading--3 o-heading o-heading--size-3 o-heading--ocean-darker"})

        if signup_text:
            div = signup_text[0]
            p_tag = div.find("p")
            if p_tag.text == "Lukket for opskrivning":
                logging.info("Nothing has changed")
            else:
                print("Now sending a mail:")
                send_mail("The following website has changed\n" + url)
        else:
            send_mail("The following website has changed\n" + url)

    except requests.RequestException as e:
        logging.info(f"requests.RequestException: {url}: {e}")
        return f"requests.RequestException: {e}"

urls = ["https://www.findbolig.nu/da-dk/udlejere/oestergaarden/ekstern-venteliste",
        "https://www.findbolig.nu/da-dk/udlejere/solgaarden/ekstern-venteliste",
        "https://www.findbolig.nu/da-dk/udlejere/arendal/ekstern-venteliste"
        ]

def run_bot(urls):
    for url in urls:
        get_website_content(url)
        time.sleep(2)
run_bot(urls)