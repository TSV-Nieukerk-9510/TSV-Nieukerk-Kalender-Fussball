import json
import os

import qrcode


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


def generate_qr_codes():

    teams = load_teams()

    os.makedirs(
        "qr",
        exist_ok=True
    )

    for team in teams:

        calendar_file = team["calendar"]

        url = build_calendar_url(
            calendar_file
        )

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4
        )

        qr.add_data(url)
        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white"
        )

        output_file = os.path.join(
            "qr",
            calendar_file.replace(
                ".ics",
                ".png"
            )
        )

        image.save(
            output_file
        )

        print(
            f"QR-Code erstellt: "
            f"{output_file}"
        )

    print()
    print(
        f"{len(teams)} QR-Codes erzeugt."
    )


if __name__ == "__main__":
    generate_qr_codes()
