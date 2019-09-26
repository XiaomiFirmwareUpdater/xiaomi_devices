#!/usr/bin/env python3.7
"""Xiaomi MIUI codes Info Scraper"""

import json
import yaml
from collections import OrderedDict
from requests import get


def main():
    """
    Scrap Xiaomi devices MIUI codes and generate JSON files
    """
    current = yaml.load(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/" +
        "stable_fastboot/stable_fastboot.yml").text, Loader=yaml.CLoader)
    eol = yaml.load(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/EOL/" +
        "stable_fastboot/stable_fastboot.yml").text, Loader=yaml.CLoader)
    data = current + eol
    info = {}
    for i in data:
        codename = i['codename']
        version = i['version']
        miui_code = version.split('.')[-1][1:5]
        info.update({codename: miui_code})
    sorted_data = OrderedDict(sorted(info.items()))
    with open('miui.json', 'w') as output:
        json.dump(sorted_data, output, indent=1)


if __name__ == '__main__':
    main()
