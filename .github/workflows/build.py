# 依赖库
import json
import time
from curl_cffi import requests

# 临时缓存
cache = []

# 筛选区域
country = ["HK", "SG", "TW", "JP", "KR", "US", "GB", "FR"]

# 获取数据
all = requests.get(
    "https://zip.cm.edu.kg/all.json",
    timeout=15,
    impersonate="chrome"
)

# 转换数据
basic = [
	item for item in all.json().get('data', [])
	if "asOrganization" in item["meta"] and item["meta"]["country"] in country
]

# 多线程处理
for i, data in enumerate( basic ):
	cache.append(f"{ data.get('ip') }:{ data.['port'][0] }\n")

# 缓存写入文件
with open("country.txt", "w", encoding="utf-8") as f:
	f.writelines( cache )
