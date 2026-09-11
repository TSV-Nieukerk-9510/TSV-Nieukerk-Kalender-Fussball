# scripts/generate_calendars.py

import os
from datetime import datetime
from ics import Calendar, Event
from scripts.fetch_matches import fetch_team_matches


def is_valid_date(date_str):
    """Prüft, ob ein Datum im Format YYYY-MM-DD ist."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False


def create_calendar(team_name, matches):
    cal = Calendar()

    for m in matches:
        # Spiele ohne gültiges Datum überspringen
        if not is_valid_date(m["date"]):
            print(f"  → Spiel übersprungen (ungültiges Datum): {m['home']} vs {m['away']}")
            continue

        event = Event()
        event.name = f"{m['home']} vs {m['away']}"
        event.begin = f"{m['date']} {m['time']}"
        event.location = f"{m['location']} ({m['pitch']})"
        cal.events.add(event)

    os.makedirs("kalender", exist_ok=True)
    filename = os.path.join("kalender", f"{team_name}.ics")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(cal))


def main():
    teams = {
        "TSV Nieukerk":
            "https://www.fussball.de/mannschaft/tsv-nieukerk-tsv-nieukerk-niederrhein/-/saison/2627/team-id/011MI9ICMK000000VTVG0001VTR8C1K7"
    }

    print(f"Gefundene Teams: {len(teams)}")

    for team_name, team_url in teams.items():
        print(f"→ Lade Spiele für {team_name}")
        matches = fetch_team_matches(team_url)
        print(f"  {len(matches)} Spiele gefunden")

        create_calendar(team_name, matches)


if __name__ == "__main__":
    main()
