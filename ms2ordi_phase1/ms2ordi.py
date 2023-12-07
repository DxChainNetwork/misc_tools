# -*- coding: UTF-8 -*-
"""
A fair MeshSpirits and Ordi pair script

https://www.yayasea.com/collection/MeshSpirits/items 
"""

import csv
import hashlib
import json
from pathlib import Path
import random
import re

from loguru import logger
import typer
from web3 import Web3


app = typer.Typer()


BURNED_INFO_FIELDNAMES = ("token_id", "btc", "owner",)
BURNED_INFO_FILE = "ms_burned_phase1.csv"


logger.add("logs/ms2btc_{time}.log", retention="7 days")


def shuffle(items, btc_hash):
    """shuffle the data by btc hash seed"""
    sort_items = sorted(list(items))
    btc_hash_seed = hashlib.sha256(btc_hash.encode("utf-8")).hexdigest()
    random.seed(btc_hash_seed)
    random.shuffle(sort_items)
    return sort_items


@app.command()
def export_burned_info():
    """export burned mesh spirits info on ETHW chain"""

    ms_ordi_deploy = json.load(Path("MeshSpiritOrdi.json").open())
    w3 = Web3(Web3.HTTPProvider("https://mainnet.ethereumpow.org"))
    contract = w3.eth.contract(address=ms_ordi_deploy["address"], abi=ms_ordi_deploy["abi"])

    ms_ids = contract.functions.meshSpiritIds().call()
    logger.info("burned count: {}", len(ms_ids))

    btcs = contract.functions.getBTCs(ms_ids).call()

    csv_writer = csv.DictWriter(Path(BURNED_INFO_FILE).open("w"), fieldnames=BURNED_INFO_FIELDNAMES)
    csv_writer.writeheader()
    for token_id, btc in zip(ms_ids, btcs):
        logger.info("tokenId[{}], btc[{}]", token_id, btc)
        burned_info = contract.functions.getBurnedInfo(token_id).call()
        assert btc == burned_info[1]
        owner = burned_info[2]
        csv_writer.writerow({
            "token_id": token_id,
            "btc": btc,
            "owner": owner,
        })


@app.command()
def pair(
    btc_hash: str = typer.Option(default="", help="BTC block hash"),
    inscriptions_file: str = typer.Option(..., help="inscription ids file"),
    out_file: str = typer.Option(..., help="out json file"),
):
    """pair inscription id with burned token id"""

    # validate btc block hash
    btc_hash_re = re.compile(r'^[0-9a-fA-F]{64}$')
    if not btc_hash_re.match(btc_hash):
        logger.error("Invalid BTC transaction hash [{}].", btc_hash)
        raise typer.Exit(1)

    if not Path(inscriptions_file).exists():
        logger.error("file not found: {}", inscriptions_file)
        raise typer.Exit(1)

    # inscription ids
    inscription_ids = []
    for item in csv.reader(Path(inscriptions_file).open()):
        inscription_ids.append(item[0])
    logger.info("inscription count: {}", len(inscription_ids))

    # burned token ids
    csv_reader = csv.DictReader(Path(BURNED_INFO_FILE).open("r"), fieldnames=BURNED_INFO_FIELDNAMES)
    next(csv_reader)
    tokens = dict()
    for row in csv_reader:
        tokens[int(row["token_id"])] = row["btc"]
    logger.info("token count: {}", len(tokens))

    if len(inscription_ids) != len(tokens):
        logger.error("inscription count[{}] is not equal to token count[{}]", len(inscription_ids), len(tokens))
        raise typer.Exit(1)

    sort_inscription_ids = sorted(inscription_ids)
    inscription_out_hash_name = "inscription_root_hash.json"
    with open(inscription_out_hash_name, "w") as f:
        json.dump(sort_inscription_ids, f)
    with open(inscription_out_hash_name, "rb") as f:
        logger.info("inscription ids root hash: {}", hashlib.sha256(f.read()).hexdigest())

    sort_token_ids = sorted(tokens.keys())
    token_out_hash_name = "token_root_hash.json"
    with open(token_out_hash_name, "w") as f:
        json.dump(sort_token_ids, f)
    with open(token_out_hash_name, "rb") as f:
        logger.info("token ids root hash: {}", hashlib.sha256(f.read()).hexdigest())

    # pair inscription with token
    shuffle_inscription_ids = shuffle(sort_inscription_ids, btc_hash)
    csv_writer = csv.writer(Path(out_file).open("w"))
    for token_id, inscription_id in zip(sort_token_ids, shuffle_inscription_ids):
        csv_writer.writerow([token_id, inscription_id, tokens[token_id]])


if __name__ == "__main__":
    app()
