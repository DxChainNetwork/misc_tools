## 一个用BTC block Hash作为种子的公平抽奖程序

### 1. 安装
本程序需要Python3环境运行

安装依赖环境

```
pip install -r requirements.txt
```


### 2. 参数说明和使用举例

```
Options:
  --start INTEGER  Start num(included) # 参与者开始数目 包含本数目
  --end INTEGER    End num(included)   # 参与者开始数目，包含本数目
  --count INTEGER  Number of winners.  # 获奖者数目
  --btc_hash TEXT  BTC Hash            # 比特币出块Hash
  --sort BOOLEAN   sort result         # 输出是否排序
  --out TEXT       output txt file     # 输出文件 
  --help           Show this message and exit.
```

BTC出块Hash可以从 https://blockstream.info/ 获取

从编号开始编号为1，结束编号为10000，以BTC block hash为种子，抽签2100名幸运者，结果进行排序，输出到文件2100_winners.txt中，命令如下:

```
python lottery.py --start 1 --end 10000 --count 2100 --btc_hash=00000000000000000000ec54266daba90891363b64536ff53ed402fe814fa0e8 --out=2100_winners.txt
```