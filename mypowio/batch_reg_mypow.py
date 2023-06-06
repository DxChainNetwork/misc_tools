# -*- coding: UTF-8 -*-
"""
@Summary : mypow.io域名是否注册查询工具
@Author  : 骆驼哥(https://twitter.com/jameslidx)
"""

import json
from pathlib import Path
import time
import csv
import sys

from loguru import logger
import secrets
from web3 import Web3
from web3.constants import ADDRESS_ZERO
import requests
from web3.exceptions import ContractLogicError


sender_address = Web3.to_checksum_address("TODO_REPLACE_ME") # 账户地址
private_key = "TODO_REPLACE_ME" # 私钥
price = Web3.to_wei(0.01, "ether") # 域名单价
gas_price = Web3.to_wei(10, "gwei") # gas price: gwei

contract_address = "0x5590BFdd8c14390F71422A4429d40274582d3bE0"
rpc = "https://mainnet.ethereumpow.org"


def create_contract(w3: Web3, contract_address: str, abi: str):
    """
    创建合约对象
    :param w3:
    :param contract_address:
    :param abi:
    :return:
    """
    file_path = Path(__file__).parent / abi
    with open(file_path, 'r') as f:
        abi = f.read()
    contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=abi)
    return contract


def check_names(names):
    logger.info("check: {}", names)
    url = "https://graph.mypow.io/subgraphs/name/service/mypow"

    query = f"""
        {{
            domains(where: {{labelName_in: {json.dumps(names)}}}) {{
                id
                labelName
                labelhash
                name
            }}
        }}
    """
    headers = {
        'Content-Type': 'application/json'
    }

    resp = requests.post(url, headers=headers, json={"query": query})
    resp_json = resp.json()
    done = [i["labelName"] for i in resp_json["data"]["domains"]]
    undo = list(set(names) - set(done))
    logger.info("尚未注册: {}", undo)
    return undo


def register_batch(w3: Web3, domains):
    abi = "ETHRegistrarController.json"
    contract = create_contract(w3, contract_address, abi)
    # 删除长度不足5的域名
    logger.info('正在删除域名长度小于5的域名...')
    data = [i.strip() for i in domains if len(i.strip()) > 4]
    if len(data) > 10:
        logger.warning("批量注册不能大于10个, 当前{}", len(data))
        return
    
    logger.info("正在注册: {}", data)
    # 4 判断钱包地址是否足够
    from_balance_wei = w3.eth.get_balance(sender_address)
    # from_balance = Web3.from_wei(from_balance_wei, 'ether')
    amount = price * len(data)
    if from_balance_wei < amount:
        logger.warning('转账地址金额不足，当前账户金额:[{}], 所需金额:[{}]', from_balance_wei, amount)
        return

    secrets_bytes = secrets.token_bytes(32)
    # 1 第一步
    bytes_list = contract.functions.makeCommitmentBatch(domains, sender_address, secrets_bytes).call()
    # 2 第二步
    tx = contract.functions.commitBatch(bytes_list).build_transaction(
        {
            'nonce': w3.eth.get_transaction_count(sender_address),
            'type': 1,
            'gasPrice': gas_price,
        }
    )
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)

    txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    logger.info("commitBatch: {} wait for...", txn_hash.hex())
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    logger.info("等待commitBatch上链后再执行registerBatch, sleep 90s...")
    time.sleep(90)
    # 打印交易结果信息
    logger.info("commitBatch: Transaction with hash {} was successful!", txn_receipt['transactionHash'].hex())

    tx = {
        'nonce': w3.eth.get_transaction_count(sender_address),
        'value': price * len(domains),
        'type': 1,
        'gasPrice': gas_price,
    }
    try:
        tx = contract.functions.registerBatch(domains, sender_address, 3124138248, secrets_bytes, [0], ADDRESS_ZERO).build_transaction(tx)
    except ContractLogicError as err:
        logger.warning(err)
        logger.warning("fail register batch: []", domains)
        return
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    logger.info("registerBatch: {} wait for...", txn_hash.hex())
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    # 打印交易结果信息
    logger.info("registerBatch: Transaction with hash {} was successful!", txn_receipt['transactionHash'].hex())
    return True


def regdomain(domains):
    available_domains = []
    page_domains = [domains[i: i+100] for i in range(0, len(domains), 100)]
    for page_domain in page_domains:
        checked = check_names(page_domain)
        available_domains.extend(checked)

    w3 = Web3(Web3.HTTPProvider(rpc))
    page_available_domains = [available_domains[i: i+10] for i in range(0, len(available_domains), 10)]

    result = open(f"{sender_address}.csv", "a")
    for page_available_domain in page_available_domains:
        try:
            if register_batch(w3, page_available_domain):
                for i in page_available_domain:
                    result.write(f"{i}\n")
        except:
            time.sleep(90)

    result.close()


def main():
    """main"""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("No arguments provided.")
        sys.exit(1)
    
    f = open(filename)
    reader = csv.reader(f)
    next(reader)
    domains = [i[0] for i in reader]

    regdomain(domains)


if __name__ == '__main__':
    main()
