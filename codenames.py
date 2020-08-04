#!/usr/bin/env python3.7
"""Xiaomi Devices codenames"""

import json
import yaml
from requests import get

DEVICES = []


def master():
    """
    extract codenames form master branch list
    """
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +\
          'xiaomi_devices/master/devices.json'
    data = get(url).json()
    codenames = []
    for key in data.keys():
        codenames.append(key)
    for i in codenames:
        if i:
            DEVICES.append(i)


def models():
    """
    extract codenames form models list
    """
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +\
          'xiaomi_devices/models/models.json'
    data = get(url).json()
    codenames = list(data.keys())
    for i in codenames:
        if i:
            DEVICES.append(i)


def gplay():
    """
    extract codenames form Google Play list
    """
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +\
          'xiaomi_devices/gplay/devices.json'
    data = get(url).json()
    codenames = []
    for i in data:
        for key in i.keys():
            codenames.append(key)
    for i in codenames:
        if i:
            DEVICES.append(i)


def tracker():
    """
    extract codenames form my tracker
    """
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' \
          'miui-updates-tracker/master/data/devices.yml'
    data = yaml.load(get(url).text, Loader=yaml.FullLoader)
    for codename in data.keys():
        DEVICES.append(codename)


def main():
    """
    Generate json file of Xiaomi devices codename form various sources
    """
    gplay()
    models()
    master()
    tracker()
    data = list(dict.fromkeys(DEVICES))  # remove duplicates
    data.sort()  # sort
    with open('codenames.json', 'w') as out:
        json.dump(data, out, indent=1)


if __name__ == '__main__':
    main()
