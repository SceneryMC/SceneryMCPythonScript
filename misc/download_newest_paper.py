import os
import json

with os.popen("curl -X 'GET' \
  'https://api.papermc.io/v2/projects/paper' \
  -H 'accept: application/json'") as f:
    result = json.load(f)
latest_version = result['versions'][-1]
with os.popen(f"curl -X 'GET' \
  'https://api.papermc.io/v2/projects/paper/versions/{latest_version}/builds' \
  -H 'accept: application/json'") as f:
    result = json.load(f)
latest_build_json = result['builds'][-1]
num, name = latest_build_json['build'], latest_build_json['downloads']['application']['name']
os.system(f"curl -X 'GET' \
  'https://api.papermc.io/v2/projects/paper/versions/{latest_version}/builds/{num}/downloads/{name}' \
  -H 'accept: application/json' \
  --output '/mnt/E/时间的沉淀/游戏/Minecraft/Minecraft服务器/灵工艺/server/paper-{latest_version}.jar'")
