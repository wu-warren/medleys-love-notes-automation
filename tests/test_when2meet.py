# import pytest

import mlna.sheets as sheets
import mlna.parts as parts
import pandas as pd
import pytest

SAMPLE_BOOKING_ID = "1sgC_mWYv8YVISnJIfU5oyCFpDt-9yO63ztJT1VbWGqM"
SAMPLE_BOOKING_RANGE_NAME = "Form Responses 1!A2:V"
SAMPLE_WHEN2MEET_URL = "https://www.when2meet.com/?28493608-48Vb9&csv"
SAMPLE_ROSTER_ID = "1ajRbwIkCLR6Inw_X3TA-iXmoown2KyFJIbuicKM-vLk"
SAMPLE_ROSTER_RANGE_NAME = "Sheet1!A2:C"


@pytest.mark.skip(reason="Skipping API call test to avoid dependency on external service.")
def test_call_sheets_api():
    """Test the Google Sheets API call."""
    spreadsheet_id = SAMPLE_BOOKING_ID
    range_name = SAMPLE_BOOKING_RANGE_NAME
    df = sheets.call_sheets_api(spreadsheet_id, range_name)
    assert not df.empty


@pytest.mark.skip(reason="Skipping When2Meet API call test to avoid dependency on external service.")
def test_get_when2meet():
    """Test fetching When2Meet data."""
    when2meet_url = SAMPLE_WHEN2MEET_URL
    w2m_df = sheets.get_when2meet(when2meet_url)
    assert not w2m_df.empty


def test_get_in_person(monkeypatch):
    """Test filtering in-person bookings."""
    fake_df = pd.DataFrame(
        [
            ["a", "b", "c", "d", "e", "Virtual (Will be sent out on Valentine's Day)", "x"],
            ["a", "b", "c", "d", "e", "In Person", "x"],
            ["a", "b", "c", "d", "e", "In Person", "x"],
        ]
    )

    def fake_call_sheets_api(spreadsheet_id, range_name):
        return fake_df

    monkeypatch.setattr(sheets, "call_sheets_api", fake_call_sheets_api)

    spreadsheet_id = SAMPLE_BOOKING_ID
    range_name = SAMPLE_BOOKING_RANGE_NAME

    in_person_bookings_df = sheets.get_in_person(spreadsheet_id, range_name)
    assert not in_person_bookings_df.empty
    assert all(in_person_bookings_df.iloc[:, 5] != "Virtual (Will be sent out on Valentine's Day)")


def test_get_parts(monkeypatch):
    """Test the get_voice_parts function."""
    fake_df_booking = pd.DataFrame(
        [
            [
                "2/1/2025 1:16:46",
                "",
                "",
                "L",
                "B",
                "Monday, 2/10",
                "A",
                "Never Gonna Give You Up - Rick Astley",
                "Might change)",
                "Social Media Posts",
                "",
                "4:00 - 4:30 PM",
                "",
                "",
                "",
                "",
                "num1",
                "Yes!",
                "",
                "",
                "email1",
            ],
            [
                "2/1/2025 11:39:34",
                "",
                "",
                "A",
                "M",
                "Friday, 2/14 (Valentine's Day)",
                "4",
                "Just The Way You Are - Bruno Mars",
                "L",
                "Friend/Referral",
                "",
                "",
                "",
                "",
                "",
                "3:30 - 4:00 PM",
                "N/A",
                "num2",
                "Yes!",
                "",
                "$10 TIP",
                "email2",
            ],
            [
                "2/3/2025 14:32:54",
                "",
                "",
                "O",
                "W",
                "Virtual (Will be sent out on Valentine's Day)",
                "virtual",
                "Never Gonna Give You Up - Rick Astley",
                "",
                "Friend/Referral",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "email3",
                "num3",
                "Yes!",
                "",
                "",
                "email3",
            ],
            [
                "2/4/2025 10:46:08",
                "",
                "",
                "K",
                "G",
                "Virtual (Will be sent out on Valentine's Day)",
                "Virtual",
                "Anything / Surprise them !!",
                "",
                "Friend/Referral",
                "",
                "",
                "",
                "",
                "",
                "",
                "",
                "email4",
                "num4",
                "Yes!",
                "",
                "",
                "email4",
            ],
        ]
    )

    fake_df_w2m = pd.DataFrame(
        [
            ["", "Mon Feb 10 16:00:00 2025", "Fri Feb 14 15:30:00 2025"],
            ["A", "Yes", "Yes"],
            ["B", "Yes", "No"],
            ["C", "No", "Yes"],
            ["D", "No", "No"],
        ]
    )

    fake_roster = pd.DataFrame(
        [
            ["A", "", "Soprano"],
            ["B", "", "Alto"],
            ["C", "", "Tenor"],
            ["D", "", "Bass"],
        ]
    )
    booking_id = SAMPLE_BOOKING_ID
    booking_range = SAMPLE_BOOKING_RANGE_NAME
    roster_id = SAMPLE_ROSTER_ID
    roster_range = SAMPLE_ROSTER_RANGE_NAME
    when2meet_url = SAMPLE_WHEN2MEET_URL

    def fake_call_sheets_api(spreadsheet_id, range_name):
        if spreadsheet_id == booking_id and range_name == booking_range:
            return fake_df_booking
        elif spreadsheet_id == roster_id and range_name == roster_range:
            return fake_roster

    def fake_get_when2meet(url):
        return fake_df_w2m

    monkeypatch.setattr(sheets, "call_sheets_api", fake_call_sheets_api)
    monkeypatch.setattr(sheets, "get_when2meet", fake_get_when2meet)

    monkeypatch.setattr(parts, "call_sheets_api", fake_call_sheets_api)
    monkeypatch.setattr(parts, "get_when2meet", fake_get_when2meet)
    # Call the function
    parts.get_voice_parts(booking_id, booking_range, roster_id, roster_range, when2meet_url)
