from .sheets import call_sheets_api, get_when2meet  # , get_in_person


def get_voice_parts(booking_id: str, booking_range: str, roster_id: str, roster_range: str, when2meet_url: str):
    # in_person_df = get_in_person(booking_id, booking_range)
    roster_df = call_sheets_api(roster_id, roster_range)
    roster_df = roster_df.rename(columns={0: "Name"})

    w2m_df = get_when2meet(when2meet_url)
    w2m_df = w2m_df.rename(columns={w2m_df.columns[0]: "Name"})

    roster_df["Name"] = roster_df["Name"].str.split().str[0].str.lower()
    w2m_df["Name"] = w2m_df["Name"].str.split().str[0].str.lower()

    print(w2m_df.head())
