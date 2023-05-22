#!/usr/bin/env python

"""
# File: meshmatch.py
# Last modified: 2023-05-19
# Version: 0.1.0
"""

import hashlib
import json
from functools import partial
from pathlib import Path
import random
import re

import typer
from loguru import logger
from tqdm import tqdm

app = typer.Typer()

@app.command()
def match(
        start: int = typer.Option(default=1, help="Start token id(included)"),
        end: int = typer.Option(default=3300, help="End token id(included)"),
        btc_hash: str = typer.Option(default="", help="BTC block hash"),
        inscriptions_file: str = typer.Option(..., help="inscriptions file"),
        out: str = typer.Option(default=..., help="Output json file")
):
    """Image matching token_id"""

    # validate btc block hash
    btc_hash_re = re.compile(r'^[0-9a-fA-F]{64}$')
    if not btc_hash_re.match(btc_hash):
        logger.error("Invalid BTC transaction hash [{}].", btc_hash)
        raise typer.Exit(1)

    if not Path.exists(Path(inscriptions_file)):
        logger.error("not fund {}", inscriptions_file)
        raise typer.Exit(1)

    inscriptions_id = []
    with open(inscriptions_file, "r") as f:
        raw_data = json.loads(f.read())
    for item in raw_data:
        inscriptions_id.append(item["id"])

    # validate quantity
    token_ids = range(start, end + 1)
    inscriptions_count, token_ids_count = len(inscriptions_id), len(token_ids)
    if inscriptions_count != token_ids_count:
        logger.error(
            "number of token ids: {}, number of inscriptions: {}. Not equal in quantity.",
            token_ids_count, inscriptions_count,
        )
        raise typer.Exit(1)

    # Calculate the root hash
    sort_hashes = sorted(inscriptions_id)
    out_hash_name = f"root_hash.json"
    with open(out_hash_name, "w") as f:
        f.write(json.dumps(sort_hashes))
    with open(out_hash_name, "rb") as f:
        logger.info("root hash:{}", hashlib.sha256(f.read()).hexdigest())

    shuffle_hashes = shuffle(sort_hashes, btc_hash)
    result = []
    for token_id, inscription_id in zip(token_ids, shuffle_hashes):
        result.append({
            "token_id": token_id,
            "inscription_id": inscription_id,
        })
    
    if out:
        tmp = {}
        for i in result:
            tmp[i["token_id"]] = i["inscription_id"]

        with open(out, "w") as out_file:
            for key, value in tmp.items():
                out_file.write(f"{key},{value}\n")
        logger.info("Output file: {}", out)
    else:
        for item in result:
            logger.info(item)


def shuffle(items, btc_hash):
    """shuffle items with btc block hash"""

    # set seed
    btc_hash_seed = hashlib.sha256(btc_hash.encode("utf-8")).hexdigest()
    random.seed(btc_hash_seed)
    sort_items = sorted(list(items))
    random.shuffle(sort_items)
    return sort_items


if __name__ == '__main__':
    app()
