# import pytest

from mlna.sheets import call_sheets_api, get_when2meet, get_in_person

SAMPLE_BOOKING_ID = "1sgC_mWYv8YVISnJIfU5oyCFpDt-9yO63ztJT1VbWGqM"
SAMPLE_BOOKING_RANGE_NAME = "Form Responses 1!A2:V"
SAMPLE_WHEN2MEET_URL = "https://www.when2meet.com/?28493608-48Vb9&csv"
SAMPLE_ROSTER_ID = "1ajRbwIkCLR6Inw_X3TA-iXmoown2KyFJIbuicKM-vLk"
SAMPLE_ROSTER_RANGE_NAME = "Sheet1!A2:C"


def test_call_sheets_api():
    """Test the Google Sheets API call."""
    spreadsheet_id = SAMPLE_BOOKING_ID
    range_name = SAMPLE_BOOKING_RANGE_NAME
    df = call_sheets_api(spreadsheet_id, range_name)
    assert not df.empty


def test_get_when2meet():
    """Test fetching When2Meet data."""
    when2meet_url = "https://www.when2meet.com/?28493608-48Vb9&csv"
    w2m_df = get_when2meet(when2meet_url)
    assert not w2m_df.empty


def test_get_in_person():
    """Test filtering in-person bookings."""
    spreadsheet_id = "1sgC_mWYv8YVISnJIfU5oyCFpDt-9yO63ztJT1VbWGqM"
    range_name = "Form Responses 1!A2:V"
    in_person_bookings_df = get_in_person(spreadsheet_id, range_name)
    # when2meet_url = "https://www.when2meet.com/?28493608-48Vb9&csv"
    assert not in_person_bookings_df.empty
    assert all(in_person_bookings_df.iloc[:, 5] != "Virtual (Will be sent out on Valentine's Day)")


def test_get_parts():
    """Test the get_voice_parts function."""
    from mlna.parts import get_voice_parts

    booking_id = SAMPLE_BOOKING_ID
    booking_range = SAMPLE_BOOKING_RANGE_NAME
    roster_id = SAMPLE_ROSTER_ID
    roster_range = SAMPLE_ROSTER_RANGE_NAME
    when2meet_url = SAMPLE_WHEN2MEET_URL

    # Call the function
    get_voice_parts(booking_id, booking_range, roster_id, roster_range, when2meet_url)
