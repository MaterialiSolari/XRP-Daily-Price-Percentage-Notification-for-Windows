from datetime import datetime
import requests
from bs4 import BeautifulSoup
import time
from plyer import notification
import schedule

def app():
    now = datetime.now()
    url = requests.get('https://coinmarketcap.com/currencies/xrp/')
    soup = BeautifulSoup(url.text, 'html.parser') 
    current_price = soup.find('span', class_='sc-f70bb44c-0 jxpCgO base-text')

    percentage = soup.find('p', class_="sc-4984dd93-0 sc-58c82cf9-1 fwNMDM")
    data_change, color = percentage.get('data-change'), percentage.get('color')

    current_percentage = percentage.text.strip()

    if (data_change == 'down' and color == 'red') and current_price: 
        result = f'Today the percentage decreased by {current_percentage}\nThe current price of XRP: {current_price.text.strip()}'

    elif (data_change == 'up' and color == 'green') and current_price:
        result = f'Today the price increased by {current_percentage}\nThe current price of XRP: {current_price.text.strip()}'
    else:
        result = 'No price found'

    notification.notify(
        title="Price Update!",
        message=result,
        app_name='XRP Price',
        timeout=10
    )

def job():
    print("Running job...")
    app()

schedule.every().day.at("03:00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)