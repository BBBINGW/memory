# CGS-34 — Public Gaussian pad delivery with a reused PartDec mask exposes the RLWE secret

Date: 2026-10-15. Active CGS single GitHub Notes workflow; last completed CGS-33. One hypothesis and one decisive falsifying test. This is an attack on a newly proposed variation, NOT on unmodified Okada–Takagi.

## Primary hypothesis and minimal test

H-CGS34 [FAIL]: The existing semi-honest noncolluding Server could generate fresh Shamir shares of source Gaussian padding online, broadcast each active participant's masked contribution using that participant's EXISTING PartDec PRF output m_i, and eliminate O(LDec) pre-shared padding without leaking FHE shares or adding more PRF domains. The proposed public transport value is d_i = lambda_i*zeta_i + m_i, with PartDec_i = lambda_i*(a*s_i+zeta_i)+m_i.

Falsifier: The source Algorithm 5 ODec transcript exposes the entire set of PartDec replies. Can an observer combine the public d_i and PartDec_i for a legal active set, and recover the original FHE secret from one session when a is a unit?

## Original source, full-text grounding [FACT]

Hiroki Okada and Tsuyoshi Takagi, Low Communication Threshold FHE from Standard (Module-)LWE, ASIACRYPT 2025, ePrint 2025/409, https://eprint.iacr.org/2025/409. Used 40-physical-page GitHub mirrored version, PDF SHA256 98993522b80695ab415cc5d8c28dddc1dbe8b78ac3550d2063140ce718c6a301, VERSION_UNVERIFIED (its printed p5 says Ver.4 March 26, 2026).
- Algorithm 7 physical p29 KeyGen stores independent zeta per sid and Shamir-shares each; PartDec line17 returns lambda_i*(a*s_i+zeta_i)+m_i, where m_i=PRF(seed_i,sid).
- Algorithm 6 p26 is the scalar analogous original.
- Algorithm 3 pp19-20 / Definition 4.2 p18: Server broadcasts one processed ciphertext in first online round; parties broadcast their PartDec_i in second round. Server must not receive the parties' replies under noncollusion, but other participants do.
- Algorithm 5 p23 ODec gives the adversary ctdec and ALL active replies, including honest participants. Thus the attacker can observe any newly broadcast d_i and the source-style PartDec_i.
- Original source §5 discussion p25 separately asserts semantic security AGAINST untrusted semi-honest Server on the basis that it sees only FHE ciphertexts and public material, not secret shares. Giving the Server hidden key-related covariance Sigma_s changes that proof interface.
- An older public web-indexed PDF of the same ePrint had 36 pages, dated March 4 2025, and different algorithm numbers; never mix it with source newer 40-page Algorithm7. A web PDF screenshot was attempted; ePrint HTTP403 blocked the visual screenshot. Thus all equation claims here come from the full newer source fetched with the Research MCP.
- CGS-16/19/20/21 prior results already excluded naive PRSS and interactive online rounding ports. This mask-reuse gate is a particular new transcript algebra falsifier, not an impossibility theorem for all dealer approaches.

## Key recovery algebra [DERIVATION]

Fix a legal active set of at least threshold T parties and Shamir interpolation weights lambda_i such that the secret satisfies sum_i lambda_i*s_i=s in R_q. The proposed public masked transfer and source-style reply are

d_i=lambda_i*zeta_i + m_i,
PartDec_i=lambda_i*(a*s_i+zeta_i)+m_i.

Subtract PUBLIC observables:
PartDec_i-d_i=lambda_i*a*s_i.

Sum over the active set:
Z=sum_i (PartDec_i-d_i)=a*sum_i(lambda_i*s_i)=a*s.

When the public ring element a is a unit in R_q=F_q[X]/(X^n+1), any observer computes the FULL secret
s=a^{-1} Z.

No honest PRF seed, Shamir share or Gaussian share is needed. The algebra is independent of how zeta was sampled. This is a one-session complete RLWE-key recovery for module rank 1 and unit a. For module rank k>1, one session exposes the linear inner product of a and s; sufficient sessions with ring-linearly independent a rows can recover s. Do not assert one session always suffices for k>1 or a nonunit a.

For q prime splitting X^n+1 into n distinct linear factors, a truly uniform a is invertible with probability (1-1/q)^n, but source distribution of a and arbitrary q need independent parameter verification. The single explicit unit-a transcript is a decisive counterexample to a universal confidentiality assertion.

## ONE exact executable test [PASS attack]

Python /mnt/data/cgs34_server_pad_mask_collision_gate.py, SHA256 8256e9dcbbb7815acf9a0594654e18cade1a82b51e6fd00938d4172808003c9b.
Output JSON /mnt/data/cgs34_server_pad_mask_collision_results.json, SHA256 a79542d2ae56719326db3f9e931b6a05c6cd5ed361c358aa9cfa27ec9e34d0de.
Deterministic seeded test uses exact modular ring arithmetic, not a CSPRNG nor real cryptosystem implementation.

