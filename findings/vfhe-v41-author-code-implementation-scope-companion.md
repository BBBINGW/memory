# vFHE V41 companion — Springer-linked author source implements kernels, NOT the full range SNARK

2026-10-15. COMPANION to authoritative V41 PDF timestamp / same-day mirror provenance finding, NOT a second numbered iteration. General FHE I192 FROZEN; V42 next SOURCE_VERSION_GATED.

## One independently testable supplemental question and result

Does the author-published GitHub repository explicitly referenced in the Springer CRYPTO2025 vFHE paper include an executable Figure1 / Pi_range grand-product prover/verifier and native F.2 Merkle/RS PCS verifier, allowing the old-mirror e261 false-range transcript to be tested against a COMPILED SNARK? **FAIL for this precisely pinned public source snapshot.** This does NOT imply that authors never built full proof code or that original paper/current revised version is insecure.

## First-party primary source evidence, exact pointers

Publisher DOI https://doi.org/10.1007/978-3-032-01907-3_21 , Springer chapter First Online 2025-08-17, Notes footnote1 links source https://github.com/vfhe/proof-friendly-CKKS . Connected GitHub tool independently retrieved author/public repo vfhe/proof-friendly-CKKS at commit e44d520ae2d6ce05dee088877ebe54f81c029439, pushed 2025-08-28, and its full nontruncated Git tree of 281 nodes including vendored dependencies, directories, binaries and source.

README blob SHA 60bc2c9bb4935bfc48ab94e70081d134a10bcb81 calls code proof of concept and documents just three demo/benchmark commands:
1) python3 -m pyckks.ckks — proof-friendly CKKS multiplication;
2) python3 -m pyckks.bench_sumcheck 10 — Libra-style ring sumcheck kernel;
3) cd lib && make main && ./main — piecewise Reed–Solomon encoding benchmark.

We explicitly fetched 13 first-party project source files at THAT commit; source file exact blob references include lib/src/sumcheck.cpp 488eaf322ab56a0bfcf2ec42cbc92da682e5f911, pyckks/bench_sumcheck.py 76a5fa6dcfd8b6409fd2dc7a06f7e2b9e632acc2, lib/main_benchmark.cpp f92e054ae758ddf3c35e22d1a0294374ef2d6b3e, and pyckks/ckks.py 517f939df7015fa12cfe1c33ab829359be8d1fef. Complete project (excluding vendored Intel HEXL/BLAKE3) file inventory contains 24 files including binaries/pyc. Search of native project source for merkle, grand_product, grandproduct, lookup, range_proof, verify_proof, verify_merkle, fiat_shamir, brakedown found no corresponding complete source. Verified positive functionality: C/Python sumcheck kernel and benchmark, native RNS RLWE/CKKS, RS encoding benchmark. A vendored BLAKE3 hash library does not itself demonstrate a native Brakedown Merkle authentication protocol.

No first-party source implements the complete original Figure1 grand-product transcript check or Appendix F.2 native Merkle/RS commitment and evaluation verifier; no documented entrypoint generates and verifies a full compiled range SNARK. No benchmark was compiled or executed; result is bounded STATIC repository/source inspection, not a universal absence proof.

## Security and provenance boundaries

Canonical V41 primary GitHub-mirror PDF provenance finding is MORE IMPORTANT: the 52-page 836,746-byte mirror's PDF Info CreationDate/ModDate 2026-02-16 strongly corroborate an edition built on the official IACR revision day, but independent official PDF SHA comparison is still absent. The source-ideal e261 CRT counterexample remains established ONLY for exact inspected 52-page mirror, NOT automatically current official 2026 version nor a compiled real proof. This code repository cannot close either missing-evidence gate.

## Decision / reproducibility

**STATUS:** PASS authentic publisher-linked benchmark code attribution; FAIL the narrow hypothesis that a full proof implementation for malicious end-to-end verification exists in this linked public snapshot. No original author defect or exploitation claimed.
**Full local report:** /mnt/data/VFHE_V41_Author_Code_EndToEnd_Implementation_Gate_2026_10_15.md SHA256 6d747c941a412f4aad9bd2388ff0e8b4521da8f99d299630f460d275c6e79751.
**Machine-readable SHA manifest:** /mnt/data/vfhe_v41_author_source_scope_results.json SHA256 be7d6be4b31e7529897e16b42a1e2c22f02d564ac89e4d9e8777248a1d5a9dbe.
**NEXT** unchanged: human supplies byte-authentic latest IACR 2026 official paper and, if claiming compiled exploit, author-identified full original range proof stack; or explicitly authorizes source-complete pivot. Keep V41 COMPLETED, V42 NOT STARTED, SOURCE_VERSION_GATED/HUMAN_REVIEW, global I192 FROZEN.