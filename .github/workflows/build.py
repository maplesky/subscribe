# 依赖库
import json
import time
from curl_cffi import requests
from urllib.parse import urlparse, parse_qsl
from concurrent.futures import ThreadPoolExecutor, as_completed

# 临时缓存
cache = []

# 复用连接
session = requests.Session(
	retry = 3,
	timeout = 15,
	impersonate = "chrome"
)

# 转换数据
basic = [
	item for item in session.get("https://zip.cm.edu.kg/all.json").json().get('data', [])
	if "asOrganization" in item["meta"] and item["meta"]["country"] in ["HK", "SG", "TW", "JP", "KR", "US", "GB", "FR", "RU", "FI", "NL", "DE"]
]

# 多线程处理
for item in basic:
	cache.append(f"{ item['ip'] } { item['port'][0] }\n")

# 缓存写入文件
with open("country.txt", "w", encoding="utf-8") as f:
	f.writelines( cache )
