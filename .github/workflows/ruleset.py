import subprocess
from pathlib import Path

base = "https://raw.githubusercontent.com/"

tasks = [
    {"url": "ACL4SSR/ACL4SSR/master/Clash/Ruleset/Spotify.list", "dir": "ruleset"},
    # 后续追加即可
]

# 闭包：生成 curl 命令（-f 失败即报错，-L 跟随重定向，-sS 静默但保留错误）
fetch = lambda url, out: subprocess.run(
    ["curl", "-fsSL", "--retry", "3", "--create-dirs", "-o", str(out), base + url],
    check=True
)

for t in tasks:
    out = Path(t["dir"]) / Path(t["url"]).name
    fetch(t["url"], out)
    git("add", str(out))
    # 只有内容有变化才提交，避免空提交报错
    if subprocess.run(["git", "diff", "--cached", "--quiet"]).returncode != 0:
        git("commit", "-m", f"chore: update {out} from {t['url']}")
        print(f"✓ committed {out}")
    else:
        print(f"= no change {out}")
