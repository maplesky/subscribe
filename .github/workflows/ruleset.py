import subprocess
from pathlib import Path

base = "https://raw.githubusercontent.com/"

tasks = [
    {"url": "ACL4SSR/ACL4SSR/master/Clash/Ruleset/Spotify.list", "dir": "ruleset"},
]

# 闭包：生成 curl 命令（-f 失败即报错，-L 跟随重定向，-sS 静默但保留错误）
fetch = lambda url, out: subprocess.run(
    ["curl", "-fsSL", "--retry", "3", "--create-dirs", "-o", str(out), base + url],
    check=True,
)

for t in tasks:
    out = Path(t["dir"]) / Path(t["url"]).name
    fetch(t["url"], out)
    subprocess.run(["git", "commit", "-m", f"Update from: { t['url'] }"], check=True)
