import json


GITHUB_ORG = "TSV-Nieukerk-9510"
REPOSITORY = "TSV-Nieukerk-Kalender-Fussball"


def load_teams():

    with open(
        "config/teams.json",
        "r",
        encoding="utf-8"
    ) as f:

        return json.load(f)


def build_calendar_url(filename):

    return (
        f"https://raw.githubusercontent.com/"
        f"{GITHUB_ORG}/"
        f"{REPOSITORY}/main/"
        f"kalender/{filename}"
    )


def generate_readme():

    teams = load_teams()

    content = []

    content.append(
        "# TSV Nieukerk Fußballkalender\n"
    )

    content.append(
        "Automatisch erzeugte Kalender für alle Mannschaften.\n"
    )

    content.append(
        "Die Kalender können direkt in Outlook, Apple Kalender oder Google Kalender abonniert werden.\n"
    )

    content.append("---\n")

    for team in sorted(
        teams,
        key=lambda x: x["name"]
    ):

        calendar_url = build_calendar_url(
            team["calendar"]
        )

        content.append(
            f"## {team['name']}\n"
        )

        content.append(
            f"**Kalenderdatei:** "
            f"`{team['calendar']}`\n"
        )

        content.append(
            f"📅 Kalender abonnieren:\n\n"
            f"{calendar_url}\n"
        )

        content.append(
            f"⚽ Mannschaftsseite:\n\n"
            f"{team['url']}\n"
        )

        content.append("\n---\n")

    with open(
        "README.md",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(content)
        )

    print(
        "README.md wurde erzeugt."
    )


if __name__ == "__main__":
    generate_readme()
