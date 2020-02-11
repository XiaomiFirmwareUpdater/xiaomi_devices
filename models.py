#!/usr/bin/env python3.7
"""Xiaomi Devices Models Info scrapper"""

import re
import json
from requests import get

DEVICES = {}


def main():
    """
    scrapes Xiaomi devices md into json
    """
    data = get("https://raw.githubusercontent.com/KHwang9883/MobileModels/" +
               "master/brands/xiaomi_en.md").text
    data = [i for i in data.splitlines() if not str(i).startswith('#') and i]
    data = '\n'.join(data).replace('\n\n', '\n').replace('\n\n', '\n')
    devices = re.findall(r"\*(?:[\s\S]*?)\n\*|\*(?:[\s\S]*?)\Z", data, re.MULTILINE)
    for item in devices:
        info = {}
        details = item.split('*')
        details = [i for i in details if i]
        try:
            codename = details[0].split('(`')[1].split('`)')[0].strip()
        except IndexError:
            codename = ''
        try:
            internal = details[0].split('[`')[1].split('`]')[0].strip()
        except IndexError:
            internal = ''
        try:
            name = details[0].split(']')[1].split('(')[0].strip()
        except IndexError:
            name = details[0].split(':')[0].strip()
        models = details[1].replace('\n\n', '\n').strip().splitlines()
        info.update({"internal_name": internal})
        info.update({"name": name})
        models_ = {}
        for i in models:
            model = i.split(':')[0].strip()
            model_name = i.split(':')[1].strip()
            models_.update({model: model_name})
        info.update({"models": models_})
        try:
            if DEVICES[codename]:
                DEVICES[codename]['internal_name'] = f"{DEVICES[codename]['internal_name']}/{internal}" \
                    if DEVICES[codename]['internal_name'] != internal else internal
                DEVICES[codename]['name'] = f"{DEVICES[codename]['name']}/{name}"
                DEVICES[codename]['models'] = {**DEVICES[codename]['models'], **models_}
        except KeyError:
            DEVICES.update({codename: info})
    with open('models.json', 'w') as output:
        json.dump(DEVICES, output, indent=1)


if __name__ == '__main__':
    main()
