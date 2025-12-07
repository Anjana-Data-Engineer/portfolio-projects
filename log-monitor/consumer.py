# consumer.py
import redis, json, time
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
last_id = "0-0"
while True:
    items = r.xread({"logs": last_id}, block=5000, count=10)
    if not items:
        continue
    for stream, msgs in items:
        for msg_id, data in msgs:
            last_id = msg_id
            payload = json.loads(data["payload"])
            if payload["level"] == "ERROR":
                print("ALERT:", payload)
            else:
                print("LOG:", payload)
