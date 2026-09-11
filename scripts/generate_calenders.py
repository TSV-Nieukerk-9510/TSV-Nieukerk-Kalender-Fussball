from ics import Calendar, Event
from scripts.fetch_matches import fetch_team_matches
import os

TEAM_URLS = {
    "u17": "https://www.fussball.de/team/u17-tsv-nieukerk/-/id/123/",
    "u15": "https://www.fussball.de/team/u15-tsv-nieukerk/-/id/456/",
}

OUTPUT_DIR = "kalender"

def create_calendar(team_name, matches):
    cal = Calendar()

    for m in matches:
        event = Event()
        event.name = f"{m['home']} – {m['away']} {m['pitch']}"
        event.begin = f"{m['date']} {m['time']}"
        event.location = m["location"]
        cal.events.add(event)

    with open(os.path.join(OUTPUT_DIR, f"{team_name}.ics"), "w") as f:
        f.write(str(cal))

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for team, url in TEAM_URLS.items():
        matches = fetch_team_matches(url)
        create_calendar(team, matches)

if __name__ == "__main__":
    main()
