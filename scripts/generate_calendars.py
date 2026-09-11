# scripts/generate_calendars.py

import os
from datetime import datetime
from ics import Calendar, Event

from scripts.fetch_matches import fetch_team_matches


def is_valid_date(date_str):
    """Prüft, ob ein Datum YYYY-MM-DD ist."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except Exception:
        return False


def create_calendar(team_name, matches):

    print(f"\nErzeuge Kalender für {team_name}")

    cal = Calendar()
    added_events = 0

    for m in matches:

        print("Prüfe Spiel:", m)

        if not is_valid_date(m["date"]):
            print(
                f"Übersprungen (ungültiges Datum): "
                f"{m['home']} vs {m['away']} | {m['date']}"
            )
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

            location = m.get("location", "")

            if m.get("pitch"):
                location = (
                    f"{location} ({m['pitch']})"
                )

            if location:
                event.location = location

            description_parts = []

            if m.get("competition"):
                description_parts.append(
                    f"Wettbewerb: {m['competition']}"
                )

            if m.get("url"):
                description_parts.append(
                    f"Spieldetails: {m['url']}"
                )

            if description_parts:
                event.description = "\n".join(
                    description_parts
                )

            cal.events.add(event)

            added_events += 1

        except Exception as e:

            print(
                "Fehler beim Erzeugen des Events:"
            )
            print(e)

    os.makedirs("kalender", exist_ok=True)

    filename = os.path.join(
        "kalender",
        f"{team_name}.ics"
    )

    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(cal)

    print(f"Datei geschrieben: {filename}")
    print(f"Events im Kalender: {added_events}")


def main():

    print("====================================")
    print("TSV Kalender Generator gestartet")
    print("====================================")

    teams = {
        "TSV Nieukerk":
        "https://www.fussball.de/mannschaft/tsv-nieukerk-tsv-nieukerk-niederrhein/-/saison/2627/team-id/011MI9ICMK000000VTVG0001VTR8C1K7#!/",

        "TSV Nieukerk Senioren":
        "https://www.fussball.de/mannschaft/tsv-nieukerk-tsv-nieukerk-niederrhein/-/saison/2627/team-id/011MIDHQJ0000000VTVG0001VTR8C1K7#!/"
    }

    print(f"Gefundene Teams: {len(teams)}")

    for team_name, team_url in teams.items():

        print("\n------------------------------------")
        print(f"Team: {team_name}")
        print(f"URL: {team_url}")
        print("------------------------------------")

        try:

            print("Rufe fetch_team_matches auf...")

            matches = fetch_team_matches(
                team_url
            )

            print(
                f"fetch_team_matches liefert "
                f"{len(matches)} Spiele"
            )

            if len(matches) == 0:
                print(
                    "WARNUNG: Keine Spiele gefunden!"
                )

            for m in matches[:10]:
                print(m)

            create_calendar(
                team_name,
                matches
            )

        except Exception as e:

            print("\nFEHLER BEI TEAM:")
            print(team_name)
            print(str(e))

    print("\nFertig.")


if __name__ == "__main__":
    main()
