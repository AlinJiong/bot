from botoy._internal.schedule import async_scheduler
import time
from botoy import logger
import json
from botoy import jconfig, logger
import requests
import base64
from io import BytesIO
from botoy import Action

__doc__ = "早报（auto)"


# async def get_news():
#     url = "http://dwz.2xb.cn/zaob"
#     content = requests.get(url)
#     text_to_dic = json.loads(content.text)
#     img_url = text_to_dic["imageUrl"]
#     if text_to_dic["code"] != 200:
#         return None
#     return img_url


async def get_news():
    url = "https://api.jun.la/60s.php?format=imgapi"
    content = requests.get(url)
    text_to_dic = json.loads(content.text)
    if int(text_to_dic["code"]) != 200:
        return None
    return text_to_dic["imageBaidu"]


async def send_news():
    img_url = await get_news()
    if img_url == None:
        return

    response = requests.get(img_url)
    # 得到图片的base64编码
    img = base64.b64encode(response.content)
    
    img_base64 = img.decode('utf-8')
    
    

    action = Action(qq=jconfig.qq)
    groups_tmp = await action.getGroupList()

    groups = []
    for group in groups_tmp:
        groups.append(group["GroupCode"])

    groups.remove(953219612)

    for group in groups:
        await action.sendGroupPic(group, text="#今日早报#", base64=img_base64)
        time.sleep(3)
        logger.info("发送" + str(group) + "早报成功！")

    await action.sendFriendPic(jconfig.superAdmin, text="#今日早报#", base64=img_base64)
    logger.info("向好友 2311366525 发送早报!")
    time.sleep(10)
    await action.sendFriendPic(3093892740, text="#今日早报#", base64=img_base64)
    logger.info("向好友 3093892740  发送早报!")


job1 = async_scheduler.add_job(send_news, "cron", hour=9, minute=0)
