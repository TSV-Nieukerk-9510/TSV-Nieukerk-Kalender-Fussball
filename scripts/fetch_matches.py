import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_team_matches(team_url):
    """
    Universeller Parser für fussball.de Spielpläne.
    Funktioniert für:
    - Teamseiten
    - JSG-Teams
    - Jugendmannschaften
    - Staffel-/Spielplan-Seiten
    """

    resp = requests.get(team_url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")

    matches = []

    # 1) Neue fussball.de Struktur (match-row)
    for row in soup.select("div.match-row, div.fixture-row, div.match"):
        home = row.select_one(".team-home, .home, .team-left")
        away = row.select_one(".team-away, .away, .team-right")
        date = row.select_one(".match-date, .date")
        time = row.select_one(".match-time, .time")
        location = row.select_one(".location,