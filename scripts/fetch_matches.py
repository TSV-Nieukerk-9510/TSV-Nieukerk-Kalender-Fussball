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



        
def fetch_match_location(match_url):

    if not match_url:
        return "", ""

    try:

        response = requests.get(
            match_url,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        text = soup.get_text(
            "\n",
            strip=True
        )

        location = ""
        pitch = ""

        lines = [
            line.strip()
            for line in text.split("\n")
            if line.strip()
        ]

        keywords = [
            "Sportanlage",
            "Spielort",
            "Austragungsort"
        ]

        for i, line in enumerate(lines):

            if any(
                keyword.lower()
                in line.lower()
                for keyword in keywords
            ):

                collected = []

                for candidate in lines[i + 1:i + 5]:

                    if any(
                        stop in candidate.lower()
                        for stop in [
                            "schiedsrichter",
                            "spielberichte",
                            "zuschauer",
                            "staffel-id",
                            "spiel:"
                        ]
                    ):
                        break

                    collected.append(
                        candidate
                    )

                location = ", ".join(
                    collected
                )

                break

        if "Kunstrasen" in text:
            pitch = "Kunstrasen"

        elif "Naturrasen" in text:
            pitch = "Naturrasen"

        elif "Rasenplatz" in text:
            pitch = "Rasenplatz"

        if location:

            location = re.sub(
                r"\s+",
                " ",
                location
            )

            location = (
                location.replace(
                    " ,",
                    ","
                )
                .strip()
            )

        return location, pitch

    except Exception as e:

        print(
            f"Spielort konnte nicht gelesen werden: "
            f"{match_url}"
        )

        print(e)

        return "", ""

def fetch_team_matches(team_id):

    matchplan_url = (
        f"https://www.fussball.de/ajax.team.matchplan/"
        f"-/mode/PAGE/team-id/{team_id}"
    )

    print(f"Lade Matchplan: {matchplan_url}")

    response = requests.get(
        matchplan_url,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    matches = []

    competition_rows = soup.select(
        "tr.row-competition"
    )

    print(
        f"Gefundene Spieltermine: "
        f"{len(competition_rows)}"
    )

    for competition_row in competition_rows:

        game_row = competition_row.find_next_sibling("tr")

        if not game_row:
            continue

        date_cell = competition_row.select_one(
            ".column-date"
        )

        if not date_cell:
            continue

        date_text = date_cell.get_text(
            " ",
            strip=True
        )

        date_match = re.search(
            r"(\d{2}\.\d{2}\.\d{2})",
            date_text
        )

        time_match = re.search(
            r"(\d{1,2}\:\d{2})",
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

        home_team = clubs[0].get_text(
            strip=True
        )

        away_team = clubs[1].get_text(
            strip=True
        )

        competition = ""

        competition_cell = competition_row.select_one(
            ".column-team"
        )

        if competition_cell:

            competition = (
                competition_cell
                .get_text(strip=True)
            )

        match_link = ""

        score_link = game_row.select_one(
            ".column-score a"
        )

        if score_link:

            match_link = score_link.get(
                "href",
                ""
            )

        location = ""
        pitch = ""

        if match_link:

            location, pitch = (
                fetch_match_location(
                    match_link
                )
            )

        matches.append({
            "home": home_team,
            "away": away_team,
            "date": date_iso,
            "time": (
                time_match.group(1)
                if time_match
                else "00:00"
            ),
            "competition": competition,
            "location": location,
            "pitch": pitch,
            "match_url": match_link
        })

    print(
        f"Insgesamt {len(matches)} Spiele gefunden"
    )

    return matches
