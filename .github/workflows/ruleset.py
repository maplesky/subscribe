import subprocess
from pathlib import Path

rule = [
	{ url: "blackmatrix7/ios_rule_script/master/rule/Loon/Twitter/Twitter.list", to: "rule" }
]

fetch = lambda url, to: subprocess.run(
    ["curl", "-fsSL", "--retry", "3", "--create-dirs", "-o", "{ to }/", "https://raw.githubusercontent.com/{url}"],
    check=True,
)

for node in tasks:
    fetch( node["url"], node["to"] )
    print(f"✓ {out}")
