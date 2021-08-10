import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

news_parameters = {
    'q': COMPANY_NAME,
    'apiKey': "_key",
}
stock_parameters = {
    'function': "TIME_SERIES_DAILY",
    'symbol': STOCK_NAME,
    'interval': "5min",
    'apikey': "_key"
}

response_stock = requests.get(STOCK_ENDPOINT, params=stock_parameters)
file = response_stock.json()
data = file["Time Series (Daily)"]
closing_stock = [value for (key, value) in data.items()]
yesterday_closing = closing_stock[0]["4. close"]
before_yesterday_close = closing_stock[1]["4. close"]
difference = float(yesterday_closing) - float(before_yesterday_close)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage = round((difference / float(yesterday_closing)) * 100)
if abs(percentage) > 5:
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][:3]

    news = [f"\n{STOCK_NAME}: {up_down}{percentage}%\nHeadline: {h['title']} \n\nBrief: {h['description']}\n" for h in news_data]

    account_sid = "___your_key____"
    auth_token = "__token___"
    client = Client(account_sid, auth_token)
    for h in news:
        message = client.messages \
            .create(
            body=h,
            from_='+mobile_no',
            to='+mobile_no'
        )
        print(message.status)