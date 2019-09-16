from bot import Bot
import json
import time

def read_data():
    raw_data = []
    filename = 'historical_data.json'
    with open(filename) as f:
        data = json.load(f)
    for pair in data['price_usd']:
        raw_data.append(pair[1])
    print 'Read', len(raw_data), 'data points'
    return raw_data

# init bot with starting money
fiat_start = 100
fiat = fiat_start
crypto = 0
bot = Bot(fiat)
history = read_data()
count = 0
buys = 0
sells = 0

for current_value in history:
    count += 1
    decision = bot.tick(current_value)
    
    if decision == 'WAIT':
        pass
    elif decision == 'BUY':
        buys += 1
        crypto = fiat / current_value
        fiat = 0.0
    elif decision == 'SELL':
        sells += 1
        fiat = crypto * current_value
        crypto = 0.0

    bot.update_currency(crypto, fiat)
    
    print 'Tick', count, ':', current_value, ', crypto:', crypto, ' / fiat:', fiat, ', decision:', decision
    time.sleep(0.01)

# summary
if crypto > 0.1:
    fiat = crypto * current_value
    
profit = (fiat-fiat_start)/fiat_start * 100
    
print 'From', fiat_start, 'to', fiat, ', profit:', round(profit, 2), '%, buys:', buys, ', sells:', sells