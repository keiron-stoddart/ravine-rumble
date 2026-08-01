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

DAY_BLOCKS = ["Morning", "Afternoon", "Evening"]

# On weekdays only Evening is offered; Morning/Afternoon show as "Not Applicable".
WEEKDAY_BLOCKS = ["Evening"]
WEEKEND_BLOCKS = ["Morning", "Afternoon", "Evening"]
