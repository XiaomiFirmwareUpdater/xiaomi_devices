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
    data = [i.text for i in data if "var phones" in i.text][0].split('=')[1].split(';')[0]
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


def global_devices():
    """
    fetch MIUI downloads devices
    """
    headers = {
        'pragma': 'no-cache',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cache-control': 'no-cache',
        'authority': 'c.mi.com',
        'x-requested-with': 'XMLHttpRequest',
        'referer': 'https://c.mi.com/oc/miuidownload/',
    }

    url = 'http://c.mi.com/oc/rom/getphonelist'
    data = get(url, headers=headers).json()['data']['phone_data']['phone_list']
    with open('c_mi.json', 'w') as output:
        json.dump(data, output, indent=1, ensure_ascii=False)


def fastboot(name, url):
    """fetch MIUI fastboot rom devices"""
    page = BeautifulSoup(get(url).content, 'html.parser')
    links = [f"{i['href'].split('=')[1].split('&')[0].strip()} - {i['href'].split('=')[2].split('&')[0]}"
             for i in page.findAll('a') if "fullromdownload" in str(i)]
    with open(f'{name}_fastboot.txt', 'w') as output:
        output.writelines(i + '\n' for i in sorted(links))


def main():
    """
    Scrap Xiaomi devices downloads info from official site and generate JSON files
    """
    urls = ['http://www.miui.com/download.html', 'http://en.miui.com/download.html']
    for url in urls:
        fetch(url)
    global_devices()
    fastboot_urls = {'global': 'https://en.miui.com/a-234.html',
                     'chinese': 'https://www.miui.com/shuaji-393.html'}
    for name, url in fastboot_urls.items():
        fastboot(name, url)


if __name__ == '__main__':
    main()
