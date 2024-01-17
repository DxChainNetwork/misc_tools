README.md

## Summary


## 2. commands


### 2.1 dump burned information from contract

```
python ms2ordi.py export-burned-info

```


### 2.2 get BTC block hash as random seed 

You can get the most recent block from from https://blockstream.info/blocks/recent

We take block 826096 hash 000000000000000000001e7e3a0b5b667e49bdd49b81de58e035367d890e2d5f as random seed

### 2.3 get the fair match for ETHW token ID and Ordi inscription

```
python ms2btc.py pair-phase3 --btc-hash=000000000000000000001e7e3a0b5b667e49bdd49b81de58e035367d890e2d5f --inscriptions-file=inscri_1893_phase3.csv --out-file=ms_phase3_1893.csv

```


### 3. Final result

The final result file is "ms_phase3_1893.csv"

