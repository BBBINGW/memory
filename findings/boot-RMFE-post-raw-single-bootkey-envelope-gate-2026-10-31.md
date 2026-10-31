# BOOT RMFE Post-Raw Single-Bootkey Envelope Gate

Date: 2026-10-31
Session: 密码学 16.0
Logical Research Turn: 2/25 (same-turn infrastructure retry; not incremented)
TRACK_ID: BOOT
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS

## Scope

This turn does **not** retry the already-killed exact full-path commutation route.

Durable prior result `boot-RMFE-p5w512-commutation-boundary-2026-10-29.md` already established:

- the real HElib order is
  `S2C -> relinearize -> rawModSwitch -> newMakeDivisible -> boot-key multiply/add -> C2S`;
- `rawModSwitch` / `newMakeDivisible` are nonlinear in their representative/rounding semantics;
- exact five-way fusion **before** that nonlinear boundary is therefore killed;
- the post-raw boot-key multiply/add itself remains outer-ring linear.

This gate tests only the strongest surviving alternative:

> Keep five branches separate through `rawModSwitch + newMakeDivisible + divide`, then merge the resulting public integer-polynomial pairs and execute the `recryptEkey` multiply/add only once.

No Codex, native execution, key generation, DFR run, benchmark, or parameter sweep occurred.

## Primary hypothesis

For p=5, w=512, k=5 and the established R8 envelope with

[
Y=X^{1024},
]

