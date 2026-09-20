import json
import os

from datetime import datetime
from ics import Calendar, Event

from scripts.fetch_matches import fetch_team_matches
from zoneinfo import ZoneInfo
import re

print("### SCRIPT STARTET ###")


def load_teams():

    print("Öffne config/teams.json")

    if not os.path.exists("config/teams.json"):
        raise FileNotFoundError(
            "config/teams.json wurde nicht gefunden"
        )

    with open(
        "config/teams.json",
        "r",
        encoding="utf-8"
    ) as f:

        content = f.read()

    print("Inhalt teams.json:")

    print(content)

    teams = json.loads(content)

    print(
        f"{len(teams)} Teams geladen"
    )

    return teams


def is_valid_date(date_str):

    try:
        datetime.strptime(
            date_str,
            "%Y-%m-%d"
        )
        return True

    except Exception:
        return False


def create_calendar(team, matches):

    print(
        f"\nErzeuge Kalender für "
        f"{team['name']}"
    )

    cal = Calendar()

    added_events = 0

    for m in matches:

        if not is_valid_date(
            m["date"]
        ):
            continue

        try:

            event = Event()

            event.name = (
                f"{m['home']} vs {m['away']}"
            )

            dt = datetime.strptime(
                f"{m['date']} {m['time']}",
                "%Y-%m-%d %H:%M"
            )

            dt = dt.replace(
                tzinfo=ZoneInfo("Europe/Berlin")
            )

            print(dt)

            # event.begin = dt
            event.begin = f"{m['date']} {m['time']}"
            print(event.begin)
                
            event.uid = (
                f"{team['team_id']}-"
                f"{m['date']}-"
                f"{m['time']}-"
                f"{m['home']}-"
                f"{m['away']}"
            ).replace(" ", "_")

            location = ""

            if m.get("location"):
                location = m["location"]

            if m.get("pitch"):

                if location:
                    location += (
                        f" ({m['pitch']})"
                    )
                else:
                    location = m["pitch"]

            if location:
                event.location = location

            description = []

            description.append(
                f"Mannschaft: {team['name']}"
            )

            description.append(
                f"Saison: {team['season']}"
            )

            if m.get("competition"):
                description.append(
                    f"Wettbewerb: "
                    f"{m['competition']}"
                )

            if m.get("location"):
                description.append(
                    f"Spielort: "
                    f"{m['location']}"
                )

            if m.get("pitch"):
                description.append(
                    f"Belag: "
                    f"{m['pitch']}"
                )

            if m.get("match_url"):
                description.append(
                    f"Spielseite: "
                    f"{m['match_url']}"
                )

            description.append(
                f"Mannschaftsseite: "
                f"{team['url']}"
            )

            event.description = (
                "\n".join(description)
            )

            cal.events.add(event)

            added_events += 1

        except Exception as e:

            print(
                "Fehler beim Event:"
            )

            print(str(e))

    os.makedirs(
        "kalender",
        exist_ok=True
    )

    filename = os.path.join(
        "kalender",
        team["calendar"]
    )

    print(
        f"Schreibe Datei: {filename}"
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.writelines(cal)
    with open(
            filename,
            "r",
            encoding="utf-8"
        ) as f:

        content = f.read()

    for m in matches:

        local_dt = datetime.strptime(
            f"{m['date']} {m['time']}",
            "%Y-%m-%d %H:%M"
        )

        berlin_dt = local_dt.replace(
            tzinfo=ZoneInfo("Europe/Berlin")
        )

        utc_dt = berlin_dt.astimezone(
            ZoneInfo("UTC")
        )

        old_value = utc_dt.strftime(
            "DTSTART:%Y%m%dT%H%M%SZ"
        )

        new_value = local_dt.strftime(
            "DTSTART:%Y%m%dT%H%M%S"
        )

        #content = content.replace(
        #    "Z\r\n",
        #    "\r\n"
        #)

        #content = content.replace(
        #    old_value,
        #    new_value
        #)

        #import re

        #content = re.sub(
        #    r"(DTSTART:\d{8}T\d{6})Z",
        #    r"\1",
        #    content
        #)

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(content)
    print(
        f"Datei geschrieben: "
        f"{filename}"
    )

    print(
        f"Events im Kalender: "
        f"{added_events}"
    )


def main():

    print("====================================")
    print("TSV Kalender Generator gestartet")
    print("====================================")

    print(
        "Aktuelles Verzeichnis:"
    )

    print(os.getcwd())

    print(
        "Dateien im Root:"
    )

    print(os.listdir("."))

    if os.path.exists("config"):

        print(
            "Dateien in config:"
        )

        print(
            os.listdir("config")
        )

    teams = load_teams()

    print(
        f"Gefundene Teams: "
        f"{len(teams)}"
    )

    for team in teams:

        print(
            "\n============================"
        )

        print(
            f"Team: {team['name']}"
        )

        print(
            f"Kalender: "
            f"{team['calendar']}"
        )

        print(
            f"Team-ID: "
            f"{team['team_id']}"
        )

        print(
            "============================"
        )

        try:

            matches = fetch_team_matches(
                team["team_id"]
            )

            print(
                f"{len(matches)} "
                f"Spiele gefunden"
            )

            create_calendar(
                team,
                matches
            )

        except Exception as e:

            print(
                "FEHLER BEI TEAM:"
            )

            print(
                team["name"]
            )

            print(str(e))

    print("\nFertig.")


if __name__ == "__main__":
    main()
