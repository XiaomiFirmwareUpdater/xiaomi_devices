#!/usr/bin/env python3.7
"""Xiaomi Devices names"""

import json
import yaml
from collections import OrderedDict
from requests import get

DEVICES = {}


def master():
    """
    extract names form master branch list
    """
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +\
          'xiaomi_devices/master/devices.json'
    data = get(url).json()
    for key, value in data.items():
        if not key:
            continue
        if value['display_name_en']:
            DEVICES.update({key: value['display_name_en']})
        else:
            DEVICES.update({key: value['display_name']})


def models():
    """
    extract names form models list
    """
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +\
          'xiaomi_devices/models/models.json'
    data = get(url).json()
    for codename, info in data.items():
        if not codename:
            continue
        DEVICES.update({codename: info['name']})


def gplay():
    """
    extract names form Google Play list
    """
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +\
          'xiaomi_devices/gplay/devices.json'
    data = get(url).json()
    for i in data:
        for key, value in i.items():
            if not key:
                continue
            DEVICES.update({key: value['name']})


def tracker():
    """
    extract codenames form my tracker
    """
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' \
          'miui-updates-tracker/master/data/devices.yml'
    data = yaml.load(get(url).text, Loader=yaml.FullLoader)
    for codename, info in data.items():
        DEVICES.update({codename: info[0]})


def main():
    """
    Generate json file of Xiaomi devices codename form various sources
    """
    gplay()
    master()
    models()
    tracker()
    data = OrderedDict(sorted(DEVICES.items()))
    with open('names.json', 'w') as out:
        json.dump(data, out, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
