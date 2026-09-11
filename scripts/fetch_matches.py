import requests
from bs4 import BeautifulSoup
from .utils import clean_text, detect_pitch

def fetch_team_matches(team_url):
    response = requests.get(team_url)
    soup = BeautifulSoup(response.text, "lxml")

    matches = []

    for game in soup.select(".match-row"):
        home = clean_text(game.select_one(".home-team").text)
        away = clean_text(game.select_one(".away-team").text)
        date = clean_text(game.select_one(".match-date").text)
        time = clean_text(game.select_one(".match-time").text)
        location = clean_text(game.select_one(".match-location").text)

        pitch = detect_pitch(location)

        matches.append({
            "home": home,
            "away": away,
            "date": date,
            "time": time,
            "location": location,
            "pitch": pitch
        })

    return matches
