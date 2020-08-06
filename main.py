from web3 import Web3
import yaml
import time



with open("config.yaml", "r") as stream:
    config = yaml.safe_load(stream)


def main():

    web = Web3(Web3.HTTPProvider(config['INFURA']['RINKEBY']))
    block_interval = 13

    remainder = (web.eth.blockNumber - 420) % 1000

    if remainder < 100:
        wait = (1000 - remainder - 20) * 13
        time.sleep(wait)


    if remainder != 0:
        print('It does not equal 0')



def send_tx(web, public_key, private_key):
    tx = {'to': public_key,
          'value': 0,
          'gas': 21032,
          'gasPrice': 150 *10**9 ,
          'data': 420,
          'nonce': web.eth.getTransactionCount(public_key)}

    signed = web.eth.account.signTransaction(tx, private_key=private_key)
    web.eth.sendRawTransaction(signed.rawTransaction)

    return


if __name__ == "__main__":
    main()
