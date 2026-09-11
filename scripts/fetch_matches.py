import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_team_matches(team_url):
    """
    Lädt alle Spiele einer Mannschaft von fussball.de
    und gibt eine Liste von Dicts zurück:

    {
        "home": str,
        "away": str,
        "date": "YYYY-MM-DD",
        "time": "HH:MM",
        "location": str,
        "pitch": str
    }
    """

    resp = requests.get(team_url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "lxml")
    matches = []

    # fussball.de hat je nach Ansicht unterschiedliche Container,
    # hier ein generischer Ansatz über Tabellenzeilen
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        # Versuch, Heim / Gast / Datum / Uhrzeit / Ort zu erkennen
        home_team = cols[0].get_text(strip=True)
        away_team = cols[2].get_text(strip=True)
        date_text = cols[3].get_text(strip=True)
        time_text = cols[4].get_text(strip=True)

        # Ort / Platz (falls vorhanden)
        location = ""
        pitch = ""

        extra_cols = cols[5:] if len(cols) > 5 else []
        for c in extra_cols:
            txt = c.get_text(" ", strip=True)
            if "Sportanlage" in txt or "Platz" in txt or "Stadion" in txt:
                location = txt
                break

        # Platzkürzel aus Location ableiten
        lt = location.lower()
        if "kunstrasen" in lt:
            pitch = "Kunstrasen"
        elif "rasen" in lt or "naturrasen" in lt:
            pitch = "Naturrasen"
        else:
            pitch = ""

        # Datum normalisieren
        try:
            date_clean = "".join(ch for ch in date_text if ch.isdigit() or ch == ".")
            dt = datetime.strptime(date_clean, "%d.%m.%Y")
            date_iso = dt.strftime("%Y-%m-%d")
        except Exception:
            date_iso = date_text  # Fallback

        # Uhrzeit normalisieren
        try:
            time_clean = time_text.strip()
            if len(time_clean) > 5:
                time_clean = time_clean[:5]
        except Exception:
            time_clean = "00:00"

        matches.append(
            {
                "home": home_team,
                "away": away_team,
                "date": date_iso,
                "time": time_clean,
                "location": location,
                "pitch": pitch,
            }
        )

    return matches


if __name__ == "__main__":
    TEST_URL = "https://www.fussball.de/team/u15-tsv-nieukerk/-/id/123/"
    for m in fetch_team_matches(TEST_URL):
        print(m)