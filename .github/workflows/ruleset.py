import subprocess

rule = [
	{ "name": "Twitter", "to": "rule" }
]

for node in rule:
	subprocess.run(
		["curl", "-fsSL", "--retry", "3", "--create-dirs", "--output-dir", node["to"], "-O", f"https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Loon/{ node['url'] }/{ node['url'] }.list"],
		check=True,
	)
