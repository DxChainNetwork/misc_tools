# -*- coding: UTF-8 -*-

"""
@Summary : mypow.io域名是否注册查询工具
@Author  : 骆驼哥(https://twitter.com/jameslidx)
"""

import json
import requests
import sys


def query_domains(domains):
    """get available domains"""
    url = "https://graph.mypow.io/subgraphs/name/service/mypow"

    query = f"""
        {{
            domains(where: {{labelName_in: {json.dumps(domains)}}}) {{
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
    not_available = [i["labelName"] for i in resp_json["data"]["domains"]]

    return list(set(domains)-set(not_available)), list(set(not_available))


def read_domains(filename):
    """read domain names from txt file"""
    names = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                names.append(line)

    return names



def main():
    """main"""
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("Please give me a filename")
        sys.exit(1)

    domains = read_domains(filename)
    availables, not_availables = query_domains(domains)
    availables.sort()
    not_availables.sort()

    print(f"Not available:{len(not_availables)}")
    print("=" * 15)
    for domain in not_availables:
        print(domain)

    print("\n"*2)

    print(f"Available:{len(availables)}")
    print("=" * 15)
    for domain in availables:
        print(domain)

if __name__ == '__main__':
    main()

