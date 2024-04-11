#!/usr/bin/env python3.7
"""Xiaomi Devices Info Scrapper"""

import json
from requests import get, post

URL = 'https://script.google.com/macros/s/AKfycbxl1aIUEI7jHepwGV8MsBKOrFAAC6iF-9dUJvhF5kgGFeCR_Tjz8f9el94aFnYs4YjgwQ/exec'

def get_codename(name):
    """
    Get the codename of a device using its name
    :param name: Device's name
    :return: codename
    """
    device_codenames = DEVICES.get(name, [])
    print('Device codenames: ' + ', '.join(device_codenames))
    return device_codenames

def get_device_info(device):
    """
    Scrap device info from gsmarena page and generate JSON
    :param device: gsmarena device key
    :return: device info JSON
    """
    detail = {
        "route": "device-detail",
        "key": device
    }
    def parse_data(data):
        if len(data) == 0:
            return {}
        if isinstance(data[0], dict):
            result = {}
            for i in data:
                result[i['title']] = parse_data(i['data'])
            return result
        else:
            return data[0]
    data = post(URL, json=detail).json()['data']
    info = {}
    info.update({'name': data['device_name']})
    info.update({'picture': data['device_image']})
    info.update({'url': f"https://www.gsmarena.com/{device}.php"})
    info.update({'codenames': get_codename(info['name'])})
    info.update({'specs': parse_data(data['more_specification'])})
    name = info['name'].replace(' ', '_')
    with open(f'all/{name}.json', 'w') as output:
        json.dump(info, output, indent=1, ensure_ascii=False)
    return info


def main():
    """
    Scrap every Xiaomi device info from gsmarena and generate JSON files
    """
    global DEVICES
    with open("gsmarena_codenames.json") as file:
        DEVICES = json.loads(file.read())
    xiaomi = {
        "route": "device-list-by-brand",
        "brand_id": 80,
        "brand_name": "xiaomi",
        "page": 1
    }
    devices = []
    all_info = []
    problems = []
    for page in range(1, post(URL, json=xiaomi).json()['data']['total_page'] + 1):
        print(f'Fetching page №{page}')
        xiaomi['page'] = page
        for device in post(URL, json=xiaomi).json()['data']['device_list']:
            if 'Xiaomi ' + device['device_name'] in DEVICES.keys():
                devices.append(device)
            else:
                problems.append(device['device_name'])
    print()
    print("Couldn't find in gsmarena_codenames.json:")
    print('\n'.join(problems))
    for device in devices:
        print()
        print('Fetching: ' + device['device_name'])
        all_info.append(get_device_info(device['key']))
    with open('devices.json', 'w') as output:
        json.dump(all_info, output, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
