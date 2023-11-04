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
    request_url = ("https://v2.alapi.cn/api/url?token=nZJjbVKX1guoU4I4&url=" +
                   origin_url + "&type=dwzmk")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    try:
        response = requests.request("GET",
                                    request_url,
                                    headers=headers,
                                    timeout=10)
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


async def get_HotList(choice: str = "weibo"):
    "获取微博热搜"
    try:
        response = requests.get(url="http://api.xtaoa.com/api/weibo.php", timeout=10)
        text_to_dic = json.loads(response.text)
        data = text_to_dic["data"]
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


job1 = async_scheduler.add_job(get_HotList, "cron", hour=9, minute=5)

job2 = async_scheduler.add_job(get_HotList, "cron", hour=19, minute=0)
