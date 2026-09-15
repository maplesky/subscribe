# 依赖库
import json
from curl_cffi import requests
from urllib.parse import urlparse, parse_qsl
from concurrent.futures import ThreadPoolExecutor, as_completed

# 临时缓存
cache = []

# 复用连接
session = requests.Session(
	timeout = 15,
	impersonate = "chrome"
)

# 转换数据
basic = [
	item for item in session.get("https://zip.cm.edu.kg/all.json").json().get('data', [])
	if "asOrganization" in item["meta"] and item["meta"]["country"] in ["HK", "SG", "TW", "JP", "KR", "US", "GB", "FR", "RU"]
]

# 多线程处理
with ThreadPoolExecutor( max_workers = 25 ) as pool:
	results = pool.map(
			lambda node: ( node["meta"], session.get(f"https://v2.xxapi.cn/api/tcping?address={ node["ip"] }&port={ node["port"][0] }")
		),
		basic
	)

	for meta, response in results:
		ip = dict( parse_qsl( urlparse( response.url ).query ) ).get("address")
		print(f"{ip:<15}", end="")
		if response.status_code == 200:
			# 转换数据
			ex = response.json()
			if ex.get("code", 0 ) == 200:
				lat = ex["data"]["ping"]
				if float( lat[:-2] ) < 200:
					# 写入缓存
					cache.append(f"{ ip }:{ ex['data']['port'] }#{ meta['country'] } { meta['city'] } / { meta['asOrganization'] } / AS{ meta['asn'] }\n")
					print(f" | \033[32m{ lat }\033[0m")
				else:
					print(f" | \033[31m延迟过高\033[0m")
			else:
				print(f" | \033[31m{ ex.get('msg', response.status_code ) }\033[0m")
		else:
			print("网络错误：", response.status_code )

# 缓存写入文件
with open("country.txt", "w", encoding="utf-8") as f:
	f.writelines( cache )
