# Named timezone normalization and extraction regression coverage

Baseline: `main` at `776faed7a7e4095627f0806e5683bea7f9ca222f`.

## Changes

- Normalize only the lookup key for the four named timezone aliases (`eastern`, `pacific`, `mountain`, `central`). Token matching is case-insensitive, so alias lookup should accept matching capitalization variants. Preserve unknown strings and abbreviations unchanged.
- Preserve selection of the last case-sensitively sorted capture when multiple timezones occur. This change does not redefine timezone precedence or daylight-saving semantics.
- Compare complete extraction result lists, rather than asserting only inside loops that silently pass when no results appear.
- Reconcile the existing `19th day of May` strict fixture with this fork's intentional unknown-year sentinel, `9999`. Do not change the missing-year policy or the existing leap-day limitation.

## Verification and limits

The added regression cases cover lower/title/uppercase aliases, abbreviation and unknown-string fallback, empty captures, and existing multi-timezone precedence and capture immutability.

Local verification passed 18 isolated assertions using the actual fetched class methods, plus syntax parsing of the candidate Python files. The isolated fallback replacement check used standard-library `re`; it does not validate the package's `regex` tokenizer. The yearless fixture was verified through `parse_date_string` with the sentinel capture.

The full pytest suite has **not run**. Both `regex` and `pytest` are absent in the available environment; no dependencies were installed. Actual extraction and end-to-end timezone behavior still require execution with the package's dependencies. Isolated assertions are not a substitute for a full suite pass.

## Separate follow-up proposal

`.github/workflows/python-package.yml` filters pushes and pull requests to `master`, whereas the current default branch is `main`. A separate change should target `main` after reviewing existing test failures. The workflow is deliberately unchanged in this patch.

The fraction division-by-zero change is already proposed in [PR #1](https://github.com/maharris77/datefinder/pull/1) and is not duplicated here.
