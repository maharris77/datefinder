# Named timezone normalization and extraction regression coverage

Baseline: `main` at `776faed7a7e4095627f0806e5683bea7f9ca222f`.

## Changes

- Normalize only the lookup key for the four named timezone aliases (`eastern`, `pacific`, `mountain`, `central`). Token matching is case-insensitive, so alias lookup should accept matching capitalization variants. Preserve unknown strings and abbreviations unchanged.
- Preserve selection of the last case-sensitively sorted capture when multiple timezones occur. This change does not redefine timezone precedence or daylight-saving semantics.
- Compare complete extraction result lists, rather than asserting only inside loops that silently pass when no results appear.
- Reconcile the existing `19th day of May` strict fixture with this fork's intentional unknown-year sentinel, `9999`. Do not change the missing-year policy or the existing leap-day limitation.

## Verification and limits

The added regression cases cover lower/title/uppercase aliases, abbreviation and unknown-string fallback, empty captures, and existing multi-timezone precedence and capture immutability.

Initial dependency-free checks passed 18 isolated assertions and syntax parsing; those were not integration verification. After installing the declared runtime/test dependencies into an isolated environment, the actual package test suites were run with `python -m pytest -q -ra`:

- Base `776faed7a7e4095627f0806e5683bea7f9ca222f`: **52 passed, 2 failed**.
- PR code/test head `ad2dbc34270061245e00a1eb261af4a668ab2cbf`: **69 passed, 1 failed, 3 xfailed**.
- Environment: Python 3.12.14, regex 2026.9.29, python-dateutil 3.0.0, pytz 2026.5, pytest 9.1.1, mock 5.2.0.

The base-only failure is the stale `19th day of May` expectation: the existing implementation returns May 19, 9999, rather than no date. This PR reconciles that expectation without changing the policy. Both trees fail the pre-existing `test_tz_gettz_for_all_patterns`: it splits `TIMEZONES_PATTERN` on the literal `|\s` instead of `|`, passing the entire alternation to `tz.gettz`; dateutil 3.0.0 raises an `OSError` for a filename that is too long. No newly introduced failing test was observed. The three strict expected failures confirm the tokenizer limitation below, not a full pass.

All package Python sources, all test modules, and package metadata were materialized from the pinned GitHub trees. Unused HTML/text sample fixtures are not referenced by these tests. This is one Python/dependency combination, not a supported-version matrix or a successful CI run. No runtime dependencies or version pins in the repository were changed.

## Separate follow-up proposal

`.github/workflows/python-package.yml` filters pushes and pull requests to `master`, whereas the current default branch is `main`. A separate change should target `main` after reviewing existing test failures. The workflow is deliberately unchanged in this patch.

The fraction division-by-zero change is already proposed in [PR #1](https://github.com/maharris77/datefinder/pull/1) and is not duplicated here.

## Known tokenizer prefix collision

The helper normalization is not an end-to-end fix for named timezones. In `constants.py`, `ALL_TIMEZONES_PATTERN` places the abbreviation alternation before the named aliases; `EAST` precedes `eastern`, and the timezone alternatives have no ending boundary. Case-insensitive matching can therefore capture `east`/`EAST` rather than the full `eastern`/`EASTERN` token before `_pop_tz_string` runs. This is pre-existing and unchanged by this PR.

The actual package tokenizer confirms the prefix match for lower/title/uppercase eastern. Three strict expected-failure regression cases exercise actual `extract_date_strings` and require the full original timezone capture. They are intentionally limited to `AssertionError` so unrelated errors are not hidden, and an unexpected pass will require removing the expected-failure marker. All three integration cases ran and were reported as expected failures in the current PR suite.

A separate tokenizer fix could put named aliases ahead of abbreviations, which narrowly addresses EAST/eastern, but should evaluate other prefix collisions and word-boundary compatibility before choosing a broader change. No alternation, boundary, or tokenizer semantics are changed in this PR.
