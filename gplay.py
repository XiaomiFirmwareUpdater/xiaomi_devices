#!/usr/bin/env python3.7
"""Xiaomi Devices Info Scrapper"""

import json
from requests import get


def get_devices_list():
    """
    Download latest certified devices list
    """
    url = "https://raw.githubusercontent.com/androidtrackers/" + \
          "certified-android-devices/master/README.md"
    response = get(url)
    with open('devices.md', 'wb') as out:
        out.write(response.content)


def extract_info():
    """
    Extract Xiaomi devices info and write json file
    """
    with open('devices.md', 'r') as file:
        data = file.readlines()
    devices = []
    for line in data:
        info = {}
        details = {}
        if line.startswith('|Xiaomi|') or line.startswith('|Redmi|') or line.startswith('|POCO|'):
            name = line.split('|')[2]
            codename = line.split('|')[3]
            model = line.split('|')[4]
            details.update({'name': name})
            details.update({'model': model})
            info.update({codename: details})
            devices.append(info)
    with open('devices.json', 'w') as output:
        json.dump(devices, output, indent=1)


def main():
    """
    Make jsom file of Xiaomi devices info from Google Play certified devices list
    """
    get_devices_list()
    extract_info()


if __name__ == '__main__':
    main()
