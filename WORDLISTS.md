# Bundled Wordlists: Provenance and Release Status

**Audit date:** 2026-11-06  
**Scope:** Local, read-only inspection of the text-list files included in this repository snapshot.

The wordlists are not required by the Distort Python package or its test suite. They are retained in the repository for compatibility, but their presence in a public repository does not establish permission to redistribute them.

## Inventory

| File | Observed size | Origin | Licence | Redistribution status |
| --- | ---: | --- | --- | --- |
| `10k-most-commonlist.txt` | 10,000 lines; 73,017 bytes | **Unknown / Unverified.** The filename resembles SecLists' `10k-most-common.txt`, but the names differ and an exact source match was not established. | **Unknown / Unverified** | Pending source and permission confirmation. |
| `Wordlists/10-million-password-list-top-1000000.txt` | 999,998 lines; 8,529,108 bytes | **Likely source family:** SecLists' `Passwords/Common-Credentials` list uses this exact filename. The local file was not verified byte-for-byte against that upstream copy. | **Unknown / Unverified for this asset.** The SecLists repository is marked MIT-licensed, but that alone does not establish the provenance or rights for this particular data file. | Pending exact-source and asset-level permission review. |
| `Wordlists/500-worst-passwords.txt` | 499 lines; 3,988 bytes | Weakpass catalogs a similarly named 500-entry list and attributes it to `wiki.skullsecurity.org`. The local file's MD5 (`54c369da44bbb3ddc7e087f7a8ec9668`) differs from the Weakpass reference (`396bb2f634884f279c8bd96092833df3`), so the exact source copy is **not verified**. | **Unknown / Unverified** | Pending source and permission confirmation. |
| `passwordlist.txt` | 100,000 lines; 951,083 bytes | **Unknown / Unverified.** Weakpass has a same-name catalogue entry that reports a torrent collection as its source, but its reference MD5 (`d0a7018ff3e9693b7ee6b1ceb346eb8a`) differs from the local file. This is a lead, not verified provenance. | **Unknown / Unverified** | **Quarantine from future public releases pending manual review.** Do not further redistribute until its contents, source, and rights are established. |
| `Wordlists/passwordlist.txt` | 100,000 lines; 951,083 bytes | Byte-identical duplicate of root `passwordlist.txt`; see the same provenance concern above. | **Unknown / Unverified** | Same quarantine recommendation as the root copy. |

## Local content checks

No wordlist contents were uploaded to third-party scanning services. The following checks were run locally: UTF-8 decoding, line and duplicate counts, maximum line length, and heuristic searches for email-like strings, URL-like strings, IP-address-like strings, phone-number-shaped strings, hash-shaped tokens, and colon-delimited records.

| File | Local heuristic observations |
| --- | --- |
| `10k-most-commonlist.txt` | No email-, URL-, or hash-shaped matches. A small number of IP-/phone-shaped tokens were flagged. |
| `Wordlists/10-million-password-list-top-1000000.txt` | No email-, URL-, or common hash-shaped matches. Numeric strings, phone-number-shaped strings, IP-address-shaped strings, and one colon-delimited line were flagged. |
| `Wordlists/500-worst-passwords.txt` | No email-, URL-, IP-address-, or hash-shaped matches were detected by these checks. |
| `passwordlist.txt` and `Wordlists/passwordlist.txt` | The scan flagged 2 email-like lines, 18 colon-delimited lines, 1 URL-like line, 1 MD5-shaped token, and phone-number-shaped strings. The longest line is 620 bytes. These are indicators for review, not proof of leaked or private credentials. |

These checks are heuristic and can produce false positives (for example, numeric password candidates can resemble telephone numbers). They cannot establish that a list is safe, complete, lawfully sourced, or free of personal information. A clean scan is not a safety certification.

## File fingerprints

SHA-256 fingerprints of the inspected files:

| File | SHA-256 |
| --- | --- |
| `10k-most-commonlist.txt` | `4adb3f0afb4a10cf19ebe48d8c69a46f934bbc8d77c694c210564f9583e7f4ba` |
| `Wordlists/10-million-password-list-top-1000000.txt` | `1843265e3860a97f417b2236dfa332a0d93b38efef0fee1a0a291fdba5458478` |
| `Wordlists/500-worst-passwords.txt` | `aadf36a80e15bc6ad7c886c0c76cf567f181bc61dfd99faa453755aa1ae36052` |
| `passwordlist.txt` and `Wordlists/passwordlist.txt` | `f7268cd297da1f1acc7b1fee505d8a1d30cc60cf1f366f2babc996582d72f4c5` |

The two `passwordlist.txt` files have identical SHA-256 fingerprints and are byte-for-byte duplicates.

## References and limitations

These public references helped identify possible origins; they do **not** prove that the local files are identical to the referenced copies or that their redistribution is permitted:

- [SecLists common-credentials 1M list](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt)
- [SecLists 10k common-password list](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10k-most-common.txt)
- [Weakpass: 500-worst-passwords.txt](https://weakpass.com/wordlists/500_worst_passwords.txt)
- [Weakpass: passwordlist.txt](https://weakpass.com/wordlists/passwordlist.txt)

No trustworthy source version/date or asset author attribution was present in the inspected wordlist files. The supplied project archive does not contain Git history. The public GitHub repository page currently reports one commit, which is not enough to establish a complete chain of authorship or the rights attached to bundled data. No copyright notice or per-file licence was found in the inspected wordlist files.

The [SecLists repository](https://github.com/danielmiessler/SecLists) identifies the repository as MIT-licensed, but that repository-level statement does not independently establish the origin or redistribution terms of the exact local data file.

## Release recommendations

1. Obtain and record the original source, version/date, licence, attribution requirements, and redistribution permission for each list.
2. Manually review `passwordlist.txt` and its duplicate in a controlled local environment. Keep them out of future release archives until that review is complete.
3. Do not assume Distort's MIT source-code licence also licenses any bundled wordlist. Keep third-party data under its own verified terms or remove it from distribution after maintainer approval.
4. Preserve the fingerprints above when comparing replacement or re-sourced files.

No wordlist file was deleted or modified as part of this audit. The wordlists remain in place pending the maintainer's decision.
