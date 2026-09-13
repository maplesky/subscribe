# 依赖库
import json
from curl_cffi import requests

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
	if "asOrganization" in item["meta"] and item["meta"]["country"] in ["HK", "SG", "TW", "JP", "KR", "US", "GB", "AU"]
]

for item in basic:
	meta = item.get("meta", {})
	ip = item.get("ip", 0)
	port = meta.get("_port", 443)

	asn = meta["asn"]
	city = meta["city"]
	country = meta["country"]
	organization = meta["asOrganization"]

	# 请求数据
	url = f"{ip}:{port}"
	print(f"正在测试：{url:<20}", end="")
	node = session.get(f"https://v2.xxapi.cn/api/tcping", params = {
		"address": ip,
		"port": port
    })
	context = node.json()

	# 结果筛选
	if node.status_code == 200 and context.get("code", 0 ) == 200:
		# 获取延迟
		lat = context['data']['ping']
		if float(lat[:-2]) < 200:
			# 写入缓存
			cache.append(f"{url}#{country} {city} / {organization} / AS{asn}\n")
			print(f" | \033[32m{ lat }\033[0m")
		else:
			print(" | \033[31m延迟过高\033[0m")
	else:
		print(f" | \033[31m{ context.get('msg', node.status_code ) }\033[0m")

# 缓存写入文件
with open("country.txt", "w", encoding="utf-8") as f:
	f.writelines( cache )
