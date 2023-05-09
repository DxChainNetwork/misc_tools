#!/usr/bin/env python

"""
# File: fair_lottery.py
# Last modified: 2023-05-09
# Version: 0.2.0
# Description: A fair lottery Python script for beatles
"""
import sys
import re
import hashlib
import random

import click
from tqdm import tqdm
from web3 import Web3

beatles_contract_address = '0x650c3Cf4fAe84C3a23a1d6f11712734efAdBef5d'

abi = [
    {
        "constant": False,
        "inputs": [{"indexed": False, "internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]


@click.command()
@click.option('--start', default=1, help='Start num(included)')
@click.option('--end', default=10_000, help='End num(included)')
@click.option('--count', default=1, help='Number of winners.')
@click.option('--btc_hash', default='', help='BTC Hash')
@click.option('--sort', default=True, help='sort result')
@click.option('--out', default='', help='output txt file')
def main(start, end, count, btc_hash, sort, out):
    """"fair lottery main fun"""
    btc_hash_re = re.compile(r'^[0-9a-fA-F]{64}$')
    if not btc_hash_re.match(btc_hash):
        print(f'Invalid BTC transaction hash [{btc_hash}].')
        sys.exit(1)

    participants = range(start, end + 1)
    winners = draw_lottery(participants, count, btc_hash)
    if sort:
        winners.sort()

    print(f'Total winners:{count}')

    w3 = Web3(Web3.HTTPProvider('https://mainnet.ethereumpow.org'))
    contract = w3.eth.contract(address=Web3.to_checksum_address(beatles_contract_address), abi=abi)
    winners = get_holder(winners, contract)

    if out:
        with open(out, 'w') as file:
            for item in winners:
                file.write(f'#{item[0]} {item[1]}\n')
        print(f"Result file: {out}")
    else:
        print()
        for i in winners:
            print(f'#{i[0]} {i[1]}')


def draw_lottery(participants, amount, btc_hash):
    """draw lottery winners based on btc block hash"""

    # set seed
    btc_hash_seed = hashlib.sha256(btc_hash.encode("utf-8")).hexdigest()
    random.seed(btc_hash_seed)

    # get winners
    winners = random.sample(participants, amount)

    return winners


def get_holder(winners, contract):
    """get token_id holder"""
    data = []
    for winner in tqdm(winners):
        address = contract.functions.ownerOf(winner).call()
        data.append((winner, address))
    return data


if __name__ == '__main__':
    main()
