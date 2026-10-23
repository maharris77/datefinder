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

## Known tokenizer prefix collision

The helper normalization is not an end-to-end fix for named timezones. In `constants.py`, `ALL_TIMEZONES_PATTERN` places the abbreviation alternation before the named aliases; `EAST` precedes `eastern`, and the timezone alternatives have no ending boundary. Case-insensitive matching can therefore capture `east`/`EAST` rather than the full `eastern`/`EASTERN` token before `_pop_tz_string` runs. This is pre-existing and unchanged by this PR.

A separate standard-library regex probe of the exact timezone alternation confirms the prefix match for lower/title/uppercase eastern. This probe is not a run of the package tokenizer. Three strict expected-failure regression cases exercise actual `extract_date_strings` and require the full original timezone capture. They are intentionally limited to `AssertionError` so unrelated errors are not hidden, and an unexpected pass will require removing the expected-failure marker. These new integration cases remain unrun here because `regex` and `pytest` are unavailable.

A separate tokenizer fix could put named aliases ahead of abbreviations, which narrowly addresses EAST/eastern, but should evaluate other prefix collisions and word-boundary compatibility before choosing a broader change. No alternation, boundary, or tokenizer semantics are changed in this PR.
