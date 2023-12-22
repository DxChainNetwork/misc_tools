README.md

## Summary


## 2. commands


### 2.1 dump burned information from contract

```
python ms2ordi.py export-burned-info

```


### 2.2 get BTC block hash as random seed 

You can get the most recent block from from https://blockstream.info/blocks/recent

We take block 822348 hash 00000000000000000003ec82000a99258c31b1bf23e60930de897ae5e8e49bd1 as random seed

### 2.3 get the fair match for ETHW token ID and Ordi inscription

```
python ms2btc.py pair-phase2 --btc-hash=00000000000000000003ec82000a99258c31b1bf23e60930de897ae5e8e49bd1 --inscriptions-file=inscri_1000_phase2.csv --out-file=ms_phase2_1000.csv

```


### 3. Final result

The final result file is "ms_phase2_1000.csv"

