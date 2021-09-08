import requests
import json

def get_stock_info(symbol):
    file = open('config.json',)
    config_data = json.load(file)
    
    querystring = {"symbol":symbol,"region":"US"}

    headers = {
        "x-rapidapi-host": config_data['x-rapidapi-host'],
        "x-rapidapi-key": config_data['x-rapidapi-key']
    }

    response = requests.request("GET", config_data['url'], headers=headers, params=querystring)
    response_dict = response.json()
    # print(response.text)
    return_dictionary = {
        "absolute_change": response_dict['price']['regularMarketChange']['raw'],
        "percent_change": response_dict['price']['regularMarketChangePercent']['raw'],
        "open": response_dict['price']['regularMarketOpen']['raw'],
        "close": response_dict['price']['regularMarketPrice']['raw']
    }
    file.close()
    return return_dictionary

def get_portfolio_data():
    file = open('config.json',)
    config_data = json.load(file)
    file.close()
    return_data = {
        "absolute_change": 0,
        "percent_change": 0,
        "open_total": 0,
        "close_total": 0,
        "stocks": {}
    }
    
    for stock in config_data["stocks"]:
        #ssd stands for single stock data
        ssd = get_stock_info(stock['symbol'])
        return_data['absolute_change'] += (ssd['absolute_change'] * stock['share_count'])
        return_data['open_total'] += ssd['open'] * stock['share_count']
        return_data['close_total'] += ssd['close'] * stock['share_count']
        return_data['stocks'][stock['symbol']] = ssd

    
    return return_data