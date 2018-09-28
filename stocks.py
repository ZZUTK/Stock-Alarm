# load stock data
from collections import OrderedDict

stocks = {
    'AAPL':     {'name': 'Apple',   'threshold': 180},
    'AMZN':     {'name': 'Amazon',  'threshold': 1900},
    'GOOGL':    {'name': 'Google',  'threshold': 1180},
    'TSLA':     {'name': 'Tasla',   'threshold': 260},
    'NVDA':     {'name': 'Nvidia',  'threshold': 220},
    'FB':       {'name': 'FaceBook','threshold': 150},
}

stocks = OrderedDict(sorted(stocks.items(), key=lambda x: x[0]))
