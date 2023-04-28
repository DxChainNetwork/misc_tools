#!/usr/bin/env python

"""
# File: fair_lottery.py
# Last modified: 2023-04-28
# Version: 0.8.0
# Description: A fair lottery Python script
"""
import sys
import re
import hashlib
import random
import click


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

    participants= range(start,end + 1)
    winners = draw_lottery(participants, count, btc_hash)
    if sort:
        winners.sort()

    print(f'Total winners:{count}')
    if out:
        with open(out, 'w') as file:
            for item in winners:
                file.write(f'#{item}\n')
        print(f"Result file: {out}")
    else:
        print()
        for i in winners:
            print(f'#{i}')


def draw_lottery(participants, amount, btc_hash):
    """draw lottery winners based on btc block hash"""

    # set seed
    btc_hash_seed = hashlib.sha256(btc_hash.encode("utf-8")).hexdigest()
    random.seed(btc_hash_seed)

    # get winners
    winners = random.sample(participants, amount)

    return winners


if __name__ == '__main__':
    main()
