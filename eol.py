#!/usr/bin/env python3.7
"""Xiaomi EOL Devices"""

import json
from requests import get
from pathlib import Path


def main():
    """
    Scrap Xiaomi eol devices generate JSON file
    """
    data = get(
        "https://trust.mi.com/bff/eos-products/phones?type=Xiaomi-Redmi-POCO"
    ).json()
    # sorted_data = sorted(
    #     data["phone"][0]["Xiaomi"]
    #     + data["phone"][1]["Redmi"]
    #     + data["phone"][2]["POCO"],
    #     key=lambda x: x["deviceName"],
    # )
    # devices = [i["deviceName"] for i in sorted_data]

    Path("eol.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
