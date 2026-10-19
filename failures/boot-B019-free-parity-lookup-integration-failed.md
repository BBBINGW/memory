# BOOT-B019 failure archive — No free import into existing exact HasteBoots lookup

TRACK_ID: BOOT
DATE: 2026-10-19
ITERATION: B019
STATUS: FAIL_FREE_INTEGRATION / NOT_A_GENERAL_IMPOSSIBILITY

The B018 Goldilocks odd-prime parity lemma is correct under SAME canonical integer witnesses and their tight bounds. However HasteBoots official f7ed/HasteBoots current source (snarks/src/fhe_op/external_product.rs, trace/src/lookup_trace/small_table.rs, README.md) proves range for exact small gadget digits (Zama comparison B=2^5, ell=13). It has no preexisting 41/42-bit approximate rounding-remainder trace. To integrate a 2025/686 approximate single-level gadget with Q=2^64, B=2^23 or22, a concrete radix-32 witness layout needs approx 5 digit lookups, 9 remainder lookups, 1 binary carry and potentially 13 canonical x-word lookups when the torus input is not already bound. Thus the local one-bit parity property does NOT imply one-bit or zero marginal TOTAL proof cost, much less faster complete PBS proof. Exact counts are a natural implementation layout, not proof lower bounds or matched empirical cost.

ATTACK on naive independent proofs: q=256,p=251,B=G=16, x=0,d=0,r_field=-5,w=1, so e=-251=0 mod p but e!=0 in integers. Another unbound r_parity=-4 passes x≡r_parity mod2. Joint proof must bind the same r. Also x=0 vs x=251 have the same field image but distinct q=256 torus values, showing field-only x commitments do not necessarily bind canonical torus inputs.

POSITIVE REPAIR: Given an already committed, properly bounded remainder r'=r+G/2 and trusted x parity b, replace low 5-bit limb r0'∈[0,32) by 2u+b with u∈[0,16). A 4-bit lookup replaces the old 5-bit lookup with no extra lookup COLUMN for parity, and reconstruction/commitments must use same u/b. At private x, share Boolean bit b between x0=2v+b and r0'=2u+b, introducing at least bit binding. Exhaustive q256 toy checks 256 good and zero bad witness after this repair. This does not rescue nonexistent remainder/boundary witness in old HasteBoots.
FINDINGS: findings/boot-B019-lookup-parity-shared-witness-gate.md.
NEXT B020: test two-lift (Goldilocks z, parity b) as compressed exact canonical 64-bit torus representation and one-step operation closure/cost. Goldilocks p odd with p<2^64<2p gives up to two lifts, which parity distinguishes; must prove validity for z<2^32-1 when upper lift and tie to ciphertext trace, not just field output.
All source fidelity, security, prover-cost and prior art constraints retained. BOOT only.