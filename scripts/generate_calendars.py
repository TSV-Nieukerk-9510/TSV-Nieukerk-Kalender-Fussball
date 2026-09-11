import json
import os
from datetime import datetime
from ics import Calendar, Event
from scripts.fetch_matches import fetch_team_matches

def load_teams():
    with open(
        "config/teams.json",
        "r",
        encoding="utf-8"
    ) as f:
        return json.load(f)

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
    team_name = team["name"]
    print(
        f"\nErzeuge Kalender für "
        f"{team_name}"
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

            event.begin = dt

            event.uid = (
                f"{team['team_id']}-"
                f"{m['date']}-"
                f"{m['time']}-"
                f"{m['home']}-"
                f"{m['away']}"
            ).replace(" ", "_")
            
            description = []

            description.append(
                f"Mannschaft: {team['name']}"
            )

            if m.get("competition"):
                description.append(
                    f"Wettbewerb: {m['competition']}"
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

            print(e)

    os.makedirs(
        "kalender",
        exist_ok=True
    )

    filename = os.path.join(
        "kalender",
        team["calendar"]
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.writelines(cal)

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

    teams = load_teams()

    print(
        f"Gefundene Teams: "
        f"{len(teams)}"
    )

    for team in teams:

        try:

            print("\n------------------------------------")
            print(
                f"Team: {team['name']}"
            )
            print(
                f"Team-ID: {team['team_id']}"
            )
            print("------------------------------------")

            matches = fetch_team_matches(
                team["team_id"]
            )

            print(
                f"{len(matches)} Spiele gefunden"
            )

            create_calendar(
                team,
                matches
            )

        except Exception as e:

            print(
                f"Fehler bei "
                f"{team['name']}"
            )

            print(str(e))

    print("\nFertig.")


if __name__ == "__main__":
    main()
