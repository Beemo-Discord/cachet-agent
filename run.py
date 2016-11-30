import json
import redis
import requests
import time
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    db=int(os.getenv("REDIS_DB")),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

def make_request(id, value):
    url = "{0}/api/v1/metrics/{1}/points".format(os.getenv("CACHET_WEBSITE"), id)

    headers = {
        "content-type": "application/json",
        "X-Cachet-Token": os.getenv("CACHET_TOKEN")
    }

    contents = json.dumps({
        "value": value
    })

    resp = requests.post(url, data=contents, headers=headers)

    return resp.json()

def get_server_count():
    servers = 0
    for shard_key in r.keys("shard-*:servers"):
        servers += int(r.get(shard_key))

    return servers

while True:
    server_count = get_server_count()
    resp = make_request(3, server_count)
    print("server count: {0}".format(server_count))
    print("response: {0}\n".format(resp))
    time.sleep(65)
