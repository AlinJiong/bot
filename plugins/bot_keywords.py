import asyncio
import datetime
import time
import httpx
import requests
import json
import cpuinfo
import psutil
from botoy import S, ctx, mark_recv, logger
import asyncio

__doc__ = "发送 '二次元'"


def dog_diary():
    url = "https://v2.alapi.cn/api/dog"
    payload = "token=nZJjbVKX1guoU4I4&format=json"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.request("POST", url, data=payload, headers=headers)
    text_to_dic = json.loads(response.text)
    content = text_to_dic["data"]["content"]
    return content


# def getPicUrl():
#     headers = {
#         "User-Agent":
#         "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
#     }
#     response = requests.get(url="http://121.40.95.21/api/tu.php",
#                             headers=headers,
#                             timeout=10)
#     if response.status_code != 200:
#         logger.info("获取美腿图片异常")
#         return None

#     else:
#         """坑爹玩意，找了一下午"""
#         return response.text.replace("\n", "")


async def get_Tuwei():
    url = "https://v2.alapi.cn/api/qinghua"
    payload = "token=nZJjbVKX1guoU4I4&format=json"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url,
                                         data=payload,
                                         headers=headers,
                                         timeout=10)
            text_to_dic = json.loads(response.text)

            return text_to_dic["data"]["content"]
        except:
            return None


async def main():
    if m := (ctx.group_msg or ctx.friend_msg):
        if m.text == "二次元":
            await S.image(data="http://121.40.95.21/api/tu.php")
        # elif m.text == "看看腿":
        #     await S.image(data=getPicUrl())
        elif m.text == "舔狗日记":
            await S.text(dog_diary())
        elif m.text == "土味情话":
            await S.text(await get_Tuwei())
        elif m.text == "帮助":
            await S.text(
                """#二次元#\n#舔狗日记#\n#摸鱼提醒 auto#\n#微博热搜 auto\#n#早报 auto#""")


mark_recv(main, author="alinjiong", name="关键字", usage="发送二次元、看看腿、舔狗日记")
