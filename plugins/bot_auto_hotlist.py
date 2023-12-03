from random import random
import time
import requests
import json
from botoy import Action
import random
import httpx
from botoy._internal.schedule import async_scheduler
import time
from botoy import logger
import json
from botoy import jconfig, logger
import requests
import urllib
from typing import List

__doc__ = "微博热搜(auto)"


async def long_to_short_v0(origin_url: str):
    request_url = (
        "https://v2.alapi.cn/api/url?token=nZJjbVKX1guoU4I4&url="
        + origin_url
        + "&type=m6zcn"
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.request("GET", request_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return origin_url
        data = json.loads(response.text)
        return data["data"]["short_url"]
    except:
        return origin_url


async def long_to_short_v1(origin_url: str):
    origin_url = urllib.parse.quote(origin_url)  # 有时候长链接转短链接api显示url无效，需要加上这一条
    request_url = (
        "https://v2.alapi.cn/api/url?token=nZJjbVKX1guoU4I4&url="
        + origin_url
        + "&type=dwzmk"
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.request("GET", request_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return origin_url
        data = json.loads(response.text)
        return data["data"]["short_url"]
    except:
        return origin_url


async def long_to_short(origin_url: str):
    request_url = "https://www.lzfh.com/api/dwz.php?cb=1&sturl=8&longurl=" + origin_url
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.request("GET", request_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return origin_url
        data = json.loads(response.text)
        return data["dwz_url"]
    except:
        return origin_url


def get_hotlist() -> List[dict]:
    "获取微博热搜"
    res = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    }

    offcial_api = "https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot"

    response = requests.get(url=offcial_api, headers=headers)

    res_dict = json.loads(response.text)

    for i in range(10):
        title = res_dict["data"]["cards"][0]["card_group"][i]["desc"]
        url = "https://s.weibo.com/weibo?q=%23" + urllib.parse.quote(title) + "%23"
        res.append({"title": title, "url": url})

    return res


async def send_hotlist():
    "发送微博热搜"
    try:
        data = get_hotlist()
        content = "#实时微博热搜#\n"
        for i in range(0, 10):
            link = await long_to_short(data[i]["url"])
            content += str(i) + "." + data[i]["title"] + "\n" + link + "\n"
            time.sleep(random.randint(2, 4))

        content = content[:-1]
        action = Action(qq=jconfig.bot)
        await action.sendGroupText(773933325, content)
        time.sleep(5)
        await action.sendFriendText(jconfig.superAdmin, content)
        # await action.close()
        logger.info("发送微博热搜！")

    except Exception as e:
        logger.info(e)
        logger.info("自动获取微博热搜失败！")
        return None


job1 = async_scheduler.add_job(send_hotlist, "cron", hour=9, minute=5)

job2 = async_scheduler.add_job(send_hotlist, "cron", hour=19, minute=0)