Choose n=4, q=17, R_q=F_17[X]/(X^4+1), N=3 parties, T=2, act={1,2}, interpolation weights lambda_1=2, lambda_2=-1 mod17. Original secret s=1-X^2+X^3. Public a=1+X has inverse (1-X+X^2-X^3)/2 since (1+X)(1-X+X^2-X^3)=1-X^4=2 mod X^4+1.

Generated one consistent randomized linear Shamir polynomial per coefficient of secret s and independent secret-conditioned pad value zeta (sampled arbitrary ring coefficients for algebra), independent masks m_i, all d_i and replies. Observed sum_i(PartDec_i-d_i)=X-X^2, and multiplying by a^-1 RECOVERS exactly s=1-X^2+X^3 in a single session. All assertions pass. Toy random zeta is not claimed to have the real Gaussian distribution; cancellation works for every zeta, so this is sufficient.

## Candidate repairs and source-model cost gate [DERIVATION, not complete schemes]

1. Domain-separated masks. Change transport to d_i=lambda_i*zeta_i+n_i with n_i=PRF(seed_i,"pad",sid,act), and use independent m_i=PRF(seed_i,"dec",sid,act) in replies. Then PartDec_i-d_i=lambda_i*a*s_i+(m_i-n_i); the literal public cancellation no longer works. The toy verified direct recovery FAILS with independent n_i. This is only a narrow repair, NOT full privacy or adaptive-simulation security. The online server broadcast now carries |act| extra ring values of size n log q bits each, thus grows in N instead of original O(1)-with-N broadcast size.
2. Stronger algebraic control, worthy of next iteration: If Server knows Sigma_s and directly samples zeta, it can send NO per-party zeta_i at all. Instead it replaces ctdec,1=b with b'=b-zeta and parties use source §5 pad-free replies lambda_i*a*s_i+m_i. Since sum_i lambda_i zeta_i=zeta, the recovered aggregate residual exactly matches original's padded version:
b-sum_i[lambda_i*(a*s_i+zeta_i)+m_i]
= (b-zeta)-sum_i[lambda_i*a*s_i+m_i].
The toy independently verified this identity. It preserves original two-round, one processed ciphertext, O(1) ring broadcasts in N. This proves only correctness algebra and aggregate-noise law under a common coupling, NOT party partial-share simulator security.
3. All online Server-generated zeta schemes still need secret-conditioned covariance Sigma_s=sum_j Gram(s_j). Source ServerDec has no Sigma_s input; the existing untrusted, noncolluding semi-honest Server knows public ciphertexts and PRF seeds but not this FHE secret statistic. Privately sending Sigma_s once at trusted KeyGen would require a new Server-side key-dependent setup input. Source §5 p25's server-side FHE semantic-security proof does not automatically apply when Server sees (pk, evk, Sigma_s). Establishing that leakage is safe under STANDARD MLWE reopens known-covariance MLWE-style hardness, the barrier from CGS-32/33. Noncollusion alone does not mean Server is trusted to learn auxiliary secret leakage. Nor does the original source fully specify the efficient exact multivariate discrete Gaussian sampler for arbitrary Sigma; costs must be counted.

## End of iteration

ITERATION: CGS-34.
STATUS: FAIL same-PRF public per-party masked pad transport; PASS exact one-session RLWE full-key recovery toy and general cancellation identity. PASS only aggregate algebra for separate potential Server direct b-shift. UNKNOWN security/utility of any source-respecting online dealer. No source attack or new secure ThFHE claimed.
RESULT: If d_i=lambda_i*zeta_i+m_i and PartDec_i=lambda_i*(a*s_i+zeta_i)+m_i are both public, then sum_i(PartDec_i-d_i)=a*s, and unit a gives exact s. Thus reuse of the same mask for pad transport and reply is catastrophic. Domain separation avoids only this particular subtraction, with O(|act|) broadcast overhead. Direct Server shift has better communication algebra but needs secret-dependent covariance at Server, changing trust/security.
NEXT_TEST CGS-35 (PI next "继续"): test ONE concrete Server-direct b-shift candidate. Can trusted setup provide Sigma_s privately to untrusted Server without violating original server plaintext confidentiality under standard MLWE? Formalize public/key leakage game, perhaps give one tiny distinguishing case but do not mistake secret-norm leakage for plaintext attack. Compare O(LDec) storage vs Server single Sigma state, without pretending original semantic-security theorem inherits. If impossible under same assumptions, PARK dealer branch and return to genuinely hidden on-demand conditional share generation.
STATE_UPDATE: YES single root, CGS history, own finding. Other project files untouched.
