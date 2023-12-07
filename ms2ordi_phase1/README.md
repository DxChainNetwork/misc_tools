README.md

## Summary


## 2. commands


### 2.1 dump burned information from contract

```
python ms2ordi.py export-burned-info

2023-12-06 20:42:13.393 | INFO     | __main__:export_burned_info:48 - burned count: 1000
2023-12-06 20:42:14.347 | INFO     | __main__:export_burned_info:55 - tokenId[4], btc[bc1p2uzavpgvq0x5jw3dt3uzdcwstytl5j6ms40s57lzxk6z5am5399qrncmym]
2023-12-06 20:42:14.988 | INFO     | __main__:export_burned_info:55 - tokenId[5], btc[bc1p2uzavpgvq0x5jw3dt3uzdcwstytl5j6ms40s57lzxk6z5am5399qrncmym]
2023-12-06 20:42:15.431 | INFO     | __main__:export_burned_info:55 - tokenId[2], btc[bc1pd682nrdr2nm749kvs33fvqfdt8rxq726zac005l7259vtxa7ru7qfjyncs]
...
```


### 2.2 get BTC block hash as random seed 

You can get the most recent block from from https://blockstream.info/blocks/recent

We take block 820116 as seed, https://blockstream.info/block/0000000000000000000156cef1ab4242db65d926e77adabefc71fd8b419289bd

### 2.3 get the fair match for ETHW token ID and Ordi inscription

```
python ms2ordi.py pair --btc-hash="0000000000000000000156cef1ab4242db65d926e77adabefc71fd8b419289bd" --inscriptions-file="ordi_inscription_1000.csv" --out-file="ms_ordi_phase1.csv"
2023-12-06 23:20:50.295 | INFO     | __main__:pair:88 - inscription count: 1000
2023-12-06 23:20:50.297 | INFO     | __main__:pair:96 - token count: 1000
2023-12-06 23:20:50.298 | INFO     | __main__:pair:107 - inscription ids root hash: 2ce78fb8c8c474ad55d1687765bfbf01f86561d0de007a7cfb9c60bea1d13a14
2023-12-06 23:20:50.299 | INFO     | __main__:pair:114 - token ids root hash: dfb3946a4e5ae108baed33f04074e02b6ac4f67df4269670f07de7118e00118a
```


### 3. Final result


ms_ordi_phase1.csv





