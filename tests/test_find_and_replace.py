import pytest
import datefinder
import copy
import sys, logging

from datefinder.constants import REPLACEMENTS

logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

@pytest.mark.parametrize('date_string, expected_replaced_string, captures, expected_tz_string', [
    ('due on Tuesday Jul 22, 2014 eastern standard time',
    ' tuesday jul 22, 2014 eastern ',
     {'timezones':['EST']},
     'EST',
    )
])
def test_find_and_replace(date_string, expected_replaced_string, captures, expected_tz_string):
    dt = datefinder.DateFinder()
    expected_replacements = copy.copy(REPLACEMENTS)
    actual_date_string, actual_tz_string = dt._find_and_replace(date_string, captures)

    # assert that dt._find_and_replace did not mutate dt.REPLACEMENTS
    assert REPLACEMENTS == expected_replacements

    # assert the return values of dt._find_and_replace
    assert actual_date_string == expected_replaced_string
    assert actual_tz_string == expected_tz_string


@pytest.mark.parametrize('timezone, expected', [
    ('eastern', 'EST'),
    ('Eastern', 'EST'),
    ('EASTERN', 'EST'),
    ('pacific', 'PST'),
    ('Pacific', 'PST'),
    ('PACIFIC', 'PST'),
    ('mountain', 'MST'),
    ('Mountain', 'MST'),
    ('MOUNTAIN', 'MST'),
    ('central', 'CST'),
    ('Central', 'CST'),
    ('CENTRAL', 'CST'),
    ('EST', 'EST'),
    ('Unrecognized', 'Unrecognized'),
])
def test_pop_tz_string_case_insensitive_names(timezone, expected):
    assert datefinder.DateFinder()._pop_tz_string([timezone]) == expected


def test_pop_tz_string_empty():
    assert datefinder.DateFinder()._pop_tz_string([]) == ''


def test_find_and_replace_preserves_timezone_precedence():
    finder = datefinder.DateFinder()
    captures = {'timezones': ['eastern', 'PACIFIC']}
    _, actual_timezone = finder._find_and_replace(
        'July 22, 2014 eastern PACIFIC standard time', captures
    )
    # Preserve existing case-sensitive sorted selection before normalizing lookup.
    assert actual_timezone == 'EST'
    assert captures == {'timezones': ['eastern', 'PACIFIC']}
