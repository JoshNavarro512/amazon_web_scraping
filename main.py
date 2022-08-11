from urllib import response
from bs4 import BeautifulSoup
import requests
import lxml
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from dotenv import load_dotenv  

load_dotenv()


# The AMAZON URL for the item the user wants 
URL = input("Please paste the URL of the item page: ")

# Twilio Access variables in .env file 
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv('AUTH_TOKEN')

# Request Headers for site page 
header = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Accept-Language" : "en-US,en;q=0.9"
}

# grabs HTML of the [page]
response = requests.get(URL, headers=header)
soup = BeautifulSoup(response.content, "lxml")


# Grab the price of the item from the site page 
price = soup.find(name="span", class_="a-offscreen").get_text()
price_without_currency = price.split("$")[1]
price_as_float = float(price_without_currency)
print(f"\nCurrent price is ${price_as_float}")


# Ge the amount to user wants to pay 
target_price = int(input("Now enter the price you wnat to pay: "))


# If the price of the item is equal to or less than the target
# price send text message to user to buy now 
if price_as_float <= target_price:
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
                .create(
                     body=f"BUY NOW the item you want is {price_as_float}",
                     from_='+12564491625',
                     to='+15128254626'
                 )

    print(message.status)