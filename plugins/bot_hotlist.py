# import asyncio
# import datetime
# import time
# import requests, json
# import cpuinfo
# import psutil
# from botoy import S, ctx, mark_recv, logger
# import asyncio

# __doc__ = "发送 '微博热搜'"


# async def get_HotList(choice: str = "weibo"):
#     "获取微博热搜"
#     try:
#         response = requests.get(url="https://tenapi.cn/resou/", timeout=10)
#         text_to_dic = json.loads(response.text)
#         data = text_to_dic["list"]

#         content = "#实时微博热搜#\n"

#         for i in range(0, 10):
#             content += str(i) + "." + data[i]["name"] + "\n"

#         return data, content
#     except:
#         logger.info("获取微博热搜请求超时！")
#         return None, None



# async def main():
#     if m := (ctx.group_msg or ctx.friend_msg):
#         if m.text == "微博热搜":
#             data, content = await get_HotList()
            
        


# mark_recv(main, author="alinjiong", name="关键字", usage="发送二次元、看看腿、舔狗日记")
