from todoist_api_python.api import TodoistAPI
import os,sys

key_path = os.path.expanduser("~/todoist_utils/api_key")
with open(key_path,encoding="utf8") as f:
    api_key = f.read().strip()

client = TodoistAPI(api_key)

if len(sys.argv) == 1:
    query = "##inbox"
else:
    query = " ".join(sys.argv[1:])

resp = client.filter_tasks(query=query)

for i in resp:
    for j in i:
        print(f"{j.id}: {j.content}")

