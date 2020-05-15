# 爬取B站在线列表信息
import aiohttp
import asyncio
from lxml import etree
# import re


# 创建爬取在线异步函数对象
async def online_page(url, headers):
    """
    :param url:
    :param headers:
    :return:
    """

    while True:
        hd = headers
        async with aiohttp.ClientSession() as session:  # 创建session会话对象
            async with session.get(url=url, headers=hd) as response:  # 发送异步get请求
                if response.status == 200:
                    text = await response.text()
                    html = etree.HTML(text)
                    online_title = html.xpath("//div[@id='app']//span[@class='b-head-t']/text()")[0]  # 在线列表标题
                    divs = html.xpath("//div[@class='online-list']/div[@class='ebox']")  # 获取在线列表
                    online_page_lis = []
                    print("当前爬取B站， {}".format(online_title))
                    for div in divs:
                        detail_task = {}
                        detail_url = "https:" + div.xpath(".//a/@href")[0]  # 爬取详情页
                        title = div.xpath(".//a/@title")[0]  # 详情页标题
                        online_num = "在线：" + div.xpath(".//p[@class='ol']/b/text()")[0]  # 在线人数
                        detail_task["title"] = title
                        detail_task["online_num"] = online_num
                        detail_task["detail_url"] = detail_url
                        online_page_lis.append(detail_task)
                        asyncio.ensure_future(detail_page(session, detail_url, detail_task, hd))
                else:

                    print("当前，在线列表请求状态码：{}".format(response.status))
                await asyncio.sleep(10)  # 设置每隔5秒爬取一次


# 爬取详情页（这里只爬取描述信息）
async def detail_page(session, detail_url, detail_task, hd):
    """
    :param session:
    :param detail_url:
    :param detail_task:
    :param hd:
    :return:
    """
    async with session.get(url=detail_url, headers=hd) as response:
        # **************************正则匹配*************************************
        # description = re.findall('"description": "(.*)",', text)
        # info = re.findall('"desc":"(.*)","state"', text)
        # if len(description):
        #     detail_task["description"] = description[0]
        # if len(info):
        #     detail_task["info"] = info[0]
        # print(detail_task)
        # ***************************************************************
        if response.status == 200:
            text = await response.text()
            html = etree.HTML(text)
            info = html.xpath("//div[@id='v_desc']/div[@class='info open']/text()")
            if len(info):
                detail_task["info"] = ''.join(info[0]).replace('\n', '')
            else:
                detail_task["info"] = '这个主播太懒了，没有描述信息！！！'
            print(detail_task)
        else:
            print("当前，详情页请求状态码：{}".format(response.status))

if __name__ == '__main__':
    URL = "https://www.bilibili.com/video/online.html"  # 要爬取的在线地址
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/75.0.3770.100 Safari/537.36",
        "cookie": "_uuid=2C89F850-1A60-57AD-9D54-E56935F8D00099898infoc;"
                  " buvid3=A6311267-A700-4EB4-989F-45D1A513154A190981infoc; LIVE_BUVID=AUTO3815645844862586; "
                  "CURRENT_FNVAL=16; stardustvideo=1; rpdid=|(u))uulY||k0J'ulYRl)Rlu|; DedeUserID=517851921;"
                  " DedeUserID__ckMd5=5610551f371ac367; SESSDATA=662e4b87%2C1599045834%2C713ce*31;"
                  " bili_jct=5f69deed91125e20f3c50c922fd541a8; "
                  "CURRENT_QUALITY=0; LIVE_PLAYER_TYPE=2; sid=ar6uuj1g; "
                  "bp_t_offset_517851921=389152718815264662; bsource=seo_baidu; PVID=2"
    }  # 构造请求头信息

    loop = asyncio.get_event_loop()
    loop.run_until_complete(online_page(URL, HEADERS))
