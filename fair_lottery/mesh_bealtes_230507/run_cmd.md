### 1. Hash of result

```
shasum -a 256 lottery.py
40f343e833a238c18aa8dab21909c8e61f9af194e9aec4eb084ca85240136c21  lottery.py


shasum -a 256 mesh_0507.txt
6964ee192e5aa5e3d54b9014148ce4181df61417178bfb4fdf0d2c1eb9559698  mesh_0507.txt

python lottery.py --start 1 --end 10000 --count 2000 --btc_hash=000000000000000000039e4fed8191d873216a6a6dd088e355e330cb95f568a3 --out mesh_0507.txt
```


