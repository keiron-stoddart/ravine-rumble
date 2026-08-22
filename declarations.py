from datetime import date
from enum import Enum


class Team(Enum):
    PAT = 5
    ZACH = 12
    DAN = 9
    KEIRON = 1
    JOHN = 2
    BRIAN = 10
    NAN = 7
    TIM = 3
    TYLER = 8
    PAUL = 4
    BRETT = 11
    WONJOON = 6


RAVINE_RUMBLE = "546047"
GAME_CODE = "nfl"

# NFL - 2023, lifted this from example documentation, not positive what this is used for
GAME_ID = 449


class Event(Enum):
    PRESEASON_MEETING = "preseason_meeting"
    DRAFT = "draft"


EVENT_LABELS = {
    Event.PRESEASON_MEETING: "Pre-Season Meeting",
    Event.DRAFT: "Draft",
}

EVENT_DURATION_MINUTES = {
    Event.PRESEASON_MEETING: 60,
    Event.DRAFT: 120,
}

# 2026 season availability poll window: next Wednesday through the day before
# NFL Week 1 (Wed Sep 9, 2026). Update these two dates next year.
POLL_START_DATE = date(2026, 8, 5)
POLL_END_DATE = date(2026, 9, 8)

# The 2026 poll is closed — times are locked in and posted on the /2026 page.
# Flip back to False if a future season needs the poll open again.
AVAILABILITY_ARCHIVED = True

SEASON_2026_EVENTS = [
    {
        "label": "Pre-Season Meeting",
        "date": "Thursday, August 27",
        "time": "7:00 – 8:00pm ET",
        "calendar_url": "https://calendar.google.com/calendar/event?action=TEMPLATE&tmeid=NWg0ZTQ2M3E0M2txcDVuaXQybmtyMm5rYm4ga2Vpcm9uLnN0b2RkYXJ0QG0&tmsrc=keiron.stoddart%40gmail.com",
    },
    {
        "label": "Draft",
        "date": "Thursday, September 3",
        "time": "7:00 – 9:00pm ET",
        "calendar_url": "https://calendar.google.com/calendar/event?action=TEMPLATE&tmeid=MTlyYXNsZTcwbmJtNmY0dWwwZDNtcjN0ZWMga2Vpcm9uLnN0b2RkYXJ0QG0&tmsrc=keiron.stoddart%40gmail.com",
    },
]

# League Finishes by Member, 2012-2025. Ordered by # of 1st place finishes.
# "*" on a finish count means it includes a Championship from 2009-2011.
LEAGUE_FINISHES = [
    {"manager": "Nan", "first": "4*", "second": "1", "third": "3", "top_3": 8, "championships": ""},
    {"manager": "Pat", "first": "3", "second": "", "third": "", "top_3": 3, "championships": ""},
    {"manager": "Keiron", "first": "2", "second": "3", "third": "1", "top_3": 6, "championships": ""},
    {"manager": "Brian", "first": "2*", "second": "1", "third": "", "top_3": 3, "championships": ""},
    {"manager": "Paul", "first": "1", "second": "2", "third": "1", "top_3": 4, "championships": ""},
    {"manager": "Dan", "first": "1", "second": "2", "third": "3", "top_3": 6, "championships": ""},
    {"manager": "Tim", "first": "1", "second": "1", "third": "1", "top_3": 3, "championships": "1"},
    {"manager": "Zach", "first": "1", "second": "1", "third": "1", "top_3": 3, "championships": ""},
    {"manager": "Brett", "first": "1", "second": "", "third": "1", "top_3": 2, "championships": "1"},
    {"manager": "Tyler", "first": "1*", "second": "", "third": "3", "top_3": 4, "championships": "2"},
    {"manager": "John", "first": "", "second": "3", "third": "", "top_3": 3, "championships": ""},
    {"manager": "Wonjoon", "first": "", "second": "", "third": "", "top_3": 0, "championships": ""},
]

# Historical Comparison, 2012-2025. Ordered by average league finish.
HISTORICAL_COMPARISON = [
    {"manager": "Nan", "seasons": 14, "finish": 3.7, "wins": 8.4, "waiver_adds": 28, "points_for": 110, "points_against": 99},
    {"manager": "Dan", "seasons": 14, "finish": 4.7, "wins": 7.8, "waiver_adds": 20, "points_for": 105, "points_against": 99},
    {"manager": "John", "seasons": 14, "finish": 5.2, "wins": 7.4, "waiver_adds": 29, "points_for": 104, "points_against": 99},
    {"manager": "Keiron", "seasons": 14, "finish": 5.6, "wins": 6.5, "waiver_adds": 26, "points_for": 103, "points_against": 102},
    {"manager": "Zach", "seasons": 14, "finish": 6.1, "wins": 7.1, "waiver_adds": 23, "points_for": 103, "points_against": 103},
    {"manager": "Pat", "seasons": 11, "finish": 6.1, "wins": 7.3, "waiver_adds": 26, "points_for": 108, "points_against": 105},
    {"manager": "Tim", "seasons": 14, "finish": 6.4, "wins": 6.1, "waiver_adds": 17, "points_for": 100, "points_against": 102},
    {"manager": "Brian", "seasons": 14, "finish": 6.8, "wins": 6.4, "waiver_adds": 23, "points_for": 101, "points_against": 104},
    {"manager": "Brett", "seasons": 14, "finish": 6.9, "wins": 6.1, "waiver_adds": 14, "points_for": 99, "points_against": 103},
    {"manager": "Paul", "seasons": 11, "finish": 7.1, "wins": 6.5, "waiver_adds": 11, "points_for": 102, "points_against": 104},
    {"manager": "Tyler", "seasons": 14, "finish": 7.6, "wins": 6.1, "waiver_adds": 21, "points_for": 97, "points_against": 101},
    {"manager": "Wonjoon", "seasons": 14, "finish": 9.8, "wins": 4.4, "waiver_adds": 14, "points_for": 93, "points_against": 104},
]

DAY_BLOCKS = ["Morning", "Afternoon", "Evening"]

# On weekdays only Evening is offered; Morning/Afternoon show as "Not Applicable".
WEEKDAY_BLOCKS = ["Evening"]
WEEKEND_BLOCKS = ["Morning", "Afternoon", "Evening"]
