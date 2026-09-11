import json
import os
import re

import requests
from bs4 import BeautifulSoup


CLUB_ID = "00ES8GN8UK0000ALVV0AG08LVUPGND5I"
SEASON = "2627"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0 Safari/537.36"
    )
}


def create_calendar_name(team_name):

    calendar = team_name

    calendar = calendar.replace(" - ", "-")
    calendar = calendar.replace(" / ", "-")
    calendar = calendar.replace("/", "-")
    calendar = calendar.replace("(", "")
    calendar = calendar.replace(")", "")
    calendar = calendar.replace("​", "")

    calendar = re.sub(
        r"[^A-Za-z0-9ÄÖÜäöüß-]+",
        "-",
        calendar
    )

    calendar = re.sub(
        r"-+",
        "-",
        calendar
    )

    calendar = calendar.strip("-")

    return (
        f"{calendar}-{SEASON}.ics"
    )


def extract_team_id(url):

    match = re.search(
        r"team-id/([^/?#]+)",
        url
    )

    if match:
        return match.group(1)

    return ""


def discover_teams():

    ajax_url = (
        "https://www.fussball.de/ajax.club.teams/"
        f"-/action/search/id/{CLUB_ID}"
    )

    print(
        f"Lade Mannschaften: {ajax_url}"
    )

    response = requests.post(
        ajax_url,
        headers=HEADERS,
        data={
            "saison": SEASON,
            "mannschaftsart": "-1",
            "wettkampftyp": "-1"
        },
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    teams = []

    items = soup.select(
        ".result .item"
    )

    print(
        f"Gefundene Einträge: "
        f"{len(items)}"
    )

    for item in items:

        link = item.select_one(
            "h4 a"
        )

        if not link:
            continue

        team_url = link.get(
            "href",
            ""
        )

        team_name = link.get_text(
            " ",
            strip=True
        )

        team_name = re.sub(
            r"\s+",
            " ",
            team_name
        )

        team_id = extract_team_id(
            team_url
        )

        if not team_id:
            continue

        team = {
            "name": team_name,
            "season": SEASON,
            "calendar": create_calendar_name(
                team_name
            ),
            "team_id": team_id,
            "url": team_url,
            "include_location": True
        }

        teams.append(team)

        print(
            f"{team_name} "
            f"({team_id})"
        )

    os.makedirs(
        "config",
        exist_ok=True
    )

    output_file = (
        "config/teams.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            teams,
            f,
            ensure_ascii=False,
            indent=4
        )

    print()
    print(
        f"{len(teams)} Teams gespeichert:"
    )
    print(output_file)


if __name__ == "__main__":
    discover_teams()

