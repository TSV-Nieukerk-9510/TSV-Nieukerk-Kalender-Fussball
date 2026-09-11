# scripts/fetch_matches.py

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0 Safari/537.36"
    )
}


def normalize_date(text):
    text = text.strip()

    patterns = [
        "%d.%m.%Y",
        "%d.%m.%y",
    ]

    for pattern in patterns:
        try:
            return datetime.strptime(text, pattern).strftime("%Y-%m-%d")
        except ValueError:
            pass

    match = re.search(r"(\d{2}\.\d{2}\.\d{4})", text)
    if match:
        try:
            return datetime.strptime(
                match.group(1),
                "%d.%m.%Y"
            ).strftime("%Y-%m-%d")
        except ValueError:
            pass

    return None


def normalize_time(text):
    if not text:
        return "00:00"

    match = re.search(r"(\d{1,2}:\d{2})", text)
    if match:
        return match.group(1)

    return "00:00"


def fetch_team_matches(team_url):
    print(f"Lade: {team_url}")

    response = requests.get(
        team_url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    print("HTTP:", response.status_code)

    soup = BeautifulSoup(response.text, "lxml")

    matches = []

    # Debug-Datei schreiben
    with open("debug_fussball.html", "w", encoding="utf-8") as f:
        f.write(response.text)

    # Alle Tabellen untersuchen
    rows = soup.find_all("tr")

    print(f"Gefundene Tabellenzeilen: {len(rows)}")

    for row in rows:
        cells = row.find_all(["td", "th"])

        texts = [
            cell.get_text(" ", strip=True)
            for cell in cells
        ]

        if len(texts) < 4:
            continue

        joined = " | ".join(texts)

        date_match = re.search(
            r"\d{2}\.\d{2}\.\d{4}",
            joined
        )

        time_match = re.search(
            r"\d{1,2}:\d{2}",
            joined
        )

        if not date_match:
            continue

        date_iso = normalize_date(date_match.group())

        if not date_iso:
            continue

        time_str = (
            normalize_time(time_match.group())
            if time_match
            else "00:00"
        )

        home = ""
        away = ""

        if len(texts) >= 2:
            home = texts[0]
            away = texts[1]

        if not home or not away:
            continue

        match = {
            "home": home,
            "away": away,
            "date": date_iso,
            "time": time_str,
            "location": "",
            "pitch": ""
        }

        matches.append(match)

    print(f"Ermittelte Spiele: {len(matches)}")

    for m in matches[:10]:
        print(m)

    return matches
