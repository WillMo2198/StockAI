import finnhub
from datetime import datetime
import matplotlib.pyplot as plt
import time
import html2text
from newsapi import NewsApiClient
from textblob import TextBlob
import nodebox_linguistics_extended as nle

print(nle.verb.infinitive('swimming'))
newsapi = NewsApiClient(api_key='afb1216809004e278263b3a8e9aebd7f')
h = html2text.HTML2Text()
h.ignore_links = True
finnhub_client = finnhub.Client(api_key="brb63dnrh5rb7je2ldkg")
candles = finnhub_client.stock_candles('MKSI', 'D', int(time.mktime(datetime.strptime('01/06/2021', "%m/%d/%Y").timetuple())), int(time.mktime(datetime.strptime('02/06/2021', "%m/%d/%Y").timetuple())))
print(candles)
dates = candles['t']
opened = candles['o']
closed = candles['c']
prices = [None]*(len(opened)+len(closed))
dates_opened = ['{0} - O'.format(str(datetime.fromtimestamp(i).date())) for i in dates]
dates_closed = ['{0} - C'.format(str(datetime.fromtimestamp(i).date())) for i in dates]
dates = [None]*(len(dates_closed)+len(dates_opened))
dates[::2] = dates_opened
dates[1::2] = dates_closed
prices[::2] = opened
prices[1::2] = closed
ticks = [i for i in range(len(dates_opened)+len(dates_closed))]
plt.plot(prices)
plt.xticks(ticks, dates, rotation=90)
plt.tick_params(axis='x', which='major', labelsize=7)
for i in range(len(prices)):
    if i == 0:
        plt.plot(i, prices[i], 'bo', label='Opening')
    elif i % 2 == 0:
        plt.plot(i, prices[i], 'bo')
    elif i == 1:
        plt.plot(i, prices[i], 'ro', label='Closing')
    else:
        plt.plot(i, prices[i], 'ro')
last_price = prices[0]
x_pos = 0
for curr_price in prices:
    if curr_price > last_price:
        plt.plot(x_pos, curr_price+.5, marker='+')
    elif last_price > curr_price:
        plt.plot(x_pos, curr_price+.5, marker='_')
    x_pos += 1
    last_price = curr_price
plt.legend(loc=2)
news = newsapi.get_everything(q='tsla', from_param='2021-01-07', to='2021-02-01', language='en', sort_by='relevancy')
for i in news['articles']:
    title = i['title']
    print('{0} - {1}'.format(title, TextBlob('Battery-cell shortage hindered Tesla’s production of Semi truck').sentiment))
plt.show()
