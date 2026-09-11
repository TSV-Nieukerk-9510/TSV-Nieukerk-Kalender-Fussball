import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_team_matches(team_url):

    response = requests.get(
        team_url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    matches = []

    competition_rows = soup.select("tr.row-competition")

    print(f"{len(competition_rows)} Spieltermine gefunden")

    for comp_row in competition_rows:

        game_row = comp_row.find_next_sibling("tr")

        if not game_row:
            continue

        date_cell = comp_row.select_one(".column-date")

        if not date_cell:
            continue

        date_text = date_cell.get_text(" ", strip=True)

        date_match = re.search(
            r"(\d{2}\.\d{2}\.\d{2})",
            date_text
        )

        time_match = re.search(
            r"(\d{1,2}:\d{2})",
            date_text
        )

        if not date_match:
            continue

        try:
            date_iso = datetime.strptime(
                date_match.group(1),
                "%d.%m.%y"
            ).strftime("%Y-%m-%d")
        except Exception:
            continue

        clubs = game_row.select(".club-name")

        if len(clubs) < 2:
            continue

        home = clubs[0].get_text(strip=True)
        away = clubs[1].get_text(strip=True)

        matches.append({
            "home": home,
            "away": away,
            "date": date_iso,
            "time": time_match.group(1) if time_match else "00:00",
            "location": "",
            "pitch": ""
        })

    print(f"Insgesamt {len(matches)} Spiele gefunden")

    for m in matches[:5]:
        print(m)

    return matches
