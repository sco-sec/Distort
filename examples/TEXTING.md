# Examples

`input.txt` contains synthetic seed words suitable for demonstrations and tests.

Generate candidates at level 7:

```bash
distort -i examples/input.txt --level 7
```

Write them to a file instead of stdout:

```bash
distort -i examples/input.txt --level 7 --output candidates.txt
```

Candidate output is deterministic for the same Distort version, input, and mutation level.
