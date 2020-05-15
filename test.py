import requests
import re
from lxml import etree

url = "https://www.bilibili.com/video/BV1Bz411q7g3"


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

response = requests.get(url=url, headers=HEADERS)
text = response.text
html = etree.HTML(text)

description = re.findall('"description": "(.*)",', text)
info = re.findall('"desc":"(.*)","state"', text)

if len(description):
    print(description[0])
else:
    print(info[0])