import pandas as pd
from web3 import Web3
import yaml
import time
from datetime import datetime, timedelta
import json
import requests




# Variables
ADDRESS_KARMA = "0xdfe691F37b6264a90Ff507EB359C45d55037951C"
recipients = ["0x2fd20232d72607ac54b756cf8d88f5c0792d9c6c","0xde71d7d06855b29eec3513393ddefd5f503ecbd0"]
transaction = {
    'to': '',
}


def build_tx(_from, to, gasPrice, nonce, value=0, data=None, **kwargs):

    # Handle Hexadecimal entries
    if type(_from) == "int":
        _from = hex(_from)

    if type(to) == "int":
        to = hex(int)

    # Make sure gasPrice is converted to Ether

    tx = {
        **kwargs,
        'to': to,
        'gasPrice': gasPrice
    }


    tx = {}

# Load config file
with open("config/config.yaml", "r") as stream:
    config = yaml.safe_load(stream)



def main(mainnet=False):

    # Connect to HTTPProvider
    if mainnet:
        web = Web3(Web3.HTTPProvider(config['INFURA']['RINKEBY']))
    else:  # We're on Rinkeby
        web = Web3(Web3.HTTPProvider(config['INFURA']['MAINNET']))


    for recipient in recipients:
        pass





if __name__ == "__main__":
    main()
