#!/usr/bin/env python3.7
"""Xiaomi Devices Info Scrapper"""

import json
import re
from bs4 import BeautifulSoup
from requests import get

LINKS = []
ALL = []
CODENAME = ''


def get_codename(name):
    """
    Get the codename of a device using its name
    :param name: Device's name
    :return: codename
    """
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +\
          'xiaomi_devices/models/models.json'
    devices = get(url).json()
    global CODENAME
    alt_name = ''
    if '(' in name:
        alt_name = name.split('(')[1].split(')')[0].strip().lower()
        name = name.replace('Xiaomi', '').split('(')[0].strip().lower()
    else:
        name = name.replace('Xiaomi', '').strip().lower()
    # a workaround for poco devices
    if 'pocophone' in name.lower():
        name = name.replace('pocophone', 'poco')
    # a workaround for some devices
    if 'redmi 5 plus' in alt_name:
        CODENAME = 'vince'
        return CODENAME
    elif 'redmi note 5 ai' in name:
        CODENAME = 'whyred'
        return CODENAME
    elif name == 'redmi note':
        CODENAME = 'lcsh92_wet_gb9'
        return CODENAME
    elif name == 'redmi 4 (4x)':
        CODENAME = 'santoni'
        return CODENAME
    elif name == 'redmi note 3' and not alt_name:
        CODENAME = 'kenzo'
        return CODENAME
    elif name == 'redmi note 4' and not alt_name:
        CODENAME = 'mido'
        return CODENAME
    elif name == 'redmi note 7':
        CODENAME = 'lavender'
        return CODENAME
    if re.match(r'^[a-zA-Z]*\s[a-zA-Z]*\s[0-9]$', name):  # Match exact device for main models
        try:
            CODENAME = [i['codename'] for i in devices if name == str(i['name']).lower()][0]
        except IndexError:
            CODENAME = ''
    else:
        try:
            CODENAME = [i['codename'] for i in devices if name in str(i['models']).lower()][0]
        except IndexError:
            CODENAME = ''
    return CODENAME


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
                feature = th.text
            for td in tr.findAll("td", {"class": "ttl"}):
                header = td.text
                if header == '\u00a0':
                    header = 'info'
            for td in tr.findAll("td", {"class": "nfo"}):
                detail = td.text
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
    with open('devices.json', 'w') as output:
        json.dump(ALL, output, indent=1, ensure_ascii=False)


if __name__ == '__main__':
    main()
