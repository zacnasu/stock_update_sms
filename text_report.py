from stock_info import get_portfolio_data
import json
from twilio.rest import Client
import schedule
import time

def get_text_info():
    portfolio_data = get_portfolio_data()
    portfolio_data['percent_change'] = 1 - portfolio_data['close_total']/portfolio_data['open_total']
    text_string = """Hey you Fool! Here is your daily update:
Percent Change: {:.2%}
Absolute Change: {:,}USD
Open: {:,}USD
Close: {:,}USD
""".format(portfolio_data['percent_change'],
        round(portfolio_data['absolute_change'], 2),
        round(portfolio_data['open_total'], 2),
        round(portfolio_data['close_total'], 2))

    for stock in portfolio_data['stocks'].keys():
        text_string += "{}: {:.2%}\n".format(stock, portfolio_data['stocks'][stock]['percent_change'])
    return text_string

def send_text_info():
    file = open('config.json',)
    config_data = json.load(file)
    file.close()
    client = Client(config_data['twilio_account'], config_data['twilio_token'])
    text = get_text_info()
    for number in config_data['to_number']:
        message = client.messages.create(to=number,
                                        from_=config_data['from_number'],
                                        body=text)

def setup_daily_text():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every().day.at("18:00").do(send_text_info)

if __name__ == "__main__":
    setup_daily_text()
