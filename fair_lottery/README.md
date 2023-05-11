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

## 一个用BTC block Hash作为种子的甲虫公平抽奖程序

描述：在使用公平抽奖程序的基础上新增持有者

### 1. 安装
本程序需要Python3环境运行

安装依赖环境

```
pip install -r requirements.txt
```


### 2. 参数说明和使用举例

```
Options:
  --start INTEGER  Start num(included) # 参与者开始数目 包含本数目 默认1
  --end INTEGER    End num(included)   # 参与者开始数目，包含本数目 默认10000
  --count INTEGER  Number of winners.  # 获奖者数目，数量必须小于等于start-end之间的总数
  --btc_hash TEXT  BTC Hash            # 比特币出块Hash，默认获取最新的出块Hash
  --sort BOOLEAN   sort result         # 输出是否排序
  --out TEXT       output txt file     # 输出文件 
  --exclude TEXT   exclude file, same format as output file # 排除在本次抽奖之外的白名单文件，文件必须在当前目录下，格式和输出文件保持一致
  --help           Show this message and exit.
```

BTC出块Hash可以从 https://blockstream.info/ 获取

从编号开始编号为1，结束编号为10000，以BTC block hash为种子，抽签100名幸运者，结果进行排序，输出到文件100_winners.txt中，命令如下:

```
python lottery_beatles.py --start 1 --end 10000 --count 100 --btc_hash=00000000000000000000ec54266daba90891363b64536ff53ed402fe814fa0e8 --out=100_winners.txt
```

从编号开始编号为1，结束编号为10000，使用最新的BTC block hash为种子，排除file1.txt和file2.txt内的白名单，抽签100名幸运者，结果进行排序，输出到控制台中，命令如下:

```
python lottery_beatles.py --count 100 --exclude file1.txt,file2.txt
```

控制台输出：
```
latest BTC block:[789030]
BTC block hash:[00000000000000000005b6235aa7403351750e0a08609084b9b91a4b5ef55b65]
#188 0xEF32xxxxxxxxxxxxxxxxxxxxxx546a9
#2138 0xad57xxxxxxxxxxxxxxxxxxxxxaef92
#2310 0xff7dxxxxxxxxxxxxxxxxxxxxxx1A1E5
。。。
```