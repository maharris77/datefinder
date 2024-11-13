import pytest
import datefinder
from datetime import datetime
import pytz
import sys
import logging
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
logger = logging.getLogger(__name__)

today = datetime.today()


@pytest.mark.parametrize('input_text, expected_date', [
    ((
        "Meeting Link: https://teams.microsoft.com/l/meetup-join"
        "/19%3ameeting_YjI2OWU4OTUtNWIwNS00OTU1LTk3YzQtZTg1ZTA2YTk1YzEx%40thread.v2/0?"
        "Conference Call (Group Meet) on Monday, 11th November, 2024 at 09:30 A.M. (IST) to discuss"),
        datetime(2024, 11, 11, 9, 30)
    ),
    ('June 2018', []),
    ('09/06/18',  datetime(2018, 9, 6)),
    ('09/06/2018', datetime(2018, 9, 6)),
    ('recorded: 03/14/2008', datetime(2008, 3, 14)),
    ('19th day of May, 2015', datetime(2015, 5, 19)),
    ('19th day of May', [])
    
])
def test_find_date_strings_strict(input_text, expected_date):
    if isinstance(expected_date,list):
        matches = list(datefinder.find_dates(input_text, strict=True))
        assert matches == expected_date

    else:
        return_date = None
        for return_date in datefinder.find_dates(input_text, strict=True):
            assert return_date == expected_date
        assert return_date is not None, 'Did not find date for test line: "{}"'.format(input_text) # handles dates 