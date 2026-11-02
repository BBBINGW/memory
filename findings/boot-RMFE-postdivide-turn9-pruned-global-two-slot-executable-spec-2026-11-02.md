# BOOT Research Turn 9/25 — exact 17-call pruned global two-slot executable specification

Date: 2026-11-02  
TRACK_ID: BOOT  
ACTIVE_SUBLINE: B158_CHECKPOINT_DECOUPLED_HALF_BASIS  
Phase: CORRECTNESS_GATE  
Candidate: PRE-TAG + POST-DIVIDE LATE AGGREGATION  
Evidence class: exact plaintext-ring/static canary; NOT native ciphertext correctness.

## Primary hypothesis

Turn 8 established the full-tree global two-slot semantics: with global Frobenius automorphisms and global odd-child monomials, the recovery tree already transports the second physical slot through rho and produces branch-aligned scalar leaves; the inherited post-unpack rho_pos+443 table is therefore double compensation.

The remaining implementation-level uncertainty is whether the *actually pruned* 17-call recurrence, rather than the conceptual full 8192-leaf tree, preserves exactly the same selected leaves and what vector order those five leaves have.

Hypothesis:
a source-style target-pruned recurrence that stores each node's original-coordinate residue class, appends the even child before the odd child, and discards child subtrees that contain no target in J performs exactly 17 automorphisms, returns the same five exact global two-slot Z_625 scalar leaves as the full tree, and has a deterministic output-routing map that can be frozen for the future HElib canary.

Falsifier:
- pruning changes any selected leaf;
- the true call count differs from 17;
- dirty non-target coefficients contaminate a retained leaf;
- the final pruned output order is assumed incorrectly;
- or aligned L0,L1,L2,L3 no longer equal the direct branchwise global-ring reference.

## Pinned semantics

Parameters:
- p=5
- m=32768
- outer plaintext ring degree N=phi(m)=16384
- temporary plaintext modulus 625
- local extension degree d=8192
- J=[0,1024,7168,2048,6144]
- J-order branch labels=[2,0,3,1,4]
- normalization 8192^(-1)=28 mod625.

Global CRT idempotents used by the exact canary:
- e0=313+91 X^8192
- e1=313-91 X^8192.

At split level i=1..13:
- g_i = 5^(8192/2^i) mod 32768;
- tau_i is global F(X)->F(X^g_i);
- s_i=2^(i-1);
- even child = c + tau_i(c);
- odd child = X^(-s_i) (c - tau_i(c)).

Node metadata:
after level i-1, a node labelled residue r represents original coordinates j satisfying
  j == r (mod 2^(i-1)),
with the polynomial internally shifted by -r. Therefore after level i:
- even child keeps residue r modulo 2^i;
- odd child has residue r+2^(i-1) modulo 2^i.

A child is retained iff at least one target j in J has that residue modulo 2^i.

## Exact pruned frontier

The parent counts are exactly:

[1,1,1,1,1,1,1,1,1,1,1,2,4]

so the physical Frobenius count is:

17.

Retained child counts are:

[1,1,1,1,1,1,1,1,1,1,2,4,5]

and exactly five retained odd children require a global monomial multiplication.

The last three levels are:

level 11:
  parents [0]
  children [0,1024]

level 12:
  parents [0,1024]
  children [0,2048,1024,3072]

level 13:
  parents [0,2048,1024,3072]
  children [0,2048,6144,1024,7168].

Therefore the source-style pruned vector's FINAL COORDINATE ORDER is:

  [0,2048,6144,1024,7168]

not canonical J-order:

  [0,1024,7168,2048,6144].

This distinction is essential.

## Branch routing

Canonical labels are defined in J-order:

J:
  [0,1024,7168,2048,6144]
labels:
  [2,0,3,1,4].

Consequently, in the actual pruned-vector order

  [0,2048,6144,1024,7168]

the branch order is

  [2,1,4,0,3].

To obtain canonical branch order [0,1,2,3,4] directly from the pruned vector, use indices:

  [3,1,0,4,2].

