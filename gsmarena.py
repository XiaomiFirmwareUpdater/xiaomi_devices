#!/usr/bin/env python3.7
"""Xiaomi Devices Info Scrapper"""

import json
import re
from time import sleep
from bs4 import BeautifulSoup
from requests import get

LINKS = []
ALL = []


def get_codename(name):
    """
    Get the codename of a device using its name
    :param name: Device's name
    :return: codename
    """
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' + \
          'xiaomi_devices/models/models.json'
    devices = get(url).json()
    alt_name = ''
    if '(' in name:
        alt_name = name.split('(')[1].split(')')[0].strip().lower()
        name = name.replace('Xiaomi', '').split('(')[0].strip().lower()
    else:
        name = name.replace('Xiaomi', '').strip().lower()
    print(name)
    # a workaround for poco devices
    if 'pocophone' in name.lower():
        name = name.replace('pocophone', 'poco')
    # a workaround for some devices
    if 'redmi 5 plus' in alt_name:
        return 'vince'
    if 'redmi note 5 ai' in name:
        return 'whyred'
    if name == 'redmi note':
        return 'lcsh92_wet_gb9'
    if name == 'redmi 4 (4x)':
        return 'santoni'
    if name == 'redmi note 3' and not alt_name:
        return 'kenzo'
    if name == 'redmi note 4' and not alt_name:
        return 'mido'
    if name == 'redmi note 7':
        device_codename = 'lavender'
        return device_codename
    if name == 'redmi k30':
        return 'phoenix'
    if name == 'poco X2':
        return 'phoenixin'
    if name == 'mi mix alpha':
        return 'draco'
    if 'cc9' in name:
        name = name.replace('cc9', 'cc 9')
        print(name)
    try:
        device_codename = [codename for codename, info in devices.items()
                           if name.lower() == info['name'].lower()][0]
    except IndexError:
        try:
            device_codename = [codename for codename, info in devices.items() if name in str(info['models']).lower()][0]
        except IndexError:
            try:
                device_codename = [codename for codename, info in devices.items()
                                   if name.startswith(info['name'].split('/')[1].lower())][0]
            except IndexError:
                try:
                    device_codename = [codename for codename, info in devices.items()
                                       if info['name'].lower().startswith(name.lower())][0]
                except IndexError:
                    device_codename = ''
    print(device_codename)
    return device_codename


def scrap_info(url):
    """
    Scrap device info from gsmarena paga and generate JSON
    :param url: gsmarena device specs url
    """
    response = get(url)
    page = BeautifulSoup(response.content, 'html.parser')
    data = page.findAll("table", {"cellspacing": "0"})
    info = {}
    out = {}
    meta = list(page.findAll("script", {"language": "javascript"})[0].text.splitlines())
    name = [i for i in meta if 'ITEM_NAME' in i][0].split('"')[1]
    picture = [i for i in meta if 'ITEM_IMAGE' in i][0].split('"')[1]
    codename = get_codename(name)
    for table in data:
        features = []
        details = {}
        header = ''
        detail = ''
        feature = ''
        for tr in table.findAll("tr"):
            for th in tr.findAll("th"):
                feature = th.text.strip()
            for td in tr.findAll("td", {"class": "ttl"}):
                header = td.text.strip()
                if header == '\u00a0':
                    header = 'info'
            for td in tr.findAll("td", {"class": "nfo"}):
                detail = td.text.strip()
            details.update({header: detail})
        features.append(details)
        out.update({feature: features})
    info.update({'name': name})
    info.update({'codename': codename})
    info.update({'picture': picture})
    info.update({'url': url})
    info.update({'specs': out})
    name = name.replace(' ', '_')
    with open(f'all/{name}.json', 'w') as output:
        json.dump(info, output, indent=1, ensure_ascii=False)
    ALL.append(info)


def extract_urls(url):
    """
    Extract devices specs URLs from brand page
    :param url: brand page
    :return: html page
    """
    response = get(url)
    page = BeautifulSoup(response.content, 'html.parser')
    devices = page.find("div", {"class": "makers"})
    for device in devices.findAll('li'):
        LINKS.append(f"https://www.gsmarena.com/{device.a['href']}")
    return page


def main():
    """
    Scrap every Xiaomi device info from gsmarena and generate JSON files
    """
    xiaomi = 'https://www.gsmarena.com/xiaomi-phones-80.php'
    page = extract_urls(xiaomi)
    next_pages = []
    for next_page in page.find("div", {"class": "nav-pages"}).findAll("a"):
        next_pages.append(f"https://www.gsmarena.com/{next_page['href']}")
    for page in next_pages:
        extract_urls(page)
    for device in LINKS:
        print(f'Fetching: {device}')
        scrap_info(device)
        sleep(25)
    with open('devices.json', 'w') as output:
        json.dump(ALL, output, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
