import json
from datetime import datetime
from pathlib import Path
import os


class CDP:

    MIN_RATIO = 3.0/2.0

    def __init__(self, price, preload=False, eth_deposited=0.01, dai_generated=1, start_eth_on_hand=0):

        # Load a CDP that was previously created
        if preload and Path('cdp.json').exists():
            with open(self.filename, 'r') as f:
                cdp = json.load(f)
            for key, val in cdp.items():
                setattr(self, key, val)
        # Create a new CDP
        else:
            self.actions = []
            self.trades = []
            self.summary = {}
            self.summary['Initial ETH quantity'] = start_eth_on_hand
            self.summary['ETH on hand'] = start_eth_on_hand
            self.summary['DAI on hand'] = 0
            self.summary['ETH deposited'] = eth_deposited
            self.summary['DAI generated'] = dai_generated
            self.price = price
            self.start_price = price
            self.start_eth_on_hand = start_eth_on_hand

        self._update_calculations()


    def _add_action(self, action, eth_dai, quantity, date=None):

        if date is None:
            date = datetime.now()

        self.actions.append({
            'id': len(self.actions) + 1,
            'date': int(datetime.timestamp(date)),
            'action': action,
            'eth-dai': eth_dai,
            'quantity': round(quantity, 2)
        })

        self._update_calculations()


    def _update_calculations(self, eth=None):

        self.summary['Liquidation price'] = round(self.summary['DAI generated'] * self.MIN_RATIO / self.summary['ETH deposited'], 2)
        self.summary['DAI value'] = round(self.price * self.summary['ETH deposited'], 2)
        self.summary['DAI available to generate'] = self.summary['DAI value'] / self.MIN_RATIO - self.summary['DAI generated']
        self.summary['ETH available to withdraw'] = self.summary['DAI available to generate'] / self.price

        return eth


    def update_price(self, price):

        self.price = price
        self._update_calculations()


    def deposit(self, eth, ignore=False, date=None):

        if ignore is False:
            self.summary['ETH on hand'] -= eth

        self.summary['ETH deposited'] += eth
        self._add_action(action='deposit', eth_dai='ETH', quantity=eth, date=date)


    def withdraw(self, eth, date=None):

        self.summary['ETH deposited'] -= eth
        self.summary['ETH on hand'] += eth
        self._add_action(action='withdraw', eth_dai='ETH', quantity=eth, date=date)


    # TODO: add fee calculation
    def payback(self, dai, date=None):

        self.summary['DAI generated'] -= dai
        self.summary['DAI on hand'] -= dai
        self._add_action(action='payback', eth_dai='DAI', quantity=dai, date=date)


    def generate(self, dai, date=None):

        if dai > (max_dai:= self.summary['DAI available to generate']):
            return f'{dai} DAI generated exceeds limit of {round(max_dai, 2)} DAI'

        self.summary['DAI generated'] += dai
        self.summary['DAI on hand'] += dai
        self._add_action(action='generate', eth_dai='DAI', quantity=dai, date=date)


    def trade(self, side, dai=None, eth=None, price=None, date=None):

        if price is None:
            price = self.price

        if date is None:
            date = datetime.now()

        if dai is None:
            dai = price * eth
        elif eth is None:
            eth = dai / price

        if side == 'BUY':
            self.summary['ETH on hand'] += eth
            self.summary['DAI on hand'] -= dai
        else: # side == 'SELL'
            self.summary['ETH on hand'] -= eth
            self.summary['DAI on hand'] += dai

        self.trades.append({
            'id': len(self.trades) + 1,
            'date': int(datetime.timestamp(date)),
            'side': side,
            'dai': dai,
            'price': price,
            'eth': round(eth, 2)
        })

        return self._update_calculations(eth)


    def describe(self):
        return self.__dict__['summary']


    def summarize(self, price=None, save=False):

        if price:
            self.update_price(price)

        self.summary.pop('DAI available to generate')
        self.summary.pop('ETH available to withdraw')
        self.summary['ETH on hand'] = self.summary['ETH on hand']
        self.summary['ETH price'] = self.price
        self.summary['End ETH'] = ((self.summary['ETH deposited'] + self.summary['ETH on hand']) * self.price - self.summary['DAI generated']) / self.price

        self.summary['% change in ETH price'] = (self.price - self.start_price) / self.start_price * 100
        self.summary['% profit in ETH'] = (self.summary['End ETH'] - self.start_eth_on_hand) / self.start_eth_on_hand * 100
        self.summary['ETH gained / lost'] = self.summary['End ETH'] - self.summary['Initial ETH quantity']

        # Round values to two decimals and add percentages if needed
        for key, val in self.summary.items():
            val = round(val, 2)
            if '%' in key:
                val = f'{val}%'
            self.summary[key] = val

        # Save CDP to file
        if save is True:
            with open(os.getcwd() + '/../src/assets/cdp.json', 'w') as outfile:
                json.dump(self.__dict__, outfile)

        return self.summary['End ETH']
