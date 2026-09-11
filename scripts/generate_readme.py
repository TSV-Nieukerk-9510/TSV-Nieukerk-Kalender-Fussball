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


def build_qr_url(filename):

    return (
        f"https://raw.githubusercontent.com/"
        f"{GITHUB_ORG}/"
        f"{REPOSITORY}/main/"
        f"qr/{filename.replace('.ics', '.png')}"
    )


def generate_readme():

    teams = load_teams()

    content = []

    content.append(
        "# TSV Nieukerk Fußballkalender"
    )

    content.append("")
    content.append(
        "Automatisch erzeugte Kalender für alle Mannschaften des TSV Nieukerk."
    )
    content.append("")
    content.append(
        "Die Kalender können in Outlook, Apple Kalender, Google Kalender oder anderen Kalender-Apps abonniert werden."
    )
    content.append("")
    content.append("---")
    content.append("")

    for team in sorted(
        teams,
        key=lambda x: x["name"]
    ):

        calendar_url = build_calendar_url(
            team["calendar"]
        )

        qr_url = build_qr_url(
            team["calendar"]
        )

        content.append(
            f"## {team['name']}"
        )

        content.append("")

        content.append(
            f"**Kalenderdatei:** `{team['calendar']}`"
        )

        content.append("")

        content.append(
            f"📅 **Kalender abonnieren:**"
        )

        content.append("")

        content.append(
            calendar_url
        )

        content.append("")

        content.append(
            f"⚽ **Mannschaftsseite:**"
        )

        content.append("")

        content.append(
            team["url"]
        )

        content.append("")

        content.append(
            f"📱 **QR-Code:**"
        )

        content.append("")

        content.append(
            f"{qr_url}"
        )

        content.append("")

        content.append("---")
        content.append("")

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