suppose branch i has already completed thin S2C, key switching to the recryption-key secret, raw modulus switching, balanced `newMakeDivisible`, and division by (P=p^{e'}), producing public integer polynomials

[
(a_i,b_i).
]

HElib then reconstructs a ciphertext from the common encrypted recryption key (K=	exttt{recryptEkey}) as

[
B_i=a_i+b_iK.
]

The hypothesis is that the five branch-local carries can be preserved while collapsing only this post-raw reconstruction:

[
A=sum_{i=0}^{4}Y^i a_i,qquad
B=sum_{i=0}^{4}Y^i b_i,
]

[
C=A+BK,
]

followed by the already-established RM10/R8 recovery machinery.

Falsifier: any source-level dependence on branch identity after the ((a_i,b_i)) pairs are formed, any distinct `recryptEkey` per branch, failure of multiplication by (Y^i) to commute with the common boot-key multiplication, or failure of RM10 to be (R_8)-linear.

## Source provenance

HElib public source inspected:

`homenc/HElib@3e337a66a91a92d49de6a9505340826b0eb71081`

File: `src/recryption.cpp`.

The thin-recryption source order around the relevant boundary is:

1. `trcData.slotToCoeff->apply(ctxt)`;
2. `ctxt.reLinearize(recryptKeyID)`;
3. `ctxt.rawModSwitch(zzParts,q)`;
4. `newMakeDivisible(zzParts[i],p2ePrime,q,...)`;
5. divide both `zzParts` by `p2ePrime`;
6. `ctxt = recryptEkey`;
7. `ctxt.multByConstant(zzParts[1])`;
8. `ctxt.addConstant(zzParts[0])`;
9. `trcData.coeffToSlot->apply(ctxt)`.

Thus the nonlinear representative choice is complete **before** the common `recryptEkey` multiply/add.

Aung et al. ePrint 2025/350 / PKC 2025 Algorithm 2 still performs MultKey separately on k split ciphertexts and explicitly leaves direct RMFE-packed MultKey as future work. This gate is a new BOOT redesign, not a claim about their implementation.

## Exact post-raw fusion identity

For each branch let

[
B_i=a_i+b_iK.
]

Because the ciphertext ring is commutative and (Y^i) is a public plaintext-ring monomial,

[
egin{aligned}
C
&=left(sum_i Y^i a_iight)
 +left(sum_iY^i b_iight)K \
&=sum_i Y^i(a_i+b_iK) \
&=sum_iY^iB_i.
end{aligned}
]

This is an **exact ciphertext-level identity** relative to the five separate post-raw reconstructions. It does not assume that `rawModSwitch` or `newMakeDivisible` are linear.

Therefore all branch-specific balanced carries and rounding choices have already been committed into (a_i,b_i) before fusion. The previous full-path commutation counterexample does not apply.

The construction also does not add a new boot-key encryption-noise term relative to "five separate reconstructions then shift-and-add": all five baseline branches copy the same `recryptEkey`, so linearity gives the same combined term.

## RM10 compatibility

The established R8 subring is

[
R_8=(mathbb Z/625mathbb Z)[Y]/(Y^{16}+1),
qquad Y=X^{1024}.
]

The ten RM automorphism exponents are

[
16385,8193,4097,2049,1025,513,257,129,65,33.
]

Every one is congruent to (1mod 32). Hence each automorphism fixes (Y):

[
sigma_u(Y)=Y^u=Y
]

inside the embedded (m_r=32) subring. Therefore RM10 is (R_8)-linear:

[
operatorname{RM10}(Y^i z)=Y^ioperatorname{RM10}(z).
]

Thus

[
operatorname{RM10}(C)
 =sum_iY^ioperatorname{RM10}(B_i).
]

The standard RM10 scale is (1024equiv399pmod{625}); its inverse is (224), matching the previously established fixed-Q ledger.

After RM10 the state lies in the R8 coefficient subspace already covered by the exact 16-by-16 R8 map gate. The previously verified R8 C2S map therefore remains the correct static recovery map for the first five retained power-basis coordinates.

## Verdict

```text
RESULT: PASS_STATIC_POST_RAW_SINGLE_BOOTKEY_FUSION

PRE_RAW_FULL_PATH_FUSION:
  KILLED / unchanged

POST_RAW_BRANCH_CARRY_PRESERVATION:
  PASS_EXACT

POST_RAW_RECRYPTEKEY_MULTIPLY_ADD:
  5 -> 1 exact fusion

RM10_R8_LINEARITY:
  PASS_EXACT

R8_RECOVERY_INTERFACE:
  PASS_STATIC_FROM_PRIOR_EXACT_MAP_GATE

END_TO_END_NATIVE_CORRECTNESS:
  NOT_ESTABLISHED

WHOLE_PIPELINE_CAPACITY:
  NOT_ESTABLISHED

RUNTIME_SPEEDUP:
  NOT_ESTABLISHED

DFR:
  NOT_ESTABLISHED

NOVELTY:
  NOT_ESTABLISHED
```

## What this does and does not save

This does **not** collapse the whole Aung Algorithm-2 MultKey block.

The following remain five-way / branch-local:

- RMFE projection / split path;
- thin SlotsToCoeff;
- key switching to `recryptKeyID`;
- rawModSwitch;
- newMakeDivisible;
- division by (p^{e'}).

The exact structural saving is narrower:

- five copies of
  `recryptEkey.multByConstant(zzParts[1]) + addConstant(zzParts[0])`
  become one;
- five post-raw outputs can enter one RM10/R8 envelope instead of materializing five independent post-reconstruction ciphertexts.

Whether this moves the latency/capacity frontier depends on the cost share of the retained branch-local preprocessing versus the eliminated reconstruction/C2S work. No speedup is claimed here.

## Scientific disposition

The prior candidate

[
	ext{merge before rawModSwitch/newMakeDivisible}
]

remains killed.

A narrower candidate is now structurally alive:

[
oxed{
5	imes	ext{branch-local nonlinear preprocessing}
ightarrow
1	imes	ext{post-raw boot-key reconstruction}
ightarrow
	ext{RM10/R8 recovery}
}
]

This is the first surviving exact mechanism in this line that respects the known p-adic carry boundary.

## Next cheapest decisive test

Before any native task, determine the **source-faithful cost ceiling** of this partial fusion:

1. isolate the baseline cost of branch-local S2C + reLinearize + rawModSwitch + newMakeDivisible from the cost of the eliminated `recryptEkey` multiply/add + C2S;
2. count the exact extra RM10/R8 recovery operations;
3. kill immediately if the optimistic latency ceiling cannot cross the previously established research-value threshold.

Do not run Codex/native execution until that static cost ceiling is favorable.

```text
AI_PROVISIONAL_CHOICE:
  RETAIN_POST_RAW_SINGLE_BOOTKEY_FUSION_FOR_ONE_STATIC_COST_GATE

INDEPENDENT_RESEARCH_AVAILABLE: true
RESEARCH_FRONTIER_EXHAUSTED: false
```
