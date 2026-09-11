def create_calendar(team, matches):

    team_name = team["name"]

    print(
        f"\nErzeuge Kalender für "
        f"{team_name}"
    )

    cal = Calendar()

    added_events = 0

    for m in matches:

        if not is_valid_date(
            m["date"]
        ):
            continue

        try:

            event = Event()

            event.name = (
                f"{m['home']} vs {m['away']}"
            )

            dt = datetime.strptime(
                f"{m['date']} {m['time']}",
                "%Y-%m-%d %H:%M"
            )

            event.begin = dt

            event.uid = (
                f"{team['team_id']}-"
                f"{m['date']}-"
                f"{m['time']}-"
                f"{m['home']}-"
                f"{m['away']}"
            ).replace(" ", "_")

            description = []

            description.append(
                f"Mannschaft: {team['name']}"
            )

            description.append(
                f"Saison: {team['season']}"
            )

            if m.get("competition"):
                description.append(
                    f"Wettbewerb: {m['competition']}"
                )

            description.append(
                f"Mannschaftsseite: {team['url']}"
            )

            event.description = (
                "\n".join(description)
            )

            cal.events.add(event)

            added_events += 1

        except Exception as e:

            print(
                "Fehler beim Event:"
            )

            print(e)

    os.makedirs(
        "kalender",
        exist_ok=True
    )

    filename = os.path.join(
        "kalender",
        team["calendar"]
    )

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as f:

        f.writelines(cal)

    print(
        f"Datei geschrieben: "
        f"{filename}"
    )

    print(
        f"Events im Kalender: "
        f"{added_events}"
    )
