from botoy._internal.schedule import async_scheduler
import time
from botoy import logger
import json
from botoy import jconfig, logger
import requests

from botoy import Action


__doc__ = "早报（auto)"


async def get_news():
    url = 'http://dwz.2xb.cn/zaob'
    content = requests.get(url)
    text_to_dic = json.loads(content.text)
    img_url = text_to_dic['imageUrl']
    if text_to_dic['code'] != 200:
        return None
    return img_url


async def send_news():
    img = await get_news()
    if img == None:
        return

    action = Action(qq=jconfig.qq)
    groups_tmp = await action.getGroupList()

    groups = []
    for group in groups_tmp:
        groups.append(group['GroupCode'])

    groups.remove(953219612)

    for group in groups:
        await action.sendGroupPic(group, text="#今日早报#", url=img)
        time.sleep(3)
        logger.info("发送"+str(group)+"早报成功！")

    await action.sendFriendPic(jconfig.superAdmin, text="#今日早报#", url=img)
    await action.sendFriendPic(3093892740, text="#今日早报#", url=img)
    await action.close()

    logger.info("发送早报成功！")


job1 = async_scheduler.add_job(send_news, 'cron', hour=9, minute=0)
