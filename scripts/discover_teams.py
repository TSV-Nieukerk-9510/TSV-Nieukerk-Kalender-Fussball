import json
import os
import re

import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/128.0 Safari/537.36"
    )
}


def load_club_config():

    with open(
        "config/club.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def extract_team_id(url):

    match = re.search(
        r"team-id/([^/?#]+)",
        url
    )

    if match:
        return match.group(1)

    return ""


def create_calendar_name(team_name, season):

    team_name = (
        team_name
        .replace("\u200b", "")
        .replace("​", "")
        .strip()
    )

    mappings = {

        "Herren - TSV Nieukerk":
            f"TSV-H1-{season}.ics",

        "Herren - TSV Nieukerk II":
            f"TSV-H2-{season}.ics",

        "A-Junioren - JSG Aldekerk / Nieukerk":
            f"JSG-A1-{season}.ics",

        "B-Junioren - JSG Nieukerk / Aldekerk":
            f"JSG-B1-{season}.ics",

        "C-Junioren - JSG Aldekerk / Nieukerk":
            f"JSG-C1-{season}.ics",

        "C-Junioren - JSG Aldekerk / Nieukerk II":
            f"JSG-C2-{season}.ics",

        "D-Junioren - TSV Nieukerk":
            f"TSV-D1-{season}.ics",

        "E-Junioren - TSV Nieukerk":
            f"TSV-E1-{season}.ics",

        "E-Junioren - TSV Nieukerk II":
            f"TSV-E2-{season}.ics",

        "F-Junioren - TSV Nieukerk":
            f"TSV-F1-{season}.ics",

        "F-Junioren - TSV Nieukerk II":
            f"TSV-F2-{season}.ics",

        "G-Junioren - TSV Nieukerk":
            f"TSV-G1-{season}.ics",

        "D-Juniorinnen - TSV Nieukerk":
            f"TSV-DM-{season}.ics"
    }

    if team_name in mappings:
        return mappings[team_name]

    safe_name = re.sub(
        r"[^A-Za-z0-9]+",
        "-",
        team_name
    )

    safe_name = re.sub(
        r"-+",
        "-",
        safe_name
    )

    safe_name = safe_name.strip("-")

    return f"{safe_name}-{season}.ics"


def discover_teams():

    club_config = load_club_config()

    club_id = club_config["club_id"]
    season = club_config["season"]

    ajax_url = (
        "https://www.fussball.de/ajax.club.teams/"
        f"-/action/search/id/{club_id}"
    )

    print(
        f"Lade Mannschaften: {ajax_url}"
    )

    response = requests.post(
        ajax_url,
        headers=HEADERS,
        data={
            "saison": season,
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

        team_name = (
            team_name
            .replace("\u200b", "")
            .replace("​", "")
            .strip()
        )

        team_id = extract_team_id(
            team_url
        )

        if not team_id:
            continue

        calendar_name = create_calendar_name(
            team_name,
            season
        )

        team = {
            "name": team_name,
            "season": season,
            "calendar": calendar_name,
            "team_id": team_id,
            "url": team_url,
            "include_location": True
        }

        teams.append(team)

        print(
            f"{team_name} "
            f"({team_id}) "
            f"-> {calendar_name}"
        )

    teams.sort(
        key=lambda x: x["calendar"]
    )

    os.makedirs(
        "config",
        exist_ok=True
    )

    with open(
        "config/teams.json",
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

    print(
        "config/teams.json"
    )


if __name__ == "__main__":
    discover_teams()
