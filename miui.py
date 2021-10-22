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
    data = yaml.load(get(
        "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master/data/latest.yml").text, Loader=yaml.FullLoader)
    info = {}
    for i in data:
        if i['branch'] != "Weekly" and i['method'] == "Recovery":
            codename = i['codename']
            version = i['version']
            miui_code = version.split('.')[-1][1:5]
            info.update({codename: miui_code})
    sorted_data = OrderedDict(sorted(info.items()))
    with open('miui.json', 'w') as output:
        json.dump(sorted_data, output, indent=1)


if __name__ == '__main__':
    main()
