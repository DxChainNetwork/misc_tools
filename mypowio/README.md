# mypow.io 批量查询工具

mypow.io是一个ETHW上的域名服务系统，域名注册是一次费用,终生使用。实在是web3撸毛交互，转账收钱的必备工具。

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

