import asyncio
import datetime
import time

import cpuinfo
import psutil
from botoy import S, ctx, mark_recv, logger
import asyncio
import requests
import json

__doc__ = "发送早报"


async def get_news():
    url = 'http://dwz.2xb.cn/zaob'
    content = requests.get(url)
    text_to_dic = json.loads(content.text)
    img_url = text_to_dic['imageUrl']
    if text_to_dic['code'] != 200:
        return None
    return img_url


async def main():
    if m := (ctx.group_msg or ctx.friend_msg):
        if m.text == "早报":
            url = await get_news()
            await S.image(data=url, text="#今日早报#")


mark_recv(main, author='alinjiong', name="早报", usage='发送早报')
