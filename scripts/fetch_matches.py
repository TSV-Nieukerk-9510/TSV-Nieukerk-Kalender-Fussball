print("fetch_team_matches gestartet")
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_team_matches(team_url):
    """
    Universeller Parser für fussball.de Spielpläne.
    Funktioniert für:
    - Teamseiten
    - JSG-Teams
    - Jugendmannschaften
    - Staffel-/Spielplan-Seiten
    """

    resp = requests.get(team_url)
    # resp.raise_for_status()
    print("Status Code:", resp.status_code)
    if resp.status_code != 200:
        print(resp.text[:1000])
    resp.raise_for_status()
    ``
    soup = BeautifulSoup(resp.text, "lxml")

    matches = []

    # 1) Neue fussball.de Struktur (match-row)
    for row in soup.select("div.match-row, div.fixture-row, div.match"):
        home = row.select_one(".team-home, .home, .team-left")
        away = row.select_one(".team-away, .away, .team-right")
        date = row.select_one(".match-date, .date")
        time = row.select_one(".match-time, .time")
        location = row.select_one(".location, .match-location")

        if not home or not away or not date:
            continue

        home_team = home.get_text(strip=True)
        away_team = away.get_text(strip=True)

        date_text = date.get_text(strip=True)
        time_text = time.get_text(strip=True) if time else "00:00"
        location_text = location.get_text(strip=True) if location else ""

        # Datum normalisieren
        try:
            date_clean = "".join(ch for ch in date_text if ch.isdigit() or ch == ".")
            dt = datetime.strptime(date_clean, "%d.%m.%Y")
            date_iso = dt.strftime("%Y-%m-%d")
        except:
            date_iso = date_text

        # Uhrzeit normalisieren
        try:
            time_clean = time_text.strip()
            if len(time_clean) > 5:
                time_clean = time_clean[:5]
        except:
            time_clean = "00:00"

        # Platzkürzel
        lt = location_text.lower()
        if "kunstrasen" in lt:
            pitch = "Kunstrasen"
        elif "rasen" in lt or "naturrasen" in lt:
            pitch = "Naturrasen"
        else:
            pitch = ""

        matches.append({
            "home": home_team,
            "away": away_team,
            "date": date_iso,
            "time": time_clean,
            "location": location_text,
            "pitch": pitch
        })

    # 2) Fallback: alte Tabellenstruktur
    if not matches:
        for row in soup.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            home_team = cols[0].get_text(strip=True)
            away_team = cols[2].get_text(strip=True)
            date_text = cols[3].get_text(strip=True)
            time_text = cols[4].get_text(strip=True)

            location = ""
            extra_cols = cols[5:] if len(cols) > 5 else []
            for c in extra_cols:
                txt = c.get_text(" ", strip=True)
                if "Sportanlage" in txt or "Platz" in txt or "Stadion" in txt:
                    location = txt
                    break

            # Datum
            try:
                date_clean = "".join(ch for ch in date_text if ch.isdigit() or ch == ".")
                dt = datetime.strptime(date_clean, "%d.%m.%Y")
                date_iso = dt.strftime("%Y-%m-%d")
            except:
                date_iso = date_text

            # Uhrzeit
            try:
                time_clean = time_text.strip()
                if len(time_clean) > 5:
                    time_clean = time_clean[:5]
            except:
                time_clean = "00:00"

            # Platzkürzel
            lt = location.lower()
            if "kunstrasen" in lt:
                pitch = "Kunstrasen"
            elif "rasen" in lt or "naturrasen" in lt:
                pitch = "Naturrasen"
            else:
                pitch = ""

            matches.append({
                "home": home_team,
                "away": away_team,
                "date": date_iso,
                "time": time_clean,
                "location": location,
                "pitch": pitch
            })

    return matches
