# Real-Time Log Monitor

Start Redis:
docker run -d --name redis -p 6379:6379 redis:7

Run producer:
python producer.py

Run consumer:
python consumer.py

Run dashboard:
python dashboard.py
