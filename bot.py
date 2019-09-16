#!/usr/bin/python
from __future__ import division
import time

class Bot:
    """ Class for a Trading bot """
    crypto = 0
    fiat = 0
    buy_limit = 0.4     # buy at 40% of average
    sell_limit = 0.6    # sell at 60% of average
    buy_price = 0.0
    memory_limit = 180  # maximum memory
    memory_lower = 60   # minimum amount of data to make first BUY / SELL decision
    memory = []
    BUY = 'BUY'
    SELL = 'SELL'
    WAIT = 'WAIT'

    def __init__(self, fiat):
        self.memory = []
        self.fiat = fiat
        self.buy_price = 0.0

    def tick(self, current_value):
        ''' decision algorithm what to do on update '''
        # save to memory
        if len(self.memory) >= self.memory_limit:
            self.memory.pop(0)
        self.memory.append(current_value)
        
        if len(self.memory) < self.memory_lower:
            # if not enough data, do nothing
            return self.WAIT
        
        lower = self.get_percentile(self.buy_limit)
        upper = self.get_percentile(self.sell_limit)
        
        print ' > lower:', lower, ', upper:', upper
        
        if self.crypto <= 0.1:
            # no crypto: could BUY or WAIT
            if current_value < lower:
                self.buy_price = current_value
                return self.BUY
        elif self.fiat <= 0.1:
            # no fiat: could SELL or WAIT
            if current_value > upper and current_value > self.buy_price:
                return self.SELL
                
        # no decision made, wait and drink tea
        return self.WAIT
        
    def update_currency(self, crypto, fiat):
        self.crypto = crypto
        self.fiat = fiat
    
    def get_percentile(self, perc):
        sorted_memory = sorted(self.memory)
        item = int(perc * len(sorted_memory))
        return sorted_memory[item]
