#!/usr/bin/env python3.7
"""Xiaomi AER Devices"""

import json
from requests import post
from pathlib import Path


def main():
    """
    Scrap Xiaomi AER devices generate JSON file
    """
    headers = {
        "authority": "trust.mi.com",
        "origin": "https://trust.mi.com",
        "referer": "https://trust.mi.com/misrc/updates/phone?tab=aerdata",
    }

    json_data = {
        "orderBy": True,
        "status": 1,
    }

    data = post(
        "https://trust.mi.com/bff/aer-certifications/findAll",
        headers=headers,
        json=json_data,
    ).json()

    Path("aer.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
