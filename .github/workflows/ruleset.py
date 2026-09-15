import subprocess

rule = [
	"Twitter"
]

for node in rule:
	subprocess.run(
		["curl", "-fsSL", "--retry", "3", "--create-dirs", "--output-dir", "rule/loon", "-O", f"https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Loon/{ node }/{ node }.list"],
		check=True,
	)

	subprocess.run(
		["curl", "-fsSL", "--retry", "3", "--create-dirs", "--output-dir", "rule/clash", "-O", f"https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/{ node }/{ node }.list"],
		check=True,
	)
