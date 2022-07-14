from fastapi import FastAPI, Depends
import requests
import json
# set to today 


app = FastAPI()

url = "https://api.apilayer.com/exchangerates_data/convert?to=EUR&from=USD&amount=1"

payload = {}
headers= {
  "apikey": "BzBwcOYZtoPuGSspEZkc5B6poXqOaS48"
}

def get_currency_rate(url): 

  payload = {}
  headers= {
    "apikey": "BzBwcOYZtoPuGSspEZkc5B6poXqOaS48"
  }

  response = requests.request("GET", url, headers=headers, data = payload)


  status_code = response.status_code
  result = response.text
  result_split = str(result).splitlines()[-2]
  return result_split

@app.get("/api/convert")
def currency_exchange_rate(origin_country, destination_country):
    url = f"https://api.apilayer.com/exchangerates_data/convert?to={origin_country}&from={destination_country}&amount=1"
    currency_rate = get_currency_rate(url)  
    return currency_rate


# API call output 

# {
#     "success": true,
#     "query": {
#         "from": "USD",
#         "to": "EUR",
#         "amount": 1
#     },
#     "info": {
#         "timestamp": 1657670399,
#         "rate": 0.997805
#     },
#     "date": "2022-07-11",
#     "result": 0.997805
# }
