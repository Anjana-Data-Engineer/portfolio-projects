# producer.py
import redis, json, time, random
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

levels = ["DEBUG","INFO","WARN","ERROR"]
i = 0
while True:
    ev = {"id": i, "level": random.choice(levels), "msg": f"sample message {i}"}
    r.xadd("logs", {"payload": json.dumps(ev)})
    i += 1
    time.sleep(0.5)
