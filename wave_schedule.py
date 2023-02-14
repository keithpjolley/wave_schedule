#!/usr/bin/env python3

"""
Create calendar invites for a series of events.
Maybe easier to use a csv or json file for data?
"""

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SCOPES = ["https://www.googleapis.com/auth/calendar"]
HOME_FIELD = "Snapdragon Stadium, 2101 Stadium Way, San Diego, CA 92108"


def games():
    """
    Return an object with all the game info.
    This really should be put into a different file.
    """
    return [
        {
            "team": "OL Reign",
            "month": 4,
            "day": 15,
            "hour": 19,
            "minute": 0,
            "home": False,
            "location": "Lumen Field, Seattle, Wa",
        },
        {
            "team": "Angel City",
            "month": 4,
            "day": 23,
            "hour": 17,
            "minute": 0,
            "home": False,
            "location": "BMO Stadium, Los Angeles, CA",
        },
        {
            "team": "Washington Spirit",
            "month": 5,
            "day": 6,
            "hour": 10,
            "minute": 0,
            "home": False,
            "location": "Audi Field, Washington, D.C",
        },
        {
            "team": "KC Current",
            "month": 5,
            "day": 14,
            "hour": 15,
            "minute": 0,
            "home": False,
            "location": "Children’s Mercy Park, Kansas City, KS",
        },
        {
            "team": "Houston Dash",
            "month": 5,
            "day": 20,
            "hour": 17,
            "minute": 30,
            "home": False,
            "location": "Shell Energy Stadium, Houston, TX",
        },
        {
            "team": "NY/NJ Gotham",
            "month": 6,
            "day": 4,
            "hour": 14,
            "minute": 30,
            "home": False,
            "location": "Red Bull Arena, Harrison, NJ",
        },
        {
            "team": "Racing Louisville",
            "month": 6,
            "day": 9,
            "hour": 17,
            "minute": 0,
            "home": False,
            "location": "Lynn Family Stadium, Louisville, KY",
        },
        {
            "team": "Angel City (UKG Challenge Cup)",
            "month": 6,
            "day": 28,
            "hour": 19,
            "minute": 0,
            "home": False,
            "location": "BMO Stadium, Los Angeles, CA",
        },
        {
            "team": "Chicago Red Stars",
            "month": 7,
            "day": 1,
            "hour": 17,
            "minute": 0,
            "home": False,
            "location": "Seatgeek Stadium, Bridgeview, IL",
        },
        {
            "team": "Portland Thorns (UKG Challenge Cup)",
            "month": 7,
            "day": 21,
            "hour": 19,
            "minute": 30,
            "home": False,
            "location": "Providence Park, Portland, OR",
        },
        {
            "team": "OL Reign (UKG Challenge Cup)",
            "month": 7,
            "day": 28,
            "hour": 19,
            "minute": 30,
            "home": False,
            "location": "Lumen Field, Seattle, Wa",
        },
        {
            "team": "Orlando Pride",
            "month": 8,
            "day": 25,
            "hour": 16,
            "minute": 0,
            "home": False,
            "location": "Exploria Stadium, Orlando, FL",
        },
        {
            "team": "Portland Thorns",
            "month": 9,
            "day": 30,
            "hour": 19,
            "minute": 30,
            "home": False,
            "location": "Providence Park, Portand, OR",
        },
        {
            "team": "NC Courage",
            "month": 10,
            "day": 7,
            "hour": 16,
            "minute": 0,
            "home": False,
            "location": "Sahlen’s Stadium, Cary, NC",
        },
        {
            "team": "Scrimmage (Team/Time TBA)",
            "month": 3,
            "day": 18,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "Chicago Red Stars",
            "month": 3,
            "day": 25,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "North Carolina Courage",
            "month": 4,
            "day": 1,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "Portland Thorns",
            "month": 4,
            "day": 19,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "Orlando Pride",
            "month": 4,
            "day": 29,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "Portland Thorns",
            "month": 5,
            "day": 26,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "OL Reign (UKG Challenge Cup)",
            "month": 5,
            "day": 31,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "Angel City",
            "month": 6,
            "day": 17,
            "hour": 13,
            "minute": 0,
            "home": True,
        },
        {
            "team": "OL Reign",
            "month": 6,
            "day": 24,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "Washington Spirit",
            "month": 7,
            "day": 8,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "Angel City (UKG Challenge Cup)",
            "month": 8,
            "day": 5,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "NY/NJ Gotham",
            "month": 8,
            "day": 19,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "Houston Dash",
            "month": 9,
            "day": 3,
            "hour": 17,
            "minute": 0,
            "home": True,
        },
        {
            "team": "Kansas City Current",
            "month": 9,
            "day": 16,
            "hour": 19,
            "minute": 0,
            "home": True,
        },
        {
            "team": "Racing Louisville",
            "month": 10,
            "day": 15,
            "hour": 14,
            "minute": 0,
            "home": True,
        },
    ]


def get_service():
    """
    Connect to the google api and return the connector object.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w", encoding="utf-8") as token:
            token.write(creds.to_json())
    try:
        service = build("calendar", "v3", credentials=creds)
    except HttpError as error:
        print(f"ERROR: An error occurred: {error}")
    return service


def create_game(service, game, attendees):
    """
    Do the things here.
    """
    color_id = 3

    if game.get("home"):
        location = HOME_FIELD
        summary = f'{game["team"]} @Wave'
        description = f'{game["team"]} versus SD Wave at Home'
    else:
        location = game.get("location", game.get("team"))
        summary = f'Wave @{game["team"]}'
        description = f'SD Wave versus {game["team"]} (Away)'
        if game.get("location"):
            description += f'@{game["location"]}'

    start_datetime = (
        f'2023-{int(game["month"]):02d}-'
        f'{int(game["day"]):02d}T{int(game["hour"]):02d}:'
        f'{int(game["minute"]):02d}:00'
    )
    end_datetime = (
        f'2023-{int(game["month"]):02d}-'
        f'{int(game["day"]):02d}T{int(2+game["hour"]):02d}:'
        f'{int(game["minute"]):02d}:00'
    )
    event = {
        "summary": summary,
        "location": location,
        "description": description,
        "start": {
            "dateTime": start_datetime,
            "timeZone": "America/Los_Angeles",
        },
        "end": {
            "dateTime": end_datetime,
            "timeZone": "America/Los_Angeles",
        },
        "recurrence": ["RRULE:FREQ=DAILY;COUNT=1;"],
        "attendees": attendees,
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 6 * 60},
            ],
        },
        "colorId": color_id,
    }
    print(f"creating: {game['team']} - {start_datetime}")
    try:
        event = (
            service.events().insert(calendarId="primary", body=event).execute()
        )
    except Exception as error:   # pylint: disable=broad-except
        print(f"ERROR: An error occurred here: {error}")


def main():
    """
    Assemble the pieces and do the things.
    """
    service = get_service()
    attendees = [
        {"email": "keithpjolley@gmail.com"},
        {"email": "danyawillms@gmail.com"},
        {"email": "jamulwillms@netscape.com"},
        {"email": "jamuldave@gmail.com"},
    ]
    for game in games():
        create_game(service, game, attendees)


if __name__ == "__main__":
    main()
