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

__doc__ = "微博热搜(auto)"


async def long_to_short(origin_url: str):
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


async def get_HotList(choice: str = "weibo"):
    "获取微博热搜"
    async with httpx.AsyncClient() as client:
        try:
            response = requests.get(url="https://tenapi.cn/resou/", timeout=10)
            text_to_dic = json.loads(response.text)
            data = text_to_dic["list"]
            content = "#实时微博热搜#\n"
            for i in range(0, 10):
                link = await long_to_short(data[i]["url"])
                content += str(i) + "." + data[i]["name"] + "\n" + link + "\n"
                time.sleep(random.randint(5, 8))

            action = Action(qq=jconfig.bot)
            await action.sendGroupText(773933325, content)
            time.sleep(5)
            await action.sendGroupText(331620093, content)
            time.sleep(5)
            await action.sendFriendText(jconfig.superAdmin, content)
            time.sleep(5)
            await action.sendFriendText(3093892740, content)
            # await action.close()
            logger.info("发送微博热搜！")

        except Exception as e:
            logger.info(e)
            logger.info("自动获取微博热搜失败！")
            return None


job1 = async_scheduler.add_job(get_HotList, "cron", hour=9, minute=5)

job2 = async_scheduler.add_job(get_HotList, "cron", hour=19, minute=0)
