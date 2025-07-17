# fou_douyin

## 环境配置

1. 创建环境: `conda env create -f environment.yml`
2. 初始化浏览器: 打开`initial.py`，更改`path`参数并运行该文件

```Python
from DrissionPage import ChromiumOptions

# path更换为您的 chrome.exe 地址
path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ChromiumOptions().set_browser_path(path).save()
```



## 重要说明

json文件中的`'title'`字段与爬取视频的文件名一致，均将不满足windows命名规则的符号替换为了空格符，但皆可能与douyin平台上视频标题不一致



## 免责声明

- 本项目仅用于学习和技术交流，请勿用于任何商业或非法用途
- 用户在使用本脚本时，应自行承担所有风险。因使用不当造成的任何后果，作者概不负责
- 请遵守目标网站（douyin）的用户协议和 robots.txt 规定，尊重网站版权。请勿频繁请求，以免对服务器造成过大压力



## 许可证

本项目采用 [MIT 许可证](https://opensource.org/licenses/MIT)授权

