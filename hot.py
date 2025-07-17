import os
from DrissionPage import ChromiumPage
import requests
import json
import re
import regex
import time
import random

start_time = time.time()

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

dp = ChromiumPage()

print(" 🕒 正在获取抖音热榜...")
# 获取热点榜标题
dp.listen.start("https://www.iesdouyin.com/web/api/v2/hotsearch/billboard/word/")
dp.get("https://www.iesdouyin.com/share/billboard/?id=0&utm_source=copy&utm_campaign=client_share&utm_medium=android&app=aweme")
r = dp.listen.wait()
json_data = r.response.body
# print(json_data)
hot_titles = [item['word'] for item in json_data['word_list']]
print(hot_titles)
print(f" ✅ 成功获取 {len(hot_titles)} 个热点标题\n")

# 逐一获取视频信息
os.makedirs("hot_videos", exist_ok=True)
all_videos_data = []
count = 0
for hot_title in hot_titles:
    dp.listen.start("https://www.douyin.com/aweme/v1/web/general/search/stream/")
    dp.get("https://www.douyin.com/search/{}".format(hot_title))
    r = dp.listen.wait()
    raw_str = r.response.body
    match = regex.search(r'\{(?:[^{}]|(?R))*\}', raw_str)
    json_data = json.loads(match.group(0))
    data = json_data['data'][0]
    if 'aweme_info' in data:
        aweme = data['aweme_info']
    else:
        aweme = data['sub_card_list'][0]['card_info']['attached_info']['aweme_list'][0]
        # 判断是否为图文
        bit_rates = aweme["video"]["bit_rate"]
        if not bit_rates or bit_rates[0].get("format") is None:
            continue
    stats = aweme['statistics']
    video_title = aweme['desc'].split('\n')[0]
    file_video_title = clean_filename(video_title)
    digg_count = stats['digg_count']
    comment_count = stats['comment_count']
    collect_count = stats['collect_count']
    share_count = stats['share_count']
    modal_id = aweme['aweme_id']
    author_name = aweme['author']['nickname']
    video_url = f"https://www.douyin.com/user/{author_name}?modal_id={modal_id}"
    download_url = aweme['video']['play_addr']['url_list'][0]
    if(digg_count < 100000 and comment_count < 2000 and collect_count < 5000 and share_count < 1000):
         continue
    video_info = {
        "title": video_title,
        "url": video_url,
        "likes": digg_count,
        "comments": comment_count,
        "collections": collect_count,
        "shares": share_count
    }
    all_videos_data.append(video_info)
    video_content = requests.get(url=download_url, headers=headers).content
    with open(f"hot_videos\\{file_video_title}.mp4", "wb") as f:
        f.write(video_content)
        print(" ✅ 下载完成：" + file_video_title)
    delay_time = random.uniform(3, 10)
    print(f" 🕒 等待 {delay_time:.2f} 秒后继续...")
    time.sleep(delay_time)
    count += 1
print(f'------ ✅ 任务完成，成功下载 {count} 个视频 ------')
print("------ ✅ 所有视频已成功保存到 hot_videos 文件夹中 ------")

with open("hot_videos_data.json", "w", encoding="utf-8") as f:
    json.dump(all_videos_data, f, ensure_ascii=False, indent=4)
print("------ ✅ 所有视频数据已成功保存到 hot_videos_data.json 文件中 ------")

dp.quit()

end_time = time.time()
total_time_seconds = end_time - start_time
minutes, seconds = divmod(total_time_seconds, 60)
print(f"------ 🕒 程序总耗时: {int(minutes)} 分 {seconds:.2f} 秒 ------")