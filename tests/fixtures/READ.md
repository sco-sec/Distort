# Legacy mutation baseline fixtures

These candidate-set snapshots were generated offline from the earliest available
verified Distort package archive (`Distort-upgraded.zip`), using its
`src/distort/mutations.py` implementation. The SHA-256 of that archived source
file is:

`1cad63ce66c22c149eabcb5093106458e5f0cc806fdb62370952c488d008671f`

The supplied archives do not contain `.git` metadata or the original pre-refactor
script. Accordingly, these fixtures are documented as baselines from the earliest
available verified package implementation, not as independently recovered
pre-refactor Git-history outputs.

Each fixture contains the complete candidate set for the combined synthetic
seeds `example`, `security`, and `testing` at the level in its filename. One
candidate is stored per line. The files are sorted for review, but regression
tests compare sets so historical set iteration order is not treated as a
compatibility guarantee. Tests separately verify the current deterministic,
sorted output and duplicate suppression.
