import json
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



def get_team_code(calendar_name):

    base = (
        calendar_name
        .replace(".ics", "")
    )

    parts = base.split("-")

    if len(parts) >= 2:
        return parts[-2]

    return base    


def get_pitch_code(match):

    location = (
        match.get("location", "")
        .lower()
    )

    pitch = (
        match.get("pitch", "")
        .lower()
    )

    text = f"{location} {pitch}"

    if "kunstrasen" in text:
        return "KR"

    if (
        "rasenplatz" in text
        or
        "naturrasen" in text
    ):
        return "NR"

    return "KZ"


def get_opponent(match, team):

    team_name = team["name"].lower()

    if (
        "tsv nieukerk"
        in match["home"].lower()
    ) or (
        "nieukerk"
        in match["home"].lower()
    ):
        return match["away"], True

    if (
        "tsv nieukerk"
        in match["away"].lower()
    ) or (
        "nieukerk"
        in match["away"].lower()
    ):
        return match["home"], False

    return match["away"], False


def create_event(team, match, mode):

    event = Event()

    team_code = get_team_code(
        team["calendar"]
    )

    pitch_code = get_pitch_code(
        match
    )

    opponent, is_home = get_opponent(
        match,
        team
    )

    competition = (
        match.get(
            "competition",
            ""
        )
        .lower()
    )

    is_festival = (
        "kinder"
        in competition
    )

    if mode == "team":

        if is_festival:
            title = "Kinderfestival"
        else:
            title = opponent

    elif mode == "summary":

        home_away = (
            "H"
            if is_home
            else "A"
        )

        if is_festival:
            title = (
                f"{home_away} - "
                f"{team_code} - "
                f"Kinderfestival"
            )
        else:
            title = (
                f"{home_away} - "
                f"{team_code} - "
                f"{opponent}"
            )

    elif mode == "pitch":

        if is_festival:

            title = (
                f"{team_code} - "
                f"Kinderfestival - "
                f"{pitch_code}"
            )

        else:

            title = (
                f"{team_code} - "
                f"{opponent} - "
                f"{pitch_code}"
            )

    else:
        title = opponent

    event.name = title

    dt = datetime.strptime(
        f"{match['date']} {match['time']}",
        "%Y-%m-%d %H:%M"
    )

    event.begin = dt

    description = []

    description.append(
        f"Mannschaft: {team['name']}"
    )

    description.append(
        f"Heimspiel: "
        f"{'Ja' if is_home else 'Nein'}"
    )

    description.append(
        f"Gegner: {opponent}"
    )

    if match.get("competition"):
        description.append(
            f"Wettbewerb: "
            f"{match['competition']}"
        )

    if match.get("location"):
        description.append(
            f"Spielort: "
            f"{match['location']}"
        )

    if pitch_code == "NR":
        description.append(
            "Platztyp: Naturrasen"
        )

    elif pitch_code == "KR":
        description.append(
            "Platztyp: Kunstrasen"
        )

    else:
        description.append(
            "Platztyp: Nicht angegeben"
        )

        description.append("")
        description.append(
            "⚠ Automatische Zuordnung"
        )
        description.append(
            "Keine Platzinformation auf fussball.de gefunden."
        )
        description.append(
            "Der Termin wurde dem Kunstrasen-Kalender zugeordnet."
        )

    event.description = "\n".join(
        description
    )

    if match.get("location"):
        event.location = (
            match["location"]
        )

    return event


def write_calendar(
    filename,
    events
):

    calendar = Calendar()

    for event in events:
        calendar.events.add(
            event
        )

    with open(
        f"kalender/{filename}",
        "w",
        encoding="utf-8"
    ) as f:

        f.writelines(calendar)

    print(
        f"{filename}: "
        f"{len(events)} Termine"
    )


def main():

    teams = load_teams()

    season = teams[0]["season"]

    all_events = []
    senior_events = []
    youth_events = []
    rasen_events = []
    kunst_events = []

    for team in teams:

        matches = fetch_team_matches(
            team["team_id"]
        )

        team_code = get_team_code(
            team["calendar"]
        )

        for match in matches:

            summary_event = create_event(
                team,
                match,
                "summary"
            )

            all_events.append(
                summary_event
            )

            if team_code in [
                "TSV-H1",
                "TSV-H2"
            ]:

                senior_events.append(
                    summary_event
                )

            else:

                youth_events.append(
                    summary_event
                )

            pitch_code = (
                get_pitch_code(match)
            )

            pitch_event = (
                create_event(
                    team,
                    match,
                    "pitch"
                )
            )

            if pitch_code == "NR":

                rasen_events.append(
                    pitch_event
                )

            else:

                kunst_events.append(
                    pitch_event
                )

    write_calendar(
        f"TSV-Alle-{season}.ics",
        all_events
    )

    write_calendar(
        f"TSV-Senioren-{season}.ics",
        senior_events
    )

    write_calendar(
        f"TSV-Jugend-{season}.ics",
        youth_events
    )

    write_calendar(
        f"TSV-Rasenplatz-{season}.ics",
        rasen_events
    )

    write_calendar(
        f"TSV-Kunstrasen-{season}.ics",
        kunst_events
    )


if __name__ == "__main__":
    main()
