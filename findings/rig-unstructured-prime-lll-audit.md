# RIG Fourier attack: predeclared conventional NTT prime, LLL certificate

Date: 2026-10-10
STATUS: PASS — ONE finite-instance falsification of 'weak roots only occur for purpose-built q=a^N+1 or Proth q=c*2^k+1'.
NOVELTY: NOT VERIFIED / likely low: weak polynomial evaluations, short dual lattice relations, and hidden-permutation mixture principle overlap with established prior art.
HUMAN: decide whether to continue at realistic dimensions or archive; no autonomous broad parameter sweeps.

## Sources and assumptions
User manuscript (2026-09-10) FHE_from_RIG (1).pdf: RIG-HE symmetric ciphertext Enc_pi(m)=pi(NTT(t e+m) || uniform padding), with n<=N extra uniform coordinates. Sufficient repeated-squaring correctness q > 2*H_L where H_L=N^(2^L-1)*H0^(2^L), H0=floor(t/2)+t B.
Earlier derivation: rig_fourier_attack_and_research_decision.tex/pdf; findings/rig-fourier-prior-art-audit.md. For binary messages t=2, odd v0, v_k = v0 r^k mod q, coefficient iid centered Gaussian variance <=sigma^2:
  beta>=1-2*pi^2*sigma^2*||v||^2/q^2,
  p=N/(N+n),
  Pr[correct]>=1/2+(p*beta/4)*(1+cos(pi*v0/q)).
These formulae assume the source's error representation/law, not arbitrary canonical Gaussian.

## Precisely ONE predeclared test
N=n=32, t=2, sigma=1, B=14, L=4, K=8. Select the first q strictly >2^160 with q=1 mod 64 and passing Sympy prime screen, i.e. q=2^160+64*i+1 for the least i>=1. Found i=68:
 q=1461501637330902918203684832716283019655932547329
 q.bit_length()=161, q-1=2^160+4352, v2(q-1)=8.
 q is NOT a^32+1, NOR a Proth-style construction with small odd cofactor and huge power of two; selection did not require factorable q-1. Only after selection, computed recursive primality certificate.
 2*H_L=18908088956230290401794697920047243944689401856
 q/(2*H_L)=77.29504767584311 >1.

## Exact primality/NTT certificate [FACT / CHECKED]
Full recursively verifiable Pratt/Lucas certificate: /mnt/data/fhe_audits/rig_unstructured_prime_lll_certificate.json (includes complete nested certificates, primitive generators and factorizations for each prime factor).
Full factorization q-1:
 2^8 * 3 * 7^2 * 13 * 23 * 2203 * 3631 * 2698853 * 615161 * 9780522292915672686209.
For each node p, the verifier checked full factorization p-1, each child primality certificate, pow(g,p-1,p)=1 and gcd(g^((p-1)/ell)-1,p)=1 for every distinct prime ell|p-1. Total 136 nodes checked (including repeated nested factors).
Fix first g>=2 such that r=g^((q-1)/64) mod q satisfies r^32=-1: g=29, r=570268124029534407621996591794583635795426001824. Exact order 64.

## Short public Fourier vector [FACT / CHECKED]
Basis rows (1,r,...,r^31), q*e_1,...,q*e_31, LLL delta=3/4 over exact integers in dimension 32. Among odd nonzero first-coefficient rows, choose minimum squared norm; row index 31.
v0=-13706623602647070681429815405287290986390816143, odd.
All 32 congruences v_j-v0*r^j=0 mod q verified EXACTLY. Full v coordinates and squared norm in JSON certificate.
rho=||v||/q=0.07127678867526673, versus predeclared 1/(4*pi)=0.07957747154594767. Also checked *integer-only* 88^2 ||v||^2 < 49 q^2; since pi<22/7 this proves rho <7/88 <1/(4*pi).
All 32 primitive NTT roots have centered integer representative absolute value >= 0.11042706156668128*q. Thus NO visibly tiny primitive NTT root is responsible for this witness.
Fourier beta lower (using numerical pi)=0.8997173064658956. Strict conservative rational inequality using pi<22/7 gives beta>0.8996365627645887 and cos(pi*v0/q)>0.9995656081714391, hence Pr[correct]>0.7248602913447048 for single t=2 challenge (p=1/2). These are mathematical conditional lower bounds, not measurements.
A deterministic seeded Monte Carlo of 20,000 simulated challenges, sampling an independently hidden but fixed permutation and original ciphertext generation, produced 14,485 correct (72.425%, approx 95% CI 71.8% to 73.0%). This serves as a cross-check only.

## Interpretation [BOUNDARY]
- PASS: weak short-relation/Fourier evaluation can occur for ONE publicly selected prime that has no engineered small NTT root and satisfies the user's conservative correctness bound.
- NO claim that all or most unstructured NTT primes are weak, nor that conventional ~60-bit RNS-limb moduli are weak, nor practical security at large dimensions. N=32 is a toy/insecure ring dimension in its own right.
- The prime's q bitlength is enormous relative to N; the bound intentionally addresses a parameter tension where correctness demands huge q.
- Known prior art includes Elias-Lauter-Ozman-Stange, ePrint 2015/106 and 2015/758 (small residues/full-order roots and error evaluation tests); short lattice dual Fourier arguments are classical. Handling random hidden positions by mixture with independent padding only reduces bias by p; this elementary step is not established new.
- No claim that a conditional theorem 'restricted-source hard => RIG-HE secure' is logically refuted.

## Artifacts
/mnt/data/fhe_audits/rig_unstructured_prime_lll_audit.py
/mnt/data/fhe_audits/rig_unstructured_prime_lll_certificate.json
These are session-local research artifacts, not guaranteed to exist in every future conversation; request them as needed or re-run script.

## End of iteration
STATUS: PASS (one predetermined non-engineered 161-bit NTT prime).
RESULT: Exact primality certificate, correctness bound, LLL vector, strict Fourier bias and single-challenge CPA lower bound, empirical cross-check.
NEXT_TEST: HUMAN_REVIEW. The only potentially worthwhile extension is whether analogous correctness/security conflict can be demonstrated for realistic larger N with a predeclared modulus rule, compared fairly with established dual/evaluation attacks. No more toy-prime parameter sweep without lead authorization.
STATE_UPDATE: YES, finding saved; RIG workstream not archived.
