import subprocess

rule = [
	{ url: "blackmatrix7/ios_rule_script/master/rule/Loon/Twitter/Twitter.list", to: "rule" }
]

for node in rule:
	subprocess.run(
		["curl", "-fsSL", "--retry", "3", "--create-dirs", "--output-dir", node["to"], "-O", "https://raw.githubusercontent.com/{ node["url"] }"],
		check=True,
	)
