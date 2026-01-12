"""Pipeline and processing for Google Sheets Booking Data"""

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import pandas as pd
import requests
from io import StringIO

import re

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def call_sheets_api(spreadsheet_id: str, range_name: str) -> pd.DataFrame:
    """Authenticate and fetch data from Google Sheets."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_path = os.path.join(os.path.dirname(__file__), "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=57331)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get("values", [])
        return pd.DataFrame(values)
    except HttpError as err:
        print(err)
        return pd.DataFrame()


# def get_bookings(spreadsheet_id: str, range_name: str) -> pd.DataFrame:
#     """Authenticate and fetch data from Google Sheets."""
#     creds = None
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             creds_path = os.path.join(os.path.dirname(__file__), "credentials.json")
#             flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
#             creds = flow.run_local_server(port=57331)
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())
#     try:
#         service = build("sheets", "v4", credentials=creds)
#         sheet = service.spreadsheets()
#         result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
#         values = result.get("values", [])
#         return pd.DataFrame(values)
#     except HttpError as err:
#         print(err)
#         return pd.DataFrame()


def get_when2meet(when2meet_url: str) -> pd.DataFrame:
    """Fetch and process When2Meet data."""
    response = requests.get(when2meet_url)
    w2m_df = pd.read_csv(StringIO(response.text), header=0)
    w2m_df.columns = w2m_df.columns.str.slice(
        4,
    )
    w2m_df.columns = [w2m_df.columns[0], *pd.to_datetime(w2m_df.columns[1:])]
    return w2m_df


def get_in_person(booking_id: str, booking_range: str):
    bookings_df = call_sheets_api(booking_id, booking_range)
    """Clean and process in person booking data."""
    in_person_condition = bookings_df.iloc[:, 5] != "Virtual (Will be sent out on Valentine's Day)"
    bookings_in_person_df = bookings_df[in_person_condition]
    booked_subset = bookings_in_person_df.iloc[:, 10:16]
    booked_condition = booked_subset.apply(lambda s: s.str.len()) > 0
    booked_times_single_column = bookings_in_person_df.where(booked_condition).stack()
    booked_times_single_column.index = booked_times_single_column.index.get_level_values(0)
    pattern = r"^\S+\s+(\S+)"
    date_after_comma = bookings_in_person_df.loc[:, 5].str.extract(pattern, expand=False)
    bookings_in_person_df["booked_times_date_time"] = date_after_comma + " " + booked_times_single_column + " 2025"

    def clean_datetime(date_time_str):
        if pd.isna(date_time_str):
            return None
        date_pattern = r"(\d{1,2}/\d{1,2})\s+(.*?)\s+(\d{4})"
        date_match = re.search(date_pattern, date_time_str)
        if not date_match:
            return None
        date, time_range, year = date_match.groups()
        special_cases = {
            r"11:\d{2}\s*-\s*12(?:\s*:|:)?\d{2}\s*PM": "AM",
            r"12:\d{2}\s*-\s*1(?:\s*:|:)?\d{2}\s*PM": "PM",
        }
        for pattern, correct_meridiem in special_cases.items():
            if re.search(pattern, time_range, re.IGNORECASE):
                time_match = re.search(r"(\d{1,2}:\d{2})", time_range)
                if time_match:
                    time = time_match.group(1)
                    return f"{date}/{year} {time} {correct_meridiem}"
        time_match = re.search(r"(\d{1,2}:\d{2})(?=\s*-|\s*[AP]M)", time_range)
        ampm_match = re.search(r"([AP]M)", time_range)
        if not time_match or not ampm_match:
            return None
        time = time_match.group(1)
        am_pm = ampm_match.group(1)
        return f"{date}/{year} {time} {am_pm}"

    bookings_in_person_df["booked_times_date_time"] = bookings_in_person_df["booked_times_date_time"].apply(
        clean_datetime
    )
    bookings_in_person_df["booked_times_date_time"] = pd.to_datetime(bookings_in_person_df["booked_times_date_time"])
    return bookings_in_person_df


def get_roster(spreadsheet_id: str, range_name: str) -> pd.DataFrame:
    """Fetch and process roster data from Google Sheets."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds_path = os.path.join(os.path.dirname(__file__), "credentials.json")
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=57331)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get("values", [])
        return pd.DataFrame(values)
    except HttpError as err:
        print(err)
        return pd.DataFrame()


# def main():
#     """Shows basic usage of the Sheets API.
#     Prints values from a sample spreadsheet.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
#             creds = flow.run_local_server(port=57331)
#         # Save the credentials for the next run
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         service = build("sheets", "v4", credentials=creds)

#         # Call the Sheets API
#         sheet = service.spreadsheets()
#         result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
#         values = result.get("values", [])

#         if not values:
#             print("No data found.")
#             return

#         # print("Name, Major:")
#         # for row in values:
#         # Print all columns for all rows
#         # print(f"{row}")
#     except HttpError as err:
#         print(err)

#     # Converting bookings data to DataFrame
#     bookings_df = pd.DataFrame(values)

#     # Cleaning: removing blank columns, payment information
#     # bookings_df = bookings_df.iloc[:, list(range(3, 8) + list(range(2, 5)) + 17)]

#     # Getting When2meet Data and reading it into Pandas DataFrame
#     response = requests.get("https://www.when2meet.com/?28493608-48Vb9&csv")
#     w2m_df = pd.read_csv(StringIO(response.text), header=0)

