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

# Full season-by-season results, 2012-2025, one row per manager per year.
# Sourced from the league's season data export; sorted by year desc, then finish.
SEASON_RESULTS = [
    {"year": 2025, "manager": 'Brett', "team": 'wonsuperbowl', "finish": 1, "wins": 9, "losses": 5, "points_for": 1825.2, "points_against": 1762.5, "point_diff": 62.7, "streak": 'W-1', "waiver_budget": 10, "waiver_rank": 11, "moves": 15},
    {"year": 2025, "manager": 'Paul', "team": 'Daddy Dart', "finish": 2, "wins": 8, "losses": 6, "points_for": 1706.8, "points_against": 1658.9, "point_diff": 47.9, "streak": 'W-2', "waiver_budget": 70, "waiver_rank": 8, "moves": 17},
    {"year": 2025, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 3, "wins": 10, "losses": 4, "points_for": 1749.3, "points_against": 1478.8, "point_diff": 270.5, "streak": 'W-1', "waiver_budget": 62, "waiver_rank": 12, "moves": 14},
    {"year": 2025, "manager": 'Nan', "team": 'Green Bay Parsons', "finish": 4, "wins": 9, "losses": 5, "points_for": 1790.2, "points_against": 1495.6, "point_diff": 294.6, "streak": 'L-1', "waiver_budget": 20, "waiver_rank": 10, "moves": 37},
    {"year": 2025, "manager": 'Zach', "team": 'Cook’in with Gas', "finish": 5, "wins": 8, "losses": 6, "points_for": 1832.7, "points_against": 1707.9, "point_diff": 124.8, "streak": 'L-1', "waiver_budget": 3, "waiver_rank": 9, "moves": 29},
    {"year": 2025, "manager": 'John', "team": 'Big Green Machine', "finish": 6, "wins": 8, "losses": 6, "points_for": 1658.3, "points_against": 1571.0, "point_diff": 87.3, "streak": 'L-1', "waiver_budget": 22, "waiver_rank": 7, "moves": 57},
    {"year": 2025, "manager": 'Tyler', "team": 'BirdsArentReal', "finish": 7, "wins": 6, "losses": 8, "points_for": 1610.8, "points_against": 1657.6, "point_diff": -46.8, "streak": 'W-1', "waiver_budget": 67, "waiver_rank": 4, "moves": 21},
    {"year": 2025, "manager": 'Pat', "team": 'Ebron James', "finish": 8, "wins": 8, "losses": 6, "points_for": 1608.3, "points_against": 1614.9, "point_diff": -6.6, "streak": 'W-4', "waiver_budget": 1, "waiver_rank": 6, "moves": 32},
    {"year": 2025, "manager": 'Tim', "team": 'Booty Meat', "finish": 9, "wins": 6, "losses": 8, "points_for": 1575.4, "points_against": 1662, "point_diff": -86.6, "streak": 'L-2', "waiver_budget": 25, "waiver_rank": 3, "moves": 14},
    {"year": 2025, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 10, "wins": 7, "losses": 7, "points_for": 1623.6, "points_against": 1581.9, "point_diff": 41.7, "streak": 'W-2', "waiver_budget": 50, "waiver_rank": 5, "moves": 17},
    {"year": 2025, "manager": 'Brian', "team": 'The Covfefe Crew', "finish": 11, "wins": 5, "losses": 9, "points_for": 1444.5, "points_against": 1648.1, "point_diff": -203.5, "streak": 'L-7', "waiver_budget": 55, "waiver_rank": 2, "moves": 17},
    {"year": 2025, "manager": 'Wonjoon', "team": 'Nova Jersey Clube de Futebol', "finish": 12, "wins": 0, "losses": 14, "points_for": 1135.4, "points_against": 1721.2, "point_diff": -585.8, "streak": 'L-14', "waiver_budget": 94, "waiver_rank": 1, "moves": 24},
    {"year": 2024, "manager": 'Nan', "team": 'Like a good Naber', "finish": 1, "wins": 8, "losses": 6, "points_for": 1878.6, "points_against": 1797.8, "point_diff": 80.8, "streak": 'L-3', "waiver_budget": 1, "waiver_rank": 8, "moves": 30},
    {"year": 2024, "manager": 'John', "team": 'Big Green Machine', "finish": 2, "wins": 9, "losses": 5, "points_for": 1761.3, "points_against": 1621.7, "point_diff": 139.6, "streak": 'W-5', "waiver_budget": 0, "waiver_rank": 10, "moves": 56},
    {"year": 2024, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 3, "wins": 12, "losses": 2, "points_for": 1773.2, "points_against": 1344.4, "point_diff": 428.8, "streak": 'W-4', "waiver_budget": 16, "waiver_rank": 12, "moves": 12},
    {"year": 2024, "manager": 'Zach', "team": "Allen's Army", "finish": 4, "wins": 9, "losses": 5, "points_for": 1782.1, "points_against": 1722.1, "point_diff": 60.0, "streak": 'W-5', "waiver_budget": 1, "waiver_rank": 11, "moves": 15},
    {"year": 2024, "manager": 'Pat', "team": 'Ebron James', "finish": 5, "wins": 8, "losses": 6, "points_for": 1760.9, "points_against": 1688.1, "point_diff": 72.9, "streak": 'W-2', "waiver_budget": 22, "waiver_rank": 7, "moves": 37},
    {"year": 2024, "manager": 'Brian', "team": 'The Covfefe Crew', "finish": 6, "wins": 9, "losses": 5, "points_for": 1702.5, "points_against": 1497.6, "point_diff": 204.9, "streak": 'W-1', "waiver_budget": 60, "waiver_rank": 9, "moves": 23},
    {"year": 2024, "manager": 'Tim', "team": 'Booty Meat', "finish": 7, "wins": 6, "losses": 8, "points_for": 1663.9, "points_against": 1817.5, "point_diff": -153.5, "streak": 'L-1', "waiver_budget": 14, "waiver_rank": 6, "moves": 17},
    {"year": 2024, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 8, "wins": 2, "losses": 12, "points_for": 1446.0, "points_against": 1646.2, "point_diff": -200.3, "streak": 'L-5', "waiver_budget": 57, "waiver_rank": 1, "moves": 24},
    {"year": 2024, "manager": 'Wonjoon', "team": 'Mr Rodgers NeighborHOOD', "finish": 9, "wins": 5, "losses": 9, "points_for": 1497.5, "points_against": 1683.8, "point_diff": -186.3, "streak": 'L-1', "waiver_budget": 100, "waiver_rank": 3, "moves": 0},
    {"year": 2024, "manager": 'Paul', "team": '🤌🤌🤌', "finish": 10, "wins": 6, "losses": 8, "points_for": 1583.0, "points_against": 1725.5, "point_diff": -142.4, "streak": 'L-2', "waiver_budget": 15, "waiver_rank": 5, "moves": 21},
    {"year": 2024, "manager": 'Brett', "team": 'socialismiskewl', "finish": 11, "wins": 6, "losses": 8, "points_for": 1516.3, "points_against": 1638.7, "point_diff": -122.4, "streak": 'W-1', "waiver_budget": 14, "waiver_rank": 4, "moves": 21},
    {"year": 2024, "manager": 'Tyler', "team": '#KeironIsOverParty', "finish": 12, "wins": 4, "losses": 10, "points_for": 1424.1, "points_against": 1606.1, "point_diff": -182.0, "streak": 'L-2', "waiver_budget": 0, "waiver_rank": 2, "moves": 20},
    {"year": 2023, "manager": 'Pat', "team": 'Ebron James', "finish": 1, "wins": 10, "losses": 4, "points_for": 1891.8, "points_against": 1788.3, "point_diff": 103.5, "streak": 'L-1', "waiver_budget": 0, "waiver_rank": 12, "moves": 29},
    {"year": 2023, "manager": 'Brian', "team": 'The Covfefe Crew', "finish": 2, "wins": 9, "losses": 5, "points_for": 1600.9, "points_against": 1551.4, "point_diff": 49.6, "streak": 'W-2', "waiver_budget": 48, "waiver_rank": 7, "moves": 19},
    {"year": 2023, "manager": 'Zach', "team": "Allen's Army", "finish": 3, "wins": 9, "losses": 5, "points_for": 1832.6, "points_against": 1636.0, "point_diff": 196.6, "streak": 'L-1', "waiver_budget": 1, "waiver_rank": 11, "moves": 24},
    {"year": 2023, "manager": 'John', "team": 'Big Green Machine', "finish": 4, "wins": 9, "losses": 5, "points_for": 1637.1, "points_against": 1624.1, "point_diff": 12.9, "streak": 'L-2', "waiver_budget": 8, "waiver_rank": 8, "moves": 45},
    {"year": 2023, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 5, "wins": 9, "losses": 5, "points_for": 1640.7, "points_against": 1602.5, "point_diff": 38.2, "streak": 'L-2', "waiver_budget": 13, "waiver_rank": 9, "moves": 19},
    {"year": 2023, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 6, "wins": 9, "losses": 5, "points_for": 1694.0, "points_against": 1541.9, "point_diff": 152.1, "streak": 'W-2', "waiver_budget": 67, "waiver_rank": 10, "moves": 16},
    {"year": 2023, "manager": 'Tim', "team": 'Booty Meat', "finish": 7, "wins": 7, "losses": 7, "points_for": 1605.3, "points_against": 1420.3, "point_diff": 185.0, "streak": 'W-2', "waiver_budget": 80, "waiver_rank": 5, "moves": 13},
    {"year": 2023, "manager": 'Nan', "team": 'AA(ron) the JET(s) Plane', "finish": 8, "wins": 8, "losses": 6, "points_for": 1772.1, "points_against": 1565.3, "point_diff": 206.8, "streak": 'W-2', "waiver_budget": 28, "waiver_rank": 6, "moves": 26},
    {"year": 2023, "manager": 'Brett', "team": '~☆~PhilliesPhan42069~☆~ (^~^)', "finish": 9, "wins": 4, "losses": 10, "points_for": 1556.3, "points_against": 1818.0, "point_diff": -261.7, "streak": 'L-5', "waiver_budget": 20, "waiver_rank": 2, "moves": 13},
    {"year": 2023, "manager": 'Tyler', "team": '#KeironIsOverParty', "finish": 10, "wins": 5, "losses": 9, "points_for": 1501.1, "points_against": 1609.1, "point_diff": -108.0, "streak": 'W-1', "waiver_budget": 0, "waiver_rank": 4, "moves": 32},
    {"year": 2023, "manager": 'Wonjoon', "team": 'Fantasy Futbol', "finish": 11, "wins": 1, "losses": 13, "points_for": 1337.2, "points_against": 1805.8, "point_diff": -468.6, "streak": 'L-6', "waiver_budget": 70, "waiver_rank": 1, "moves": 12},
    {"year": 2023, "manager": 'Paul', "team": "Brady's Ugly", "finish": 12, "wins": 4, "losses": 10, "points_for": 1669.4, "points_against": 1775.7, "point_diff": -106.3, "streak": 'W-1', "waiver_budget": 95, "waiver_rank": 3, "moves": 18},
    {"year": 2022, "manager": 'Nan', "team": 'Ayahuasca Journey', "finish": 1, "wins": 8, "losses": 6, "points_for": 1723.6, "points_against": 1648.3, "point_diff": 75.3, "streak": 'W-1', "waiver_budget": 0, "waiver_rank": 8, "moves": 37},
    {"year": 2022, "manager": 'Zach', "team": "Allen's Army", "finish": 2, "wins": 9, "losses": 5, "points_for": 1686.4, "points_against": 1691.8, "point_diff": -5.4, "streak": 'W-1', "waiver_budget": 0, "waiver_rank": 10, "moves": 34},
    {"year": 2022, "manager": 'Tim', "team": 'Booty Meat', "finish": 3, "wins": 11, "losses": 3, "points_for": 1755.3, "points_against": 1466.2, "point_diff": 289.1, "streak": 'W-5', "waiver_budget": 3, "waiver_rank": 12, "moves": 26},
    {"year": 2022, "manager": 'John', "team": 'Big Green Machine', "finish": 4, "wins": 9, "losses": 5, "points_for": 1721.6, "points_against": 1508.9, "point_diff": 212.7, "streak": 'L-1', "waiver_budget": 4, "waiver_rank": 11, "moves": 27},
    {"year": 2022, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 5, "wins": 9, "losses": 5, "points_for": 1554.0, "points_against": 1609.9, "point_diff": -55.8, "streak": 'L-1', "waiver_budget": 0, "waiver_rank": 9, "moves": 29},
    {"year": 2022, "manager": 'Brian', "team": 'The Covfefe Crew', "finish": 6, "wins": 7, "losses": 7, "points_for": 1632, "points_against": 1568.4, "point_diff": 63.6, "streak": 'W-1', "waiver_budget": 24, "waiver_rank": 7, "moves": 23},
    {"year": 2022, "manager": 'Tyler', "team": '#KeironIsOverParty', "finish": 7, "wins": 7, "losses": 7, "points_for": 1622.1, "points_against": 1563.9, "point_diff": 58.2, "streak": 'L-1', "waiver_budget": 0, "waiver_rank": 6, "moves": 27},
    {"year": 2022, "manager": 'Brett', "team": '~☆~PhilliesPhan42069~☆~ (^~^)', "finish": 8, "wins": 3, "losses": 11, "points_for": 1486.7, "points_against": 1765.7, "point_diff": -279.0, "streak": 'L-2', "waiver_budget": 0, "waiver_rank": 1, "moves": 11},
    {"year": 2022, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 9, "wins": 4, "losses": 10, "points_for": 1411.6, "points_against": 1529.5, "point_diff": -117.8, "streak": 'W-1', "waiver_budget": 4, "waiver_rank": 2, "moves": 25},
    {"year": 2022, "manager": 'Pat', "team": 'Ebron James', "finish": 10, "wins": 6, "losses": 8, "points_for": 1587.9, "points_against": 1577.2, "point_diff": 10.7, "streak": 'W-1', "waiver_budget": 17, "waiver_rank": 4, "moves": 24},
    {"year": 2022, "manager": 'Paul', "team": "Brady's Ugly", "finish": 11, "wins": 4, "losses": 10, "points_for": 1483.3, "points_against": 1739.8, "point_diff": -256.6, "streak": 'L-1', "waiver_budget": 50, "waiver_rank": 3, "moves": 13},
    {"year": 2022, "manager": 'Wonjoon', "team": 'Fantasy Futbol', "finish": 12, "wins": 7, "losses": 7, "points_for": 1608.2, "points_against": 1603.3, "point_diff": 4.9, "streak": 'L-1', "waiver_budget": 13, "waiver_rank": 5, "moves": 16},
    {"year": 2021, "manager": 'Paul', "team": "Brady's Ugly", "finish": 1, "wins": 10, "losses": 4, "points_for": 1766.1, "points_against": 1587.9, "point_diff": 178.2, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 8, "moves": 11},
    {"year": 2021, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 2, "wins": 8, "losses": 6, "points_for": 1759.8, "points_against": 1635.2, "point_diff": 124.6, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 10, "moves": 43},
    {"year": 2021, "manager": 'Nan', "team": 'Fire Gutekunst', "finish": 3, "wins": 13, "losses": 1, "points_for": 1945.1, "points_against": 1425.3, "point_diff": 519.8, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 6, "moves": 25},
    {"year": 2021, "manager": 'Brian', "team": 'The Covfefe Crew', "finish": 4, "wins": 6, "losses": 8, "points_for": 1693.4, "points_against": 1864.0, "point_diff": -170.5, "streak": 'L-4', "waiver_budget": None, "waiver_rank": 5, "moves": 23},
    {"year": 2021, "manager": 'John', "team": 'Big Green Machine', "finish": 5, "wins": 9, "losses": 5, "points_for": 1748.7, "points_against": 1617.2, "point_diff": 131.5, "streak": 'W-4', "waiver_budget": None, "waiver_rank": 2, "moves": 29},
    {"year": 2021, "manager": 'Brett', "team": '3 first round picks-ylvania', "finish": 6, "wins": 8, "losses": 6, "points_for": 1633.0, "points_against": 1586.7, "point_diff": 46.3, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 3, "moves": 19},
    {"year": 2021, "manager": 'Tim', "team": 'Booty Meat', "finish": 7, "wins": 4, "losses": 10, "points_for": 1567.4, "points_against": 1782.6, "point_diff": -215.2, "streak": 'L-3', "waiver_budget": None, "waiver_rank": 9, "moves": 26},
    {"year": 2021, "manager": 'Zach', "team": "Allen's Army", "finish": 8, "wins": 6, "losses": 8, "points_for": 1606.7, "points_against": 1675.8, "point_diff": -69.1, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 4, "moves": 34},
    {"year": 2021, "manager": 'Pat', "team": 'Ebron James', "finish": 9, "wins": 3, "losses": 11, "points_for": 1546.1, "points_against": 1675.4, "point_diff": -129.2, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 7, "moves": 21},
    {"year": 2021, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 10, "wins": 5, "losses": 9, "points_for": 1589.9, "points_against": 1729.0, "point_diff": -139.1, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 1, "moves": 20},
    {"year": 2021, "manager": 'Wonjoon', "team": 'Fantasy Futbol', "finish": 11, "wins": 6, "losses": 8, "points_for": 1606.9, "points_against": 1722.4, "point_diff": -115.5, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 11, "moves": 20},
    {"year": 2021, "manager": 'Tyler', "team": '#KeironIsOverParty', "finish": 12, "wins": 6, "losses": 8, "points_for": 1606.2, "points_against": 1767.9, "point_diff": -161.7, "streak": 'L-3', "waiver_budget": None, "waiver_rank": 12, "moves": 42},
    {"year": 2020, "manager": 'Brian', "team": 'The Covfefe Crew', "finish": 1, "wins": 9, "losses": 4, "points_for": 1355.3, "points_against": 1200.8, "point_diff": 154.5, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 12, "moves": 25},
    {"year": 2020, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 2, "wins": 10, "losses": 3, "points_for": 1361.7, "points_against": 1154.3, "point_diff": 207.4, "streak": 'W-4', "waiver_budget": None, "waiver_rank": 11, "moves": 36},
    {"year": 2020, "manager": 'Tyler', "team": 'KeironComeHome', "finish": 3, "wins": 7, "losses": 6, "points_for": 1207.7, "points_against": 1297.6, "point_diff": -89.9, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 10, "moves": 37},
    {"year": 2020, "manager": 'Brett', "team": 'Hurtsylvania', "finish": 4, "wins": 7, "losses": 6, "points_for": 1228.4, "points_against": 1137.7, "point_diff": 90.7, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 1, "moves": 5},
    {"year": 2020, "manager": 'Pat', "team": 'Ebron James', "finish": 5, "wins": 9, "losses": 4, "points_for": 1262, "points_against": 1162.8, "point_diff": 99.2, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 9, "moves": 27},
    {"year": 2020, "manager": 'Nan', "team": "Todd Grrrley's knees", "finish": 6, "wins": 8, "losses": 5, "points_for": 1356.3, "points_against": 1183, "point_diff": 173.3, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 6, "moves": 18},
    {"year": 2020, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 7, "wins": 5, "losses": 8, "points_for": 1207.7, "points_against": 1231.4, "point_diff": -23.8, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 5, "moves": 25},
    {"year": 2020, "manager": 'Zach', "team": 'Billieve Baby', "finish": 8, "wins": 7, "losses": 6, "points_for": 1206.5, "points_against": 1243.6, "point_diff": -37.1, "streak": 'L-3', "waiver_budget": None, "waiver_rank": 8, "moves": 38},
    {"year": 2020, "manager": 'Tim', "team": 'Booty Meat', "finish": 9, "wins": 3, "losses": 10, "points_for": 1129.8, "points_against": 1294.2, "point_diff": -164.4, "streak": 'L-5', "waiver_budget": None, "waiver_rank": 3, "moves": 12},
    {"year": 2020, "manager": 'Paul', "team": "Brady's Ugly", "finish": 10, "wins": 5, "losses": 8, "points_for": 1228.9, "points_against": 1286.7, "point_diff": -57.8, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 7, "moves": 15},
    {"year": 2020, "manager": 'John', "team": 'Big Green Machine', "finish": 11, "wins": 5, "losses": 8, "points_for": 1089.6, "points_against": 1214.6, "point_diff": -125.0, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 2, "moves": 17},
    {"year": 2020, "manager": 'Wonjoon', "team": 'Fantasy Futbol', "finish": 12, "wins": 3, "losses": 10, "points_for": 1112.7, "points_against": 1340.0, "point_diff": -227.3, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 4, "moves": 17},
    {"year": 2019, "manager": 'Tim', "team": 'Booty Meat', "finish": 1, "wins": 9, "losses": 4, "points_for": 1315.4, "points_against": 1165.1, "point_diff": 150.3, "streak": 'W-5', "waiver_budget": None, "waiver_rank": 11, "moves": 21},
    {"year": 2019, "manager": 'John', "team": 'Big Green Machine', "finish": 2, "wins": 9, "losses": 4, "points_for": 1349.8, "points_against": 1103.6, "point_diff": 246.3, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 9, "moves": 27},
    {"year": 2019, "manager": 'Brett', "team": 'Wentzsylvania', "finish": 3, "wins": 8, "losses": 5, "points_for": 1224.3, "points_against": 1243.0, "point_diff": -18.6, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 10, "moves": 22},
    {"year": 2019, "manager": 'Nan', "team": 'Luck-less Colt', "finish": 4, "wins": 9, "losses": 4, "points_for": 1304.3, "points_against": 1175.1, "point_diff": 129.3, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 8, "moves": 21},
    {"year": 2019, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 5, "wins": 8, "losses": 5, "points_for": 1211.9, "points_against": 1149.7, "point_diff": 62.2, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 7, "moves": 29},
    {"year": 2019, "manager": 'Paul', "team": "Brady's Ugly", "finish": 6, "wins": 9, "losses": 4, "points_for": 1149.6, "points_against": 1086.0, "point_diff": 63.6, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 1, "moves": 8},
    {"year": 2019, "manager": 'Zach', "team": 'White Wolverines', "finish": 7, "wins": 6, "losses": 7, "points_for": 1167.5, "points_against": 1209.5, "point_diff": -42.0, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 6, "moves": 18},
    {"year": 2019, "manager": 'Brian', "team": 'The Covfefe Crew', "finish": 8, "wins": 5, "losses": 8, "points_for": 1181.3, "points_against": 1270.9, "point_diff": -89.6, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 12, "moves": 22},
    {"year": 2019, "manager": 'Tyler', "team": 'Keirons a Bitch42069', "finish": 9, "wins": 6, "losses": 7, "points_for": 1190.2, "points_against": 1116.4, "point_diff": 73.8, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 3, "moves": 29},
    {"year": 2019, "manager": 'Wonjoon', "team": 'Fantasy Futbol', "finish": 10, "wins": 1, "losses": 12, "points_for": 924.1, "points_against": 1233.5, "point_diff": -309.4, "streak": 'L-4', "waiver_budget": None, "waiver_rank": 4, "moves": 6},
    {"year": 2019, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 11, "wins": 3, "losses": 10, "points_for": 1028.8, "points_against": 1279.6, "point_diff": -250.8, "streak": 'L-4', "waiver_budget": None, "waiver_rank": 2, "moves": 31},
    {"year": 2019, "manager": 'Pat', "team": 'Ebron James', "finish": 12, "wins": 5, "losses": 8, "points_for": 1236.7, "points_against": 1251.6, "point_diff": -14.9, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 5, "moves": 18},
    {"year": 2018, "manager": 'Pat', "team": 'Ebron James', "finish": 1, "wins": 10, "losses": 3, "points_for": 1425.5, "points_against": 1113.3, "point_diff": 312.2, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 11, "moves": 27},
    {"year": 2018, "manager": 'Tim', "team": 'Booty Meat', "finish": 2, "wins": 8, "losses": 5, "points_for": 1348.5, "points_against": 1269.2, "point_diff": 79.2, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 6, "moves": 17},
    {"year": 2018, "manager": 'Paul', "team": "Brady's Ugly", "finish": 3, "wins": 7, "losses": 6, "points_for": 1386.8, "points_against": 1246.7, "point_diff": 140.1, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 8, "moves": 6},
    {"year": 2018, "manager": 'Nan', "team": 'Happy Saquon-za', "finish": 4, "wins": 8, "losses": 5, "points_for": 1271.3, "points_against": 1153.1, "point_diff": 118.2, "streak": 'W-4', "waiver_budget": None, "waiver_rank": 9, "moves": 31},
    {"year": 2018, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 5, "wins": 8, "losses": 5, "points_for": 1243.4, "points_against": 1210.7, "point_diff": 32.6, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 10, "moves": 28},
    {"year": 2018, "manager": 'Tyler', "team": 'Keirons a Bitch42069', "finish": 6, "wins": 7, "losses": 6, "points_for": 1151.0, "points_against": 1203.5, "point_diff": -52.4, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 3, "moves": 16},
    {"year": 2018, "manager": 'John', "team": 'Big Green Machine', "finish": 7, "wins": 5, "losses": 8, "points_for": 1089.3, "points_against": 1216.4, "point_diff": -127.2, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 12, "moves": 21},
    {"year": 2018, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 8, "wins": 6, "losses": 7, "points_for": 1235.5, "points_against": 1309.2, "point_diff": -73.7, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 4, "moves": 23},
    {"year": 2018, "manager": 'Wonjoon', "team": 'Fantasy Futbol', "finish": 9, "wins": 6, "losses": 7, "points_for": 1310.1, "points_against": 1268.5, "point_diff": 41.6, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 5, "moves": 17},
    {"year": 2018, "manager": 'Zach', "team": 'White Wolverines', "finish": 10, "wins": 6, "losses": 7, "points_for": 1109.8, "points_against": 1245.0, "point_diff": -135.1, "streak": 'L-4', "waiver_budget": None, "waiver_rank": 2, "moves": 15},
    {"year": 2018, "manager": 'Brian', "team": 'The Covfefe Crew', "finish": 11, "wins": 5, "losses": 8, "points_for": 1393.1, "points_against": 1418.4, "point_diff": -25.3, "streak": 'L-5', "waiver_budget": None, "waiver_rank": 7, "moves": 20},
    {"year": 2018, "manager": 'Brett', "team": 'Wentzsylvania', "finish": 12, "wins": 2, "losses": 11, "points_for": 1018.9, "points_against": 1329.2, "point_diff": -310.3, "streak": 'L-7', "waiver_budget": None, "waiver_rank": 1, "moves": 5},
    {"year": 2017, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 1, "wins": 8, "losses": 5, "points_for": 1097.1, "points_against": 1049.2, "point_diff": 47.9, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 11, "moves": 26},
    {"year": 2017, "manager": 'Paul', "team": "Brady's Ugly", "finish": 2, "wins": 9, "losses": 4, "points_for": 1136.1, "points_against": 1079.4, "point_diff": 56.6, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 3, "moves": 1},
    {"year": 2017, "manager": 'Nan', "team": 'Cash me OWLside hbd', "finish": 3, "wins": 7, "losses": 6, "points_for": 1183.1, "points_against": 1108.0, "point_diff": 75.1, "streak": 'W-5', "waiver_budget": None, "waiver_rank": 12, "moves": 39},
    {"year": 2017, "manager": 'Pat', "team": 'Ebron James', "finish": 4, "wins": 7, "losses": 6, "points_for": 1235.1, "points_against": 1183.3, "point_diff": 51.8, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 9, "moves": 22},
    {"year": 2017, "manager": 'Brian', "team": 'The Covfefe Crew', "finish": 5, "wins": 7, "losses": 6, "points_for": 1169.1, "points_against": 1124, "point_diff": 45.1, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 7, "moves": 28},
    {"year": 2017, "manager": 'Wonjoon', "team": 'Fantasy Futbol', "finish": 6, "wins": 7, "losses": 6, "points_for": 1187.0, "points_against": 1156.2, "point_diff": 30.9, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 8, "moves": 14},
    {"year": 2017, "manager": 'Brett', "team": 'Wentzsylvania', "finish": 7, "wins": 7, "losses": 6, "points_for": 1135.1, "points_against": 1181.7, "point_diff": -46.6, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 5, "moves": 14},
    {"year": 2017, "manager": 'John', "team": 'Big Green Machine', "finish": 8, "wins": 3, "losses": 10, "points_for": 1048.0, "points_against": 1225.3, "point_diff": -177.4, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 10, "moves": 19},
    {"year": 2017, "manager": 'Tim', "team": 'Booty Meat', "finish": 9, "wins": 4, "losses": 9, "points_for": 1013.9, "points_against": 1194.5, "point_diff": -180.7, "streak": 'L-5', "waiver_budget": None, "waiver_rank": 2, "moves": 19},
    {"year": 2017, "manager": 'Zach', "team": 'White Wolverines', "finish": 10, "wins": 7, "losses": 6, "points_for": 1134.4, "points_against": 1094.2, "point_diff": 40.2, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 4, "moves": 18},
    {"year": 2017, "manager": 'Tyler', "team": 'Keirons a Bitch42069', "finish": 11, "wins": 6, "losses": 7, "points_for": 1078.8, "points_against": 1133.7, "point_diff": -54.9, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 1, "moves": 32},
    {"year": 2017, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 12, "wins": 6, "losses": 7, "points_for": 1191.3, "points_against": 1079.4, "point_diff": 112.0, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 6, "moves": 29},
    {"year": 2016, "manager": 'Pat', "team": 'Ebron James', "finish": 1, "wins": 9, "losses": 4, "points_for": 1291.1, "points_against": 1179.8, "point_diff": 111.3, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 12, "moves": 27},
    {"year": 2016, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 2, "wins": 8, "losses": 5, "points_for": 1321.6, "points_against": 1204.4, "point_diff": 117.2, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 10, "moves": 12},
    {"year": 2016, "manager": 'Tyler', "team": 'Luke I Am Your Daddy', "finish": 3, "wins": 9, "losses": 4, "points_for": 1310.3, "points_against": 1101.5, "point_diff": 208.8, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 2, "moves": 10},
    {"year": 2016, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 4, "wins": 9, "losses": 4, "points_for": 1362.9, "points_against": 1172.6, "point_diff": 190.3, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 9, "moves": 23},
    {"year": 2016, "manager": 'Tim', "team": 'LeBron 4 President', "finish": 5, "wins": 7, "losses": 6, "points_for": 1179.6, "points_against": 1102.3, "point_diff": 77.3, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 7, "moves": 20},
    {"year": 2016, "manager": 'Nan', "team": 'Chickadeeflategate', "finish": 6, "wins": 5, "losses": 8, "points_for": 1246.3, "points_against": 1156.7, "point_diff": 89.6, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 6, "moves": 16},
    {"year": 2016, "manager": 'Zach', "team": 'White Wolverines', "finish": 7, "wins": 4, "losses": 9, "points_for": 1076.1, "points_against": 1239.3, "point_diff": -163.2, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 11, "moves": 7},
    {"year": 2016, "manager": 'Brett', "team": 'Temp Non-Adult', "finish": 8, "wins": 5, "losses": 8, "points_for": 1119.7, "points_against": 1201.5, "point_diff": -81.8, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 4, "moves": 7},
    {"year": 2016, "manager": 'John', "team": 'Big Green Machine', "finish": 9, "wins": 6, "losses": 7, "points_for": 1186.4, "points_against": 1175.5, "point_diff": 10.9, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 8, "moves": 15},
    {"year": 2016, "manager": 'Brian', "team": 'White Chocolate', "finish": 10, "wins": 6, "losses": 7, "points_for": 1064.9, "points_against": 1166.9, "point_diff": -102, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 5, "moves": 18},
    {"year": 2016, "manager": 'Paul', "team": "Brady's Ugly", "finish": 11, "wins": 2, "losses": 11, "points_for": 820.6, "points_against": 1172.4, "point_diff": -351.7, "streak": 'L-8', "waiver_budget": None, "waiver_rank": 1, "moves": 7},
    {"year": 2016, "manager": 'Wonjoon', "team": 'Fantasy Futbol', "finish": 12, "wins": 5, "losses": 8, "points_for": 1056.3, "points_against": 1163.1, "point_diff": -106.8, "streak": 'L-5', "waiver_budget": None, "waiver_rank": 3, "moves": 20},
    {"year": 2015, "manager": 'Zach', "team": 'White Wolverines', "finish": 1, "wins": 7, "losses": 6, "points_for": 1188.5, "points_against": 1134.3, "point_diff": 54.2, "streak": 'L-3', "waiver_budget": None, "waiver_rank": 10, "moves": 32},
    {"year": 2015, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 2, "wins": 10, "losses": 3, "points_for": 1429.3, "points_against": 1130.9, "point_diff": 298.4, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 12, "moves": 26},
    {"year": 2015, "manager": 'Nan', "team": "Duck Norris'", "finish": 3, "wins": 9, "losses": 4, "points_for": 1274.0, "points_against": 1139.0, "point_diff": 135.0, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 6, "moves": 33},
    {"year": 2015, "manager": 'Tim', "team": 'Road Beers', "finish": 4, "wins": 8, "losses": 5, "points_for": 1151.2, "points_against": 1206.9, "point_diff": -55.7, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 9, "moves": 26},
    {"year": 2015, "manager": 'John', "team": 'Big Green Machine', "finish": 5, "wins": 8, "losses": 5, "points_for": 1163.6, "points_against": 1119.4, "point_diff": 44.2, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 8, "moves": 20},
    {"year": 2015, "manager": 'Wonjoon', "team": 'Fantasy Futbol', "finish": 6, "wins": 8, "losses": 5, "points_for": 1346.9, "points_against": 1189.7, "point_diff": 157.3, "streak": 'W-4', "waiver_budget": None, "waiver_rank": 7, "moves": 21},
    {"year": 2015, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 7, "wins": 1, "losses": 12, "points_for": 1058.4, "points_against": 1240.7, "point_diff": -182.3, "streak": 'L-8', "waiver_budget": None, "waiver_rank": 5, "moves": 26},
    {"year": 2015, "manager": 'Tyler', "team": 'VICKtory', "finish": 8, "wins": 3, "losses": 10, "points_for": 981.3, "points_against": 1239.3, "point_diff": -258.0, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 2, "moves": 7},
    {"year": 2015, "manager": 'Brian', "team": 'White Chocolate', "finish": 9, "wins": 6, "losses": 7, "points_for": 1136.2, "points_against": 1306.8, "point_diff": -170.7, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 11, "moves": 32},
    {"year": 2015, "manager": 'Paul', "team": "Brady's Ugly", "finish": 10, "wins": 7, "losses": 6, "points_for": 1172.5, "points_against": 1074.6, "point_diff": 97.9, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 1, "moves": 3},
    {"year": 2015, "manager": 'Pat', "team": 'Show Me Your TDs', "finish": 11, "wins": 5, "losses": 8, "points_for": 1185.0, "points_against": 1260.7, "point_diff": -75.7, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 4, "moves": 19},
    {"year": 2015, "manager": 'Brett', "team": 'Temp Non-Adult', "finish": 12, "wins": 6, "losses": 7, "points_for": 1065.3, "points_against": 1109.9, "point_diff": -44.6, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 3, "moves": 13},
    {"year": 2014, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 1, "wins": 6, "losses": 7, "points_for": 1347.7, "points_against": 1463.4, "point_diff": -115.7, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 9, "moves": 29},
    {"year": 2014, "manager": 'John', "team": 'Big Green Machine', "finish": 2, "wins": 8, "losses": 5, "points_for": 1427.6, "points_against": 1277.9, "point_diff": 149.7, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 10, "moves": 24},
    {"year": 2014, "manager": 'Tyler', "team": "Red White 'n Blessed", "finish": 3, "wins": 6, "losses": 7, "points_for": 1217.8, "points_against": 1305.1, "point_diff": -87.3, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 6, "moves": 15},
    {"year": 2014, "manager": 'Zach', "team": 'White Wolverines', "finish": 4, "wins": 11, "losses": 2, "points_for": 1423.7, "points_against": 1178.2, "point_diff": 245.5, "streak": 'W-4', "waiver_budget": None, "waiver_rank": 8, "moves": 13},
    {"year": 2014, "manager": 'Brett', "team": 'Temp Non-Adult', "finish": 5, "wins": 7, "losses": 6, "points_for": 1281.9, "points_against": 1195.6, "point_diff": 86.3, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 2, "moves": 12},
    {"year": 2014, "manager": 'Nan', "team": 'Thirsty Emus', "finish": 6, "wins": 8, "losses": 5, "points_for": 1270.2, "points_against": 1266.5, "point_diff": 3.8, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 7, "moves": 36},
    {"year": 2014, "manager": 'Dan', "team": 'PlaxidantalDischarge', "finish": 7, "wins": 5, "losses": 8, "points_for": 1279.5, "points_against": 1347.3, "point_diff": -67.8, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 4, "moves": 26},
    {"year": 2014, "manager": 'Wonjoon', "team": 'Fantasy Futbol', "finish": 8, "wins": 6, "losses": 7, "points_for": 1151.3, "points_against": 1131.2, "point_diff": 20.0, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 3, "moves": 15},
    {"year": 2014, "manager": 'Brian', "team": 'White Chocolate', "finish": 9, "wins": 5, "losses": 8, "points_for": 1224.7, "points_against": 1324.3, "point_diff": -99.6, "streak": 'L-6', "waiver_budget": None, "waiver_rank": 5, "moves": 30},
    {"year": 2014, "manager": 'Tim', "team": 'Road Beers', "finish": 10, "wins": 3, "losses": 10, "points_for": 1145.2, "points_against": 1280.0, "point_diff": -134.8, "streak": 'L-5', "waiver_budget": None, "waiver_rank": 1, "moves": 22},
    {"year": 2013, "manager": 'Nan', "team": 'Bulimic Parakeets', "finish": 1, "wins": 8, "losses": 5, "points_for": 1300.4, "points_against": 1226.6, "point_diff": 73.8, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 9, "moves": 24},
    {"year": 2013, "manager": 'Dan', "team": 'Tittsburgh Feelers', "finish": 2, "wins": 7, "losses": 6, "points_for": 1150.7, "points_against": 1152.2, "point_diff": -1.5, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 4, "moves": 8},
    {"year": 2013, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 3, "wins": 9, "losses": 4, "points_for": 1427.2, "points_against": 1192.2, "point_diff": 235.0, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 7, "moves": 31},
    {"year": 2013, "manager": 'John', "team": 'Big Green Machine', "finish": 4, "wins": 8, "losses": 5, "points_for": 1351.6, "points_against": 1190.6, "point_diff": 161, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 10, "moves": 30},
    {"year": 2013, "manager": 'Brett', "team": 'Temp Non-Adult', "finish": 5, "wins": 7, "losses": 6, "points_for": 1298, "points_against": 1204.1, "point_diff": 93.9, "streak": 'W-2', "waiver_budget": None, "waiver_rank": 5, "moves": 18},
    {"year": 2013, "manager": 'Brian', "team": 'White Chocolate', "finish": 6, "wins": 7, "losses": 6, "points_for": 1124.5, "points_against": 1147.1, "point_diff": -22.6, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 8, "moves": 31},
    {"year": 2013, "manager": 'Zach', "team": 'White Wolverines', "finish": 7, "wins": 6, "losses": 7, "points_for": 1164.3, "points_against": 1223.2, "point_diff": -58.9, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 6, "moves": 29},
    {"year": 2013, "manager": 'Tim', "team": 'Road Beers', "finish": 8, "wins": 4, "losses": 9, "points_for": 1095.5, "points_against": 1290.7, "point_diff": -195.2, "streak": 'L-5', "waiver_budget": None, "waiver_rank": 1, "moves": 1},
    {"year": 2013, "manager": 'Wonjoon', "team": 'Azn Beast', "finish": 9, "wins": 3, "losses": 10, "points_for": 1068.5, "points_against": 1282.6, "point_diff": -214.1, "streak": 'L-3', "waiver_budget": None, "waiver_rank": 3, "moves": 14},
    {"year": 2013, "manager": 'Tyler', "team": '81YearsToLife', "finish": 10, "wins": 6, "losses": 7, "points_for": 1111.7, "points_against": 1183.0, "point_diff": -71.3, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 2, "moves": 7},
    {"year": 2012, "manager": 'Keiron', "team": "Brady's Bunch", "finish": 1, "wins": 10, "losses": 3, "points_for": 1436.7, "points_against": 1216.0, "point_diff": 220.8, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 5, "moves": 19},
    {"year": 2012, "manager": 'Nan', "team": '3Peat', "finish": 2, "wins": 10, "losses": 3, "points_for": 1293.4, "points_against": 1191.9, "point_diff": 101.6, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 10, "moves": 17},
    {"year": 2012, "manager": 'Dan', "team": 'Tittsburgh Feelers', "finish": 3, "wins": 6, "losses": 7, "points_for": 1264.8, "points_against": 1233.9, "point_diff": 30.9, "streak": 'L-2', "waiver_budget": None, "waiver_rank": 4, "moves": 8},
    {"year": 2012, "manager": 'John', "team": 'Big Green Machine', "finish": 4, "wins": 8, "losses": 5, "points_for": 1307.5, "points_against": 1134.6, "point_diff": 172.9, "streak": 'W-4', "waiver_budget": None, "waiver_rank": 9, "moves": 16},
    {"year": 2012, "manager": 'Tyler', "team": '[redacted]', "finish": 5, "wins": 8, "losses": 5, "points_for": 1151.0, "points_against": 1144.8, "point_diff": 6.2, "streak": 'W-3', "waiver_budget": None, "waiver_rank": 3, "moves": 0},
    {"year": 2012, "manager": 'Brett', "team": '2 Real Adult 4 U', "finish": 6, "wins": 6, "losses": 7, "points_for": 1171.3, "points_against": 1159.9, "point_diff": 11.5, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 7, "moves": 14},
    {"year": 2012, "manager": 'Brian', "team": 'White Chocolate', "finish": 7, "wins": 4, "losses": 9, "points_for": 1190, "points_against": 1370.8, "point_diff": -180.8, "streak": 'L-4', "waiver_budget": None, "waiver_rank": 6, "moves": 11},
    {"year": 2012, "manager": 'Tim', "team": 'Senior Year Blackout', "finish": 8, "wins": 5, "losses": 8, "points_for": 1062.1, "points_against": 1213.2, "point_diff": -151.2, "streak": 'W-1', "waiver_budget": None, "waiver_rank": 2, "moves": 0},
    {"year": 2012, "manager": 'Zach', "team": 'White Wolverines', "finish": 9, "wins": 4, "losses": 9, "points_for": 1097.7, "points_against": 1228.6, "point_diff": -130.9, "streak": 'L-1', "waiver_budget": None, "waiver_rank": 8, "moves": 12},
    {"year": 2012, "manager": 'Wonjoon', "team": 'Azn Beast', "finish": 10, "wins": 4, "losses": 9, "points_for": 1030.0, "points_against": 1110.8, "point_diff": -80.9, "streak": 'L-3', "waiver_budget": None, "waiver_rank": 1, "moves": 0},
]

