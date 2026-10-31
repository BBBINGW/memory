# Evidence — RM10 Physical-Key-Switch Strategy Matrix

Date: 2026-11-01
Session: 密码学 17.0
Logical Turn: 3/25

Pinned HElib: `acdb264e1a991eaee35fd8b3c31bebe9528c49a1`.

Parameters:
- m=32768
- p=5
- ord_m(5)=8192
- BSGS giant step g=91

## RM10 targets

| u | e: 5^e=u mod 32768 | q | r in e=91q+r | FULL hops | BSGS hops | MIN hops | MIN (a,b) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 16385 | 4096 | 45 | 1 | 1 | 2 | 46 | (1,45) |
| 8193 | 6144 | 67 | 47 | 1 | 2 | 114 | (47,67) |
| 4097 | 7168 | 78 | 70 | 1 | 2 | 148 | (70,78) |
| 2049 | 7680 | 84 | 36 | 1 | 2 | 120 | (36,84) |
| 1025 | 7936 | 87 | 19 | 1 | 2 | 106 | (19,87) |
| 513 | 3968 | 43 | 55 | 1 | 2 | 98 | (55,43) |
| 257 | 6080 | 66 | 74 | 1 | 2 | 140 | (74,66) |
| 129 | 5088 | 55 | 83 | 1 | 2 | 138 | (83,55) |
| 65 | 2032 | 22 | 30 | 1 | 2 | 52 | (30,22) |
| 33 | 888 | 9 | 69 | 1 | 2 | 78 | (69,9) |

Totals:
- FULL RM10: 10 physical KS
- BSGS RM10: 20 physical KS
- MIN RM10: 1040 physical KS

MIN values are exact exhaustive minima over b in 0..8191 of
`a+b` with `a=(e-91b) mod 8192`.

## Baseline five-branch C2S

Binary trace targets under FULL/BSGS:
`1,2,4,8,16,32,64,128,256,512,1024,2048,4096`.

- FULL trace: 13 hops; plus D=2 map 1 => 14/branch => 70 total.
- BSGS trace: first 7 direct + last 6 two-hop = 19; plus D=2 map 1 => 20/branch => 100 total.
- MIN trace source schedule: 90 direct j=1 baby steps + 90 direct j=91 giant steps = 180; plus D=2 map 1 => 181/branch => 905 total.

## Candidate recovery

Turn-1 chained joint recovery = 4 physical j=1 Frobenius KS under all standard strategies.

Thus:
- FULL: 70 -> 14
- BSGS: 100 -> 24
- MIN: 905 -> 1044

## Direct RM10 key augmentation

Adding the ten exact RM10 direct matrices makes RM10 10 hops under any starting strategy.

Matrix-count impact:
- FULL: no new matrices.
- BSGS Frobenius family: 180 -> 190 (+5.555...% matrix count).
- MIN Frobenius family: 2 -> 12 (+500% matrix count).

With the same BSGS+10 keyset, the direct e=4096 matrix also reduces each baseline trace by one hop, so baseline five-branch C2S becomes 100 -> 95; candidate recovery is 14.

No key-byte/RSS claim is made.
