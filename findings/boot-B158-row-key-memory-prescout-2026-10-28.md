# BOOT-B158 — row-key level/memory prescout

Date: 2026-10-28
TRACK_ID: BOOT
Parent: B158 minimal native gate specification

No native run was performed.

## Correction

B158 does not appear to add a new Galois *element* to the complete 9-bit
2026/975 pipeline.

The row-swap element is already required by the low-level Algorithm-5
linear-transform path. B158 instead raises the required LevelQ of that existing
row key from the low polynomial-evaluation region to the high input region.

## Source-level reconstruction

Current 9-bit key summary:

- L19 / logQ~679: 11 Galois keys, total ~660.02 MiB
- L2  / logQ~105: 4 Galois keys, total ~14.00 MiB

For m=1, r=32768, grouped s=2:

neededGaloisElsAlg3 -> neededGaloisElsAlg2 contributes:
- shift 1 from the small BSGS core;
- sum-column shifts 2,4,8,...,8192;
- plus RowRotation.

Step 1 independently requires high-level sparse rotate-and-sum column shifts
1,2,4,...,1024.

Because RotationKeyPlan keeps one key per Galois element at the maximum level at
which it is used, the overlaps shift 1..1024 are promoted to L19.

This leaves exactly four low-level elements:
- shift 2048
- shift 4096
- shift 8192
- RowRotation

matching the observed L2 count of four.

Therefore B158 should promote the existing RowRotation key to approximately
the B158 input level rather than increasing the distinct key count.

## Memory estimate before native measurement

Observed L2 group:
- 14.00 MiB / 4 ~= 3.5 MiB per low-level Galois key

Observed L18 relinearization key:
- ~57.50 MiB

A Galois key at the same Q level has comparable gadget-ciphertext size, so a
reasonable prescout estimate for promoting row-swap L2 -> L18 is:

- new row key ~= 57.5 MiB
- replaced low row key ~= 3.5 MiB
- incremental memory ~= 54 MiB

Against the current ~731.5 MiB evaluation-key footprint this is about a
7--8% increase.

This is an estimate, not a native measurement.

## Decision

- DISTINCT_GALOIS_ELEMENT_INCREASE: EXPECTED 0
- ROW_KEY_LEVEL_PROMOTION: YES
- ESTIMATED_INCREMENTAL_KEY_MEMORY: ~54 MiB
- KEY_MEMORY_BLOCKER: NOT_FOUND
- NATIVE BinarySize measurement remains required

The native-gate report must describe this as a key-level promotion, not as an
additional rotation-key element, unless the actual source plan disproves this
reconstruction.
