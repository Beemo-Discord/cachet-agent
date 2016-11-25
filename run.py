import json
import redis
import requests
import time

config = json.load(open("config.json", "r"))
r = redis.Redis(host=config["host"], port=config["port"], password=config["auth"], db=config["db"], decode_responses=True)

def make_request(id, value):
    url = "{0}/api/v1/metrics/{1}/points".format(config["cachet_website"], id)

    headers = {
        "content-type": "application/json",
        "X-Cachet-Token": config["cachet_token"]
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
    resp = make_request(2, server_count)
    print("server count: {0}".format(server_count))
    print("response: {0}\n".format(resp))
    time.sleep(65)
