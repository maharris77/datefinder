import pytest
import datefinder
import sys, logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

#TODO: many more TZINFO examples

@pytest.mark.parametrize('date_string, expected_match_date_string', [
    ['March 20, 2015 3:30 pm GMT ', 'March 20, 2015 3:30 pm GMT'],
    ['March 20, 2015 3:30 pm ACWDT in the parking lot', 'March 20, 2015 3:30 pm ACWDT'],
    ['blah blah March 20, 2015 3pm MADMT for some thing', 'March 20, 2015 3pm MADMT'],
    ['we need it back on Friday 2p.m. central standard time', 'on Friday 2p.m. central standard time'],
    ['the big fight at 2p.m. mountain standard time on ufc.com', 'at 2p.m. mountain standard time on'],

    # issue: Thu not recognised by regex #138
    ['starting Thursday 2020-11-05 13:50 GMT', 'Thursday 2020-11-05 13:50 GMT'],
    ['starting Thu 2020-11-05 13:50 GMT', 'Thu 2020-11-05 13:50 GMT'],
])
def test_extract_date_strings(date_string, expected_match_date_string):
    dt = datefinder.DateFinder()
    matches = list(dt.extract_date_strings(date_string))
    assert [match[0] for match in matches] == [expected_match_date_string]
    for actual_date_string, indexes, captures in matches:
        logger.debug("actual={}  expected={}".format(actual_date_string, expected_match_date_string))
        assert actual_date_string == expected_match_date_string
        assert len(captures.get('timezones',[])) > 0, "timezone expected in result"

# Compare complete result lists so missing positive matches cannot pass silently.

@pytest.mark.parametrize('date_string, expected_match_date_string', [
    ['the Friday after next Tuesday the 20th', ''], # no matches
    ['This Tuesday March 2015 in the evening', ''], # no matches
    ['They said it was on 01-03-2015', 'on 01-03-2015'], # 3 digits strict match
    ['May 20 2015 is nowhere near the other date', 'May 20 2015'], # one month two digit match
])
def test_extract_date_strings_with_strict_option(date_string, expected_match_date_string):
    """
    make sure that `strict` mode works for the dates we care about
    and doesn't work for others

    :param date_string:
    :param expected_match_date_string:
    :return:
    """
    dt = datefinder.DateFinder()
    matches = list(dt.extract_date_strings(date_string, strict=True))
    expected = [expected_match_date_string] if expected_match_date_string else []
    assert [match[0] for match in matches] == expected


@pytest.mark.parametrize('timezone', ['eastern', 'Eastern', 'EASTERN'])
@pytest.mark.xfail(
    strict=True,
    raises=AssertionError,
    reason='Existing tokenizer prefix collision: EAST precedes eastern without a boundary',
)
def test_extract_complete_eastern_timezone_name(timezone):
    # Exercise actual extraction, not a manually supplied helper capture.
    finder = datefinder.DateFinder()
    matches = list(finder.extract_date_strings('July 22, 2014 2 p.m. ' + timezone))
    captured_timezones = [
        captured
        for _, _, captures in matches
        for captured in captures.get('timezones', [])
    ]
    assert captured_timezones == [timezone]
