# BOOT-B151 — Free carry-LUT elimination in B145

- Date: 2026-10-27 (Asia/Singapore)
- TRACK_ID: BOOT
- Parent: B145
- Status: PASS_EXACT / FREE_OUTPUT_REDUCTION
- CODEX_REQUIRED: NO

## Setting

Use B=64, E=16 and the corrected B=4E recurrence from B145.

Write

    F_k(b)=bit_k(b),  k=0,...,5,

and

    D_k(b,c)=L(c)(F_k(b-1)-F_k(b)),

where L(c)=1[c<32].

The corrected carry recurrence is

    sigma_j = G_j + S_j sigma_{j-1}

with

    G_j = H(b_j),
    S_j = L(c_j)(P(b_j)-T(b_j)),

where
- H(b)=1[32<=b<64],
- P(b)=1[b=0],
- T(b)=1[b=32].

## Exact identities

Because B=64, the most significant radix bit is exactly

    F_5(b)=1[32<=b<64]=H(b).

Thus

    G = F_5.

For the MSB transition,

    F_5(b-1)-F_5(b)
      = +1 if b=0,
        -1 if b=32,
         0 otherwise
      = P(b)-T(b).

Therefore

    D_5 = L(c)(P(b)-T(b)) = S.

Hence the generic carry-state LUT pair (G,S) is exactly the same pair already needed for the highest output bit (F_5,D_5).

## Consequences

A naive multi-bit adaptation of 2368 Algorithm 3 would request:
- 2 real LUTs for the complex carry symbol xi=(G,S);
- 6 real LUTs F_k;
- 6 real LUTs D_k;

for 14 real LUT outputs on the shared 4096 root.

B151 removes the two redundant carry LUTs:

    xi = chi(F_5,D_5).

Only the twelve real functions

    {F_k,D_k}_{k=0}^5

need to be evaluated.

No additional ciphertext multiplication, rotation, key switching, level, or approximation error is introduced.

There is a second free saving. For k=5,

    F_5(a_j)
      = F_5(b_j) + sigma_{j-1} D_5(b_j,c_j)
      = G_j + S_j sigma_{j-1}
      = sigma_j.

After PrefixScan, the carry-state intercept at position j is already the recovered MSB. Thus the final post-scan correction multiplication is needed only for k=0,...,4.

For n=256, u=43:
- prefix scan: 6 ciphertext multiplications;
- final corrections: 5, not 6;
- post-LUT CMult count: 11, not 12;
- post-LUT depth remains 7 in the cheap-output variant.

## Generalization

The identity is tied to choosing the carry high interval H as exactly the upper half of the radix. At B=64,E=16, B-2E=32, so this alignment is exact.

It should not be stated for arbitrary B,E.

## Decision

PASS_EXACT / KEEP.

B145 canonical direct backend should use:
- one Root_{4096};
- twelve real LUT outputs (six (F_k,D_k) pairs);
- one shared affine prefix scan using (F_5,D_5);
- five final correction multiplications.

This is a strict free improvement over the previously recorded 14-LUT/12-tail-CMult formulation.
