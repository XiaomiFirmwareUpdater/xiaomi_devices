#!/usr/bin/env python3.7
"""Xiaomi MIUI Downloads Devices Info Scraper"""

import json
from bs4 import BeautifulSoup
from requests import get


def fetch(url):
    """
    Extract devices json from MIUI downloads page
    :param url: MIUI downloads page
    """
    response = get(url)
    page = BeautifulSoup(response.content, 'html.parser')
    data = page.findAll("script")
    data = [i for i in data if not i.attrs][0].text.split('=')[1].split(';')[0]
    info = json.loads(data)
    sorted_info = sorted(info, key=lambda k: k['pid'], reverse=True)
    if 'en.' in url:
        name = 'global'
    elif 'ru.' in url:
        name = 'russian'
    elif 'in.' in url:
        name = 'indian'
    else:
        name = 'china'
    with open(f'{name}.json', 'w') as output:
        json.dump(sorted_info, output, indent=1, ensure_ascii=False)


def main():
    """
    Scrap Xiaomi devices downloads info from official site and generate JSON files
    """
    urls = ['http://www.miui.com/download.html', 'http://en.miui.com/download.html',
            'http://ru.miui.com/download.html', 'http://in.miui.com/download.html']
    for url in urls:
        fetch(url)


if __name__ == '__main__':
    main()
