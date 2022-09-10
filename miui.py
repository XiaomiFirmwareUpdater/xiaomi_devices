#!/usr/bin/env python3.7
"""Xiaomi MIUI Downloads Devices Info Scraper"""

import json
from bs4 import BeautifulSoup
from requests import get


def china_devices():
    """
    Extract devices json from MIUI downloads page
    :param url: MIUI downloads page
    """
    response = get("http://www.miui.com/download.html")
    page = BeautifulSoup(response.content, "html.parser")
    data = page.select("script")
    data = (
        [str(i) for i in data if "var phones" in str(i)][0].split("=")[1].split(";")[0]
    )
    info = json.loads(data)
    sorted_info = sorted(info, key=lambda k: k["pid"], reverse=True)
    with open("china.json", "w") as output:
        json.dump(sorted_info, output, indent=1, ensure_ascii=False)


def global_devices():
    """
    fetch MIUI downloads devices
    """
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Origin": "https://new.c.mi.com",
        "Referer": "https://new.c.mi.com/",
    }

    url = "https://sgp-api.buy.mi.com/bbs/api/global/phone/getphonelist"
    data = get(url, headers=headers).json()["data"]["phone_data"]["phone_list"]
    unified = []
    for item in data:
        if "http://" in item["pic_url"]:
            item["pic_url"] = item["pic_url"].replace("http://", "https://")
        unified.append(data)
    with open("c_mi.json", "w") as output:
        json.dump(data, output, indent=1, ensure_ascii=False)


def china_fastboot():
    """fetch MIUI china fastboot rom devices"""
    page = BeautifulSoup(
        get(
            "https://www.miui.com/shuaji-393.html",
            headers={
                "User-Agent": "Mozilla/5.0 (Linux; U; Android 10; zh-cn; M2007J1SC Build/QKQ1.200419.002) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/12.8.25"
            },
        ).content,
        "html.parser",
    )
    links = [
        f"{i['href'].split('=')[1].split('&')[0].strip()} - {i['href'].split('=')[2].split('&')[0]}"
        for i in page.findAll("a")
        if "fullromdownload" in str(i)
    ]
    with open("chinese_fastboot.txt", "w") as output:
        output.writelines(i + "\n" for i in sorted(links))


def global_fastboot():
    """fetch MIUI global fastboot rom devices"""
    data = get(
        "https://sgp-api.buy.mi.com/bbs/api/global/phone/getlinepackagelist"
    ).json()["data"]
    links = [
        f'{"_".join(i["key"].split("_")[:-2])} - {i["key"].split("_")[-1]}'
        for i in data
    ]
    with open("global_fastboot.txt", "w") as output:
        output.writelines(i + "\n" for i in sorted(links))


def main():
    """
    Scrap Xiaomi devices downloads info from official site and generate JSON files
    """
    # china_devices()
    global_devices()
    # china_fastboot()
    global_fastboot()


if __name__ == "__main__":
    main()
