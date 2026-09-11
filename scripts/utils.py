import re

def clean_text(text):
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()

def detect_pitch(location):
    if not location:
        return ""

    loc = location.lower()

    if "kunstrasen" in loc:
        return "(Kunstrasen)"
    if "rasen" in loc:
        return "(Naturrasen)"

    return ""
