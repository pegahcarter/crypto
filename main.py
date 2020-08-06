from web3 import Web3
import yaml
import time


with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)

web = Web3(Web3.HTTPProvider(config['INFURA']['MAINNET']))



def main():

    block_interval = 13
    remainder = (web.eth.blockNumber - 420) % 1000

    if remainder == 0:
        for account in config['wallet']:
            send_tx(web, account['PUBLIC_KEY'], account['PRIVATE_KEY'])
            print(f"Tx sent for: {account['PUBLIC_KEY']}")

        # Wait until ~25 blocks before start time
        wait = (975) * block_interval
        print(f"Sleeping for {wait} seconds")
        time.sleep(wait)

    elif remainder < 975:
        wait = (1000 - remainder - 25) * block_interval
        print(f"Sleeping for {wait} seconds")
        time.sleep(wait)

    else:  # Check every second for the last 25 blocks up to 420
        time.sleep(1)

    return True


def send_tx(web, public_key, private_key):
    tx = {'to': public_key,
          'value': 0,
          'gas': 21032,
          'gasPrice': 120 * 10**9 ,
          'data': 420,
          'nonce': web.eth.getTransactionCount(public_key)}

    signed = web.eth.account.signTransaction(tx, private_key=private_key)
    web.eth.sendRawTransaction(signed.rawTransaction)

    return True


if __name__ == "__main__":
    while True:
        main()
