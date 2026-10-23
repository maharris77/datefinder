# Named timezone normalization and extraction regression coverage

Baseline: `main` at `776faed7a7e4095627f0806e5683bea7f9ca222f`.

## Changes

- Normalize only the lookup key for the four named timezone aliases (`eastern`, `pacific`, `mountain`, `central`). Token matching is case-insensitive, so alias lookup should accept matching capitalization variants. Preserve unknown strings and abbreviations unchanged.
- Preserve selection of the last case-sensitively sorted capture when multiple timezones occur. This change does not redefine timezone precedence or daylight-saving semantics.
- Prefer the four full named timezone aliases before abbreviation alternatives so EAST no longer truncates eastern. Other abbreviation ordering and the sorted multi-capture selection are unchanged.
- Compare complete extraction result lists, rather than asserting only inside loops that silently pass when no results appear.
- Reconcile the existing `19th day of May` strict fixture with this fork's intentional unknown-year sentinel, `9999`. Do not change the missing-year policy or the existing leap-day limitation.

## Verification and limits

The added regression cases cover lower/title/uppercase aliases, abbreviation and unknown-string fallback, empty captures, and existing multi-timezone precedence and capture immutability.

Initial dependency-free checks passed 18 isolated assertions and syntax parsing; those were not integration verification. After installing the declared runtime/test dependencies into an isolated environment, the actual package test suites were run with `python -m pytest -q -ra`:

- Base `776faed7a7e4095627f0806e5683bea7f9ca222f`: **52 passed, 2 failed**.
- Initial PR code/test head `ad2dbc34270061245e00a1eb261af4a668ab2cbf`: **69 passed, 1 failed, 3 xfailed**.
- Final alias-first code/test candidate: **82 passed, 1 failed, no xfails**. This includes 12 actual alias-extraction variants and a regression test containing 1,161 abbreviation-matching comparisons.
- Environment: Python 3.12.14, regex 2026.9.29, python-dateutil 3.0.0, pytz 2026.5, pytest 9.1.1, mock 5.2.0.

The base-only failure is the stale `19th day of May` expectation: the existing implementation returns May 19, 9999, rather than no date. This PR reconciles that expectation without changing the policy. Both trees fail the pre-existing `test_tz_gettz_for_all_patterns`: it splits `TIMEZONES_PATTERN` on the literal `|\s` instead of `|`, passing the entire alternation to `tz.gettz`; dateutil 3.0.0 raises an `OSError` for a filename that is too long. No newly introduced failing test was observed. The initial three strict expected failures confirmed the tokenizer collision below. They were replaced with passing ordinary regression cases after the narrow alias-ordering fix; the shared diagnostic failure remains unmasked. This is not a full suite pass.

All package Python sources, all test modules, and package metadata were materialized from the pinned GitHub trees. Unused HTML/text sample fixtures are not referenced by these tests. This is one Python/dependency combination, not a supported-version matrix or a successful CI run. No runtime dependencies or version pins in the repository were changed.

## Separate follow-up proposal

`.github/workflows/python-package.yml` filters pushes and pull requests to `master`, whereas the current default branch is `main`. A separate change should target `main` after reviewing existing test failures. The workflow is deliberately unchanged in this patch.

The fraction division-by-zero change is already proposed in [PR #1](https://github.com/maharris77/datefinder/pull/1) and is not duplicated here.

## Resolved named-alias prefix collision and remaining limits

The original `ALL_TIMEZONES_PATTERN` placed abbreviation alternatives before named aliases. Since `EAST` appears before `eastern` and there is no ending boundary, actual extraction captured `east`/`EAST` instead of the complete name. The final change puts the four named aliases before the existing abbreviation alternation, without reordering abbreviations or changing boundaries.

Twelve ordinary regression cases now exercise actual `extract_date_strings` for lower/title/uppercase eastern, pacific, mountain, and central. They require both the full source match and complete timezone capture. A separate regression compares old and new matching for every existing abbreviation in three capitalization forms: 1,161 comparisons passed. The original three strict expected-failure markers were removed because their cases now pass.

This is a token-recognition and helper-lookup fix, not a DST or timezone-database fix. Abbreviations such as PST/CST can still fail to resolve in the installed timezone database; successful token extraction does not guarantee a timezone-aware datetime. Other abbreviation-to-abbreviation prefix collisions and word-boundary behavior are deliberately outside this change.
