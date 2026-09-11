import os
import requests
from bs4 import BeautifulSoup
from ics import Calendar, Event
from scripts.fetch_matches import fetch_team_matches

CLUB_URL = "https://www.fussball.de/verein/tsv-nieukerk-tsv-nieukerk-niederrhein/-/id/00ES8GN2HC000000VV0AG08LVUPGND5I"
OUTPUT_DIR = "kalender"


# Platzkürzel automatisch erkennen
def detect_pitch_short(location_text):
    text = location_text.lower()

    if "kunstrasen" in text:
        return "(Kunstrasen)"
    if "rasen" in text or "naturrasen" in text:
        return "(Naturrasen)"

    return ""


# Mannschaften automatisch auslesen
def get_all_team_urls():
    response = requests.get(CLUB_URL)
    soup = BeautifulSoup(response.text, "lxml")

    teams = {}

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/team/" in href:
            team_name = a.get_text(strip=True)
            team_url = "https://www.fussball.de" + href
            teams[team_name] = team_url

    return teams


# ICS erzeugen
def create_calendar(team_name, matches):
    cal = Calendar()

    for m in matches:
        pitch_short = detect_pitch_short(m["location"])

        event = Event()
        event.name = f"{team_name}: {m['home']} – {m['away']} {pitch_short}"
        event.begin = f"{m['date']} {m['time']}"
        event.location = m["location"]
        cal.events.add(event)

    filename = os.path.join(OUTPUT_DIR, f"{team_name}.ics")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(str(cal))


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Lese Mannschaften aus fussball.de …")
    team_urls = get_all_team_urls()

    print(f"{len(team_urls)} Mannschaften gefunden.\n")

    for team_name, url in team_urls.items():
        print(f"Erzeuge Kalender für: {team_name}")
        matches = fetch_team_matches(url)
        create_calendar(team_name, matches)

    print("\nAlle Kalender wurden erfolgreich erzeugt.")


if __name__ == "__main__":
    main()