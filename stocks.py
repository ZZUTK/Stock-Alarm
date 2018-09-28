# examples of stock data
from collections import OrderedDict

# add or remove lines in the dictionary of stocks
# note that the keys are stock symbols --- unique identifier
# 'name' is for your convenience of recognizing a stock
# 'threshold' is the low price trigger for sending alert to you
stocks = {
    'AAPL':     {'name': 'Apple',   'threshold': 180},
    'AMZN':     {'name': 'Amazon',  'threshold': 1900},
    'GOOGL':    {'name': 'Google',  'threshold': 1180},
    'TSLA':     {'name': 'Tesla',   'threshold': 260},
    'NVDA':     {'name': 'Nvidia',  'threshold': 220},
    'FB':       {'name': 'FaceBook','threshold': 150},
}

stocks = OrderedDict(sorted(stocks.items(), key=lambda x: x[0]))
