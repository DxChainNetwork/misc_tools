# mypow.io 批量注册工具

mypow.io是一个ETHW上的域名服务系统，域名注册是一次费用,终生使用。实在是web3撸毛交互，转账收钱的必备工具。
本工具提供了一个批量注册的工具

## 安全警示
本工具需要你设置自己的私钥，有可能会有人拷贝和修改这个工具，盗用你的财产。 为保护好个人财产，一定要注意一下几点:

1. 生成一个新的账号，确保里面没有资产，导入ETHW，用这个账号运行
2. 运行完毕之后，把你的私钥从程序中删除，不要长期保留在文件中，含有私钥的程序不用与他人分享
3. 运行之前，确保文件没有被篡改。在没有输入地址和私钥之前，文件checksum如下:

```
% shasum -a 256 batch_reg_mypow.py
4e42693af79b7e5484f050fb44f76ba00b4f0e328293dcbd81e39619d9bdbca6  batch_reg_mypow.py
```

### 运行举例

把程序21，22行，"TODO_REPLACE_ME"的地方，换成你的地址和私钥。

```
sender_address = Web3.to_checksum_address("TODO_REPLACE_ME") # 账户地址
private_key = "TODO_REPLACE_ME" # 私钥
```

```
python batch_reg_mypow.py mylist.txt
```

其中 mylist.txt是你的词典，一行一个单词。



# mypow.io 批量查询工具


本工具提供了一个批量查询的工具，可以查询自己喜欢的域名是不是已经被注册。

## 使用方式

### 1. 安装和配置好Python
就这样吧，google或者chatgpt一下


### 2. 准备好要查询的文件，一行一个域名

例如: mynames.txt

```
0000000
1111111
2222222
3333333
4444444
5555555
6666666
7777777
8888888
9999999
aaaaaaaaaaaaaaaaaaaa
```

### 3. 运行

```
python mypowq.py mynames.txt
```

### 4. 执行结果

```
Not available:10
===============
0000000
1111111
2222222
3333333
4444444
5555555
6666666
7777777
8888888
9999999



Available:1
===============
aaaaaaaaaaaaaaaaaaaa
```

## 工具说明

本工具只为简化mypow.io批量查询，是否应该注册请自行决策，DYOR.
如有bug或其他反馈，欢迎到本人twitter(https://twitter.com/jameslidx) 下留言交流讨论，谢谢大家。

