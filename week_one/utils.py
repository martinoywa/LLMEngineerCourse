import json
import re


def extract_json(text: str) -> dict:
    # Remove Markdown code fences if present
    text = re.sub(r"^```(?:json)?\s*", "", text.strip())
    text = re.sub(r"\s*```$", "", text)
    return json.loads(text)