Equivalently, a safer implementation is to key every retained leaf by its coordinate and only then assemble canonical J-order / branch-order arrays.

IMPORTANT:
Turn 8's full-tree indices [0,4,7,2,3] refer to positions in the COMPLETE 8192-leaf binary tree. They are NOT indices into the five-element pruned output vector and must not be reused as such.

## Exact global two-slot dirty canary

One deterministic exact-Z625 canary was evaluated entirely in

R=(Z/625Z)[X]/(X^16384+1).

Distinct branch values were used in the two physical CRT components:

slot0=[11,22,33,44,55]
slot1=[101,202,303,404,505].

The five tagged target coefficients follow J-order labels [2,0,3,1,4].

To prevent a sparse-only false positive, deterministic 5-divisible off-target dirty coefficients were added at:

[1,3,17,511,1023,1025,1536,3072,4095,4096,5000,7000,8191].

The exact source-style pruned recurrence then produced:

calls=17
parent_counts=[1,1,1,1,1,1,1,1,1,1,1,2,4]
child_counts=[1,1,1,1,1,1,1,1,1,1,2,4,5]
odd_monomial_mults=5
pruned_coord_order=[0,2048,6144,1024,7168]
pruned_branch_order=[2,1,4,0,3]
reorder_to_branch=[3,1,0,4,2].

After multiplying every leaf by 28, all five outputs exactly equalled the corresponding two-slot CRT scalar coefficient at the target coordinate. All off-target dirty terms were eliminated from those leaves.

Result:

PASS_PRUNED_GLOBAL_TWO_SLOT_EXACT_Z625_LEAVES.

## Exact L0..L3 closure

Using the inherited exact RMFE basis coefficient lists, ordinary aligned global correction constants were constructed for phi(e_i)^(5^r), r=0,1,2,3.

The five pruned outputs were first routed by target coordinate, not by their vector position. The four correction images were then compared against a direct branchwise global-ring reference.

Results:

L0 exact mod625: PASS
L1 exact mod625: PASS
L2 exact mod625: PASS
L3 exact mod625: PASS.

No post-unpack rho_pos or 443 compensation was applied.

Therefore:

PASS_PRUNED_ROUTING_EXACT_L0_L3.

## Scientific consequence

Turn 8 proved the correct global two-slot semantics; Turn 9 now supplies the exact *pruned executable specification* that the missing HElib implementation must realize.

The remaining correctness blocker is no longer ambiguous tree algebra or routing. A future concrete HElib witness has an exact acceptance oracle:

1. use global Frobenius and global X^(-s) odd-child multipliers;
2. preserve coordinate-residue metadata through pruning;
3. execute exactly 17 parent automorphisms;
4. normalize each retained leaf by 28;
5. require final coordinate set exactly {0,1024,7168,2048,6144};
6. if stored in source-style vector append order, require [0,2048,6144,1024,7168];
7. route by coordinate or reorder pruned-array indices [3,1,0,4,2] to branch order;
8. do NOT apply the obsolete post-unpack rho_pos+443 table;
9. require exact Z_625 L0,L1,L2,L3 equality against the direct global-ring reference.

This is still not native ciphertext correctness, baseline correctness, security, DFR, or performance evidence.

## Verdict

PASS_PRUNED_17_CALL_EXECUTABLE_SPEC
PASS_PRUNED_GLOBAL_TWO_SLOT_EXACT_Z625_LEAVES
PASS_PRUNED_ROUTING_EXACT_L0_L3
REFINE_TURN8_FULLTREE_INDEX_ORACLE_FOR_PRUNED_IMPLEMENTATION

CORRECTNESS_GATE remains BLOCKED pending concrete HElib/current-candidate source and native correctness.

NOVELTY_STATUS remains PREFLIGHT.
SECURITY_GATE remains PENDING.
VALUE_GATE remains PENDING.
PAPER_READINESS remains NOT_READY.

## Durable companion

Compact canary output:
findings/boot-RMFE-postdivide-turn9-pruned-global-two-slot-canary-2026-11-02.txt
