from stocks import stocks
import json
from time import sleep
import smtplib
from email.mime.text import MIMEText
import urllib
from datetime import datetime
from threading import Thread
from collections import OrderedDict


class StockAlarm(Thread):
    # store stock prices, {ticker: [time_stamp, price]}
    price_table = OrderedDict()

    def __init__(self, ticker):
        """
        :param ticker: str, e.g., GOOGLE, AAPL, etc.
        """
        Thread.__init__(self)
        self.ticker = ticker
        self.is_active = True

        # add stock to price table
        if self.ticker not in StockAlarm.price_table:
            StockAlarm.price_table[self.ticker] = []

    def run(self):
        while self.is_active:
            data = StockAlarm.get_stock_price(ticker=self.ticker)
            if data:
                price = data[0][-1]
                StockAlarm.price_table[self.ticker] = [datetime.now().strftime("%Y-%m-%d %H:%M:%S"), price]
                if 0 < price <= stocks[self.ticker]['threshold']:
                    stocks[self.ticker]['threshold'] = price - .1
                    subject = '%s (%s) fell to $%.2f' % (stocks[self.ticker]['name'], self.ticker, price)
                    StockAlarm.send_email(subject=subject)
            sleep(5)

    def stop(self):
        self.is_active = False

    @staticmethod
    def get_stock_price(ticker, interval='Latest'):
        """
        :param ticker: str, the stock ticker name
        :param interval: str, ['Latest', 'Intraday', 'Daily', 'Weekly', 'Monthly']
        :return: list, [(date_time, open_price, close_price)]
        """

        # pre defined intervals
        intervals = {
            'Latest': 'GLOBAL_QUOTE',
            'Intraday': 'TIME_SERIES_INTRADAY',
            'Daily': 'TIME_SERIES_DAILY',
            'Weekly': 'TIME_SERIES_WEEKLY',
            'Monthly': 'TIME_SERIES_MONTHLY'
        }

        # check input arguments
        assert isinstance(ticker, str)
        assert isinstance(interval, str)
        if interval not in intervals:
            raise Exception('INTERVAL must be in %s' % str(intervals.keys()))

        # personal key obtained from https://www.alphavantage.co/
        api_key = '67HCBBBVFYQM9LYZ'

        # construct the request
        url = 'https://www.alphavantage.co/query?' \
              'function=%s&' \
              'symbol=%s&' \
              'apikey=%s&' \
              'outputsize=compact&' \
              'datatype=json&' \
              'interval=1min&' % \
              (intervals[interval], ticker, api_key)

        # request data
        fp = urllib.urlopen(url)
        response_data = json.loads(fp.read().decode('utf8'))
        fp.close()

        # target the price data
        price_data = []
        for key in response_data:
            if 'Meta Data' not in key:
                price_data = response_data[key]
                break

        time_stamp = []
        price_open = []
        price_close = []

        if interval == 'Latest':
            for key in price_data:
                if 'day' in key:
                    time_stamp.append(price_data[key])
                elif 'open' in key:
                    price_open.append(float(price_data[key]))
                elif 'price' in key:
                    price_close.append(float(price_data[key]))
        else:
            for date_time in price_data:
                time_stamp.append(date_time)
                for key in price_data[date_time]:
                    if 'open' in key:
                        price_open.append(float(price_data[date_time][key]))
                    elif 'close' in key:
                        price_close.append(float(price_data[date_time][key]))

        date_price = zip(time_stamp, price_open, price_close)
        date_price = sorted(date_price, key=lambda x: x[0], reverse=True)

        return date_price

    @staticmethod
    def send_email(subject=None, content=None, to_addrs='zhifei.zhang.vip@gmail.com'):
        """
        :param subject: str, subject of the email
        :param content: str, content of the email
        :param to_addrs: str, email address of the receiver
        """

        # sender email and password
        my_address = 'dounjeff@gmail.com'
        pwd = 'S871005y@ge'

        # prepare the message
        msg = MIMEText(content)
        msg['Subject'] = subject
        msg['From'] = 'Stock Alarm'
        msg['To'] = 'Stocker'

        # login to Gmail server and send the email
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        server.ehlo()
        server.starttls()
        server.login(user=my_address, password=pwd)
        server.sendmail(from_addr=my_address, to_addrs=to_addrs, msg=msg.as_string())
        server.close()


if __name__ == '__main__':
    import os
    print('Querying your stocks ...')
    stock_alarms = []
    for ticker in stocks:
        stock_alarms.append(StockAlarm(ticker))
        stock_alarms[-1].start()
        # sleep(5)

    try:
        head = '{:^15}{:>10}{:>12}{:^30}\n{:-<67}\n'.format('Company', 'Price($)', 'Alarm($)', 'Last Update', '')
        line_format = '{:^15}{:10.2f}{:12.2f}{:^30}\n'
        lines_pre = head
        while True:
            lines = head
            for ticker in StockAlarm.price_table:
                if StockAlarm.price_table[ticker]:
                    lines += line_format.format(
                        stocks[ticker]['name'],
                        StockAlarm.price_table[ticker][-1],
                        stocks[ticker]['threshold'],
                        StockAlarm.price_table[ticker][0]
                    )
            if lines != lines_pre:
                lines_pre = lines
                os.system('cls')
                print(lines)

            sleep(5)
    except KeyboardInterrupt:
        for stock_alarm in stock_alarms:
            stock_alarm.stop()
