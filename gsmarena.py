#!/usr/bin/env python3.7
"""Xiaomi Devices Info Scrapper"""

import json
from bs4 import BeautifulSoup
from requests import get

LINKS = []
ALL = []


def get_codename(name):
    url = 'https://raw.githubusercontent.com/XiaomiFirmwareUpdater/' +\
          'xiaomi_devices/models/models.json'
    devices = get(url).json()
    name = ' '.join(name.split(' ')[1:])
    try:
        codename = [i['codename'] for i in devices if name in i['name']][0]
    except IndexError:
        codename = ''
    return codename


def scrap_info(url):
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
    info.update({'specs': out})
    name = name.replace(' ', '_')
    with open(f'all/{name}.json', 'w') as output:
        json.dump(info, output, indent=1)
    ALL.append(info)


def extract_urls(url):
    response = get(url)
    page = BeautifulSoup(response.content, 'html.parser')
    devices = page.find("div", {"class": "makers"})
    for device in devices.findAll('li'):
        LINKS.append(f"https://www.gsmarena.com/{device.a['href']}")
    return page


def main():
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
        json.dump(ALL, output, indent=1)


if __name__ == '__main__':
    main()