SEASON_RESULTS_YEARS = sorted({row['year'] for row in SEASON_RESULTS}, reverse=True)

# Live trivia deck. Every answer below was derived from SEASON_RESULTS /
# HISTORICAL_COMPARISON rather than memory — "note" is the supporting stat,
# shown only once the host reveals the answer.
TRIVIA_QUESTIONS = [
    {
        "question": "In 2021 a team went 13-1 — the best record in league history — and scored more points than any team ever has. Where did it finish?",
        "options": ["1st", "2nd", "3rd", "4th"],
        "answer": 2,
        "note": "Nan's Fire Gutekunst went 13-1 with 1,945.1 points and a +519.8 differential, all league records, and still finished 3rd.",
    },
    {
        "question": "Which manager has never once finished in the top three?",
        "options": ["Tyler", "Wonjoon", "Brett", "Paul"],
        "answer": 1,
        "note": "Wonjoon is the only manager with zero top-three finishes in 14 seasons, and has finished last four times.",
    },
    {
        "question": "Tyler has named his team after the same league member in at least five different seasons. Who?",
        "options": ["Keiron", "Nan", "Wonjoon", "Brett"],
        "answer": 0,
        "note": "Keirons a Bitch42069 (2017-19), KeironComeHome (2020), then #KeironIsOverParty (2021-24).",
    },
    {
        "question": "Who holds the record for the FEWEST points in a single season — just 820.6?",
        "options": ["Wonjoon", "Tyler", "Paul", "Brett"],
        "answer": 2,
        "note": "Paul's 2016 Brady's Ugly scored 820.6 and went 2-11. The next-worst season is over 100 points higher.",
    },
    {
        "question": "What is the most roster moves anyone has made in a single season?",
        "options": ["38", "45", "57", "64"],
        "answer": 2,
        "note": "John made 57 moves in 2025 — and still only finished 6th. He also leads all-time with 403.",
    },
    {
        "question": "Who won the league in 2015 with a losing 7-6 record?",
        "options": ["Zach", "Dan", "Brian", "Tim"],
        "answer": 0,
        "note": "Zach's White Wolverines took the 2015 title at 7-6. Keiron did it too in 2014, at 6-7.",
    },
    {
        "question": "Wonjoon set a league record in 2025. What was his final record?",
        "options": ["2-12", "1-13", "0-14", "0-13"],
        "answer": 2,
        "note": "0-14 — the only winless season in league history, with a -585.8 point differential.",
    },
    {
        "question": "Which team name has won the league three separate times?",
        "options": ["Big Green Machine", "Ebron James", "Brady's Bunch", "PlaxidantalDischarge"],
        "answer": 1,
        "note": "Pat's Ebron James won in 2016, 2018 and 2023 — the only name to take three titles.",
    },
    {
        "question": "Who has the best average league finish across all 14 seasons?",
        "options": ["Dan", "John", "Pat", "Nan"],
        "answer": 3,
        "note": "Nan averages a 3.7 finish and 8.4 wins per season, comfortably ahead of Dan at 4.7.",
    },
    {
        "question": "Who won the 2025 season?",
        "options": ["Brett", "Paul", "Dan", "Nan"],
        "answer": 0,
        "note": "Brett's wonsuperbowl went 9-5 and took the 2025 title.",
    },
]
