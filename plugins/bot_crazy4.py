from botoy._internal.schedule import async_scheduler
import time
from botoy import logger
import json
from botoy import jconfig, logger
import requests
import base64
from io import BytesIO
from botoy import Action
import os

__doc__ = "疯4（auto)"


# async def get_news():
#     url = "http://dwz.2xb.cn/zaob"
#     content = requests.get(url)
#     text_to_dic = json.loads(content.text)
#     img_url = text_to_dic["imageUrl"]
#     if text_to_dic["code"] != 200:
#         return None
#     return img_url

# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)

# 获取当前脚本所在目录
current_directory = os.path.dirname(current_script_path)



async def get_text():
    url = "https://vme.im/api?format=text"
    res = requests.get(url=url)
    if res.status_code!=200:
        return None
    return res.text


def file_to_base64(file_path):
    # 以二进制模式读取文件
    with open(file_path, 'rb') as file:
        # 读取文件内容
        file_content = file.read()
        # 将文件内容转换为 Base64 编码
        base64_encoded = base64.b64encode(file_content)
        # 将字节转换为字符串
        return base64_encoded.decode('utf-8')


async def send_news():
    text = await get_text()
    if  text == None:
        return
    
    img_base64 = file_to_base64(current_directory + r"/crazy.jpg")

    action = Action(qq=jconfig.qq)
    await action.sendFriendPic(jconfig.superAdmin, text=text, base64=img_base64)
    # groups_tmp = await action.getGroupList()

    # groups = []
    # for group in groups_tmp:
    #     groups.append(group["GroupCode"])

    # groups.remove(953219612,544830164)

    # for group in groups:
    #     await action.sendGroupPic(group, text=text, base64=img_base64)
    #     time.sleep(3)
    #     logger.info("发送" + str(group) + "疯4成功！")

  


job1 = async_scheduler.add_job(send_news, "cron", day_of_week='thu', hour=10, minute=0)