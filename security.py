#!/usr/bin/env python3.7
"""Xiaomi Android Security Patch Information"""

from datetime import datetime, timedelta
import json
from requests import get
from pathlib import Path


def main():
    """
    Scrap Android Security Patch Information and generate JSON file
    """
    previous_month = datetime.utcnow().replace(day=1) - timedelta(days=1)
    # months = ["two months ago", "last month", "this month", "next month"]
    months = [
        (previous_month.replace(day=1) - timedelta(days=1)).strftime("%Y%m"),
        previous_month.strftime("%Y%m"),
        datetime.utcnow().strftime("%Y%m"),
        (
            (datetime.utcnow().replace(day=1) + timedelta(days=32)).replace(day=1)
        ).strftime("%Y%m"),
    ]
    models_data = ""
    for item in months:
        data = get(
            f"https://trust.mi.com/bff/security-update-detail/synctime/{item}"
        ).json()
        if not data:
            continue
        Path(f"data/{item}.json").write_text(
            json.dumps(data, indent=1, ensure_ascii=False)
        )
        models_data = data["models"]
    Path("models.json").write_text(json.dumps(sorted(models_data.split(";")), indent=1))


if __name__ == "__main__":
    main()
