import ccxt

bitfinex = ccxt.bitfinex()
bitfinex.apiKey = 'my-api-key'
bitfinex.secret = 'my-secret'

for c in bitfinex.fetch_balance()['info']:
    print c['currency'], ':', c['available']