#     # converting into standard Date/Time
#     w2m_df.columns = w2m_df.columns.str.slice(
#         4,
#     )  # removes day of the week

#     w2m_df.columns = [w2m_df.columns[0], *pd.to_datetime(w2m_df.columns[1:])]  # converts columns to date/time
#     # w2m_df.to_csv("w2m.csv")

#     in_person_condition = (
#         bookings_df.iloc[:, 5] != "Virtual (Will be sent out on Valentine's Day)"
#     )  # removing virtual bookings
#     bookings_in_person_df = bookings_df[in_person_condition]

#     # finding which column the actual booked time slot falls under
#     booked_subset = bookings_in_person_df.iloc[:, 10:16]
#     booked_condition = booked_subset.apply(lambda s: s.str.len()) > 0

#     # Putting the booked time slots into a single column
#     booked_times_single_column = bookings_in_person_df.where(booked_condition).stack()
#     booked_times_single_column.index = booked_times_single_column.index.get_level_values(
#         0
#     )  # re indexing since stack() creates a series with multiIndexing

#     # converting into a format that can be converted to date/time (can be removed by fixing the form)
#     # 1. get rid of empty columns
#     # 2. date column should be like "2/14/2025"
#     # 3. monday/tuesday/etc should be like "4:00 PM - 4:30 PM"
#     # 4. or "4:00 PM" (no time slot)

#     # removing the day of the week part of the date
#     pattern = r"^\S+\s+(\S+)"
#     date_after_comma = bookings_in_person_df.loc[:, 5].str.extract(pattern, expand=False)

#     bookings_in_person_df["booked_times_date_time"] = date_after_comma + " " + booked_times_single_column + " 2025"

#     # bookings_in_person_df["booked_times_date_time"].to_csv("booked_times_date_time.csv")

#     # modify the date/time formatting:

#     def clean_datetime(date_time_str):
#         if pd.isna(date_time_str):
#             return None

#         # Extract date parts first
#         date_pattern = r"(\d{1,2}/\d{1,2})\s+(.*?)\s+(\d{4})"
#         date_match = re.search(date_pattern, date_time_str)
#         if not date_match:
#             return None

#         date, time_range, year = date_match.groups()

#         # Handle special cases for time ranges crossing AM/PM boundary
#         special_cases = {
#             r"11:\d{2}\s*-\s*12(?:\s*:|:)?\d{2}\s*PM": "AM",  # 11:30-12 PM → 11:30 AM
#             r"12:\d{2}\s*-\s*1(?:\s*:|:)?\d{2}\s*PM": "PM",  # 12:30-1 PM → 12:30 PM
#         }

#         # Check if time_range matches any special case
#         for pattern, correct_meridiem in special_cases.items():
#             if re.search(pattern, time_range, re.IGNORECASE):
#                 # Extract the first time
#                 time_match = re.search(r"(\d{1,2}:\d{2})", time_range)
#                 if time_match:
#                     time = time_match.group(1)
#                     return f"{date}/{year} {time} {correct_meridiem}"

#         # Regular case processing
#         time_match = re.search(r"(\d{1,2}:\d{2})(?=\s*-|\s*[AP]M)", time_range)
#         ampm_match = re.search(r"([AP]M)", time_range)

#         if not time_match or not ampm_match:
#             return None

#         time = time_match.group(1)
#         am_pm = ampm_match.group(1)

#         # Combine into standard format
#         return f"{date}/{year} {time} {am_pm}"

#     # Apply the cleaning to the datetime column
#     bookings_in_person_df["booked_times_date_time"] = bookings_in_person_df["booked_times_date_time"].apply(
#         clean_datetime
#     )

#     # Now convert to datetime
#     bookings_in_person_df["booked_times_date_time"] = pd.to_datetime(bookings_in_person_df["booked_times_date_time"])

#     print(bookings_in_person_df["booked_times_date_time"])

#     # Getting people's availability of booked time slots
#     def match_bookings_with_availability(booked_times, w2m_df):
#         """
#         Creates a data structure matching booked times with available people.

#         Args:
#             booked_times: Series of datetime objects from bookings
#             w2m_df: DataFrame from When2Meet with people's availability

#         Returns:
#             List of dictionaries containing:
#             - datetime: The booked datetime
#             - available_people: List of people available at that time
#         """
#         availability_matches = []

#         for booked_time in booked_times:
#             if pd.isna(booked_time):
#                 continue

#             # Find the matching column in w2m_df
#             matching_col = w2m_df.columns[1:][w2m_df.columns[1:] == booked_time]

#             if matching_col is not None:
#                 # Get names of people who are available (where value is 1)
#                 available_people = w2m_df[w2m_df[matching_col] == 1].iloc[:, 0].tolist()

#                 availability_matches.append({"datetime": booked_time, "available_people": available_people})
#             else:
#                 # Handle case where no matching time found
#                 availability_matches.append({"datetime": booked_time, "available_people": []})

#         return availability_matches

#     # availability_matches = match_bookings_with_availability(bookings_in_person_df["booked_times_date_time"], w2m_df)

#     # Print the results
#     # for match in availability_matches:
#     #     print(f"\nTime: {match['datetime']}")
#     #     print(f"Available people: {', '.join(match['available_people'])}")


# if __name__ == "__main__":
#     main()
