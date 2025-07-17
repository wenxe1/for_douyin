import os
from DrissionPage import ChromiumPage
import requests
import json
import re
import regex

# 模拟浏览器
headers = {
    "referer": "https://www.douyin.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
}

# 清洗文件名
def clean_filename(original_title):
    illegal_chars_pattern = r'[\\/*?:"<>|]'
    clean_title = re.sub(illegal_chars_pattern, ' ', original_title)
    final_title = clean_title.strip()
    return final_title

# 实例化浏览器
dp = ChromiumPage()
# 监听数据包特征
dp.listen.start("https://www.douyin.com/aweme/v1/web/general/search/stream/")
# 打开网页
hot_title = "6月16-24岁劳动力失业率公布"
dp.get("https://www.douyin.com/search/{}".format(hot_title))
# 等待数据包加载
r = dp.listen.wait()
# 获取响应数据
raw_str = r.response.body
# 正则匹配第一个json
match = regex.search(r'\{(?:[^{}]|(?R))*\}', raw_str)
json_data = json.loads(match.group(0))
print(json_data)
# 提取数据
data = json_data['data'][0]
if 'aweme_info' in data:
    aweme = data['aweme_info']
else:
    aweme = data['sub_card_list'][0]['card_info']['attached_info']['aweme_list'][0]
    # 判断是否为图文
    bit_rates = aweme["video"]["bit_rate"]
    if not bit_rates or bit_rates[0].get("format") is None:
        exit(0)
statistics = aweme['statistics']
video_title = aweme['desc'].split('\n')[0]
file_video_title = clean_filename(video_title)
digg_count = statistics['digg_count']
comment_count = statistics['comment_count']
collect_count = statistics['collect_count']
share_count = statistics['share_count']
modal_id = aweme['aweme_id']
author_name = aweme['author']['nickname']
video_url = f"https://www.douyin.com/user/{author_name}?modal_id={modal_id}"
download_url = aweme['video']['play_addr']['url_list'][0]
print(f"标题：{file_video_title}")
print(f"点赞数：{digg_count}")
print(f"评论数：{comment_count}")
print(f"收藏数：{collect_count}")
print(f"分享数：{share_count}")
print(f"视频链接：{video_url}")
print(f"视频下载链接：{download_url}")
# 保存数据
video_content = requests.get(url=download_url, headers=headers).content
os.makedirs("video", exist_ok=True)
with open(f"video\\{video_title}.mp4", "wb") as f:
    f.write(video_content)

