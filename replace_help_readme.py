import subprocess

README="README.md"

content = open(README).read()
help_content = subprocess.check_output("python3 examples/main.py -h", shell=True).decode("utf-8")

print(help_content)

help_old_content = content[content.find("usage: main"):]
help_old_content = help_old_content[:help_old_content.find("```")]

open(README, 'w').write(content.replace(help_old_content, help_content))
