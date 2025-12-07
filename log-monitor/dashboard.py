# dashboard.py
from flask import Flask, jsonify, render_template_string
import redis, json

app = Flask(__name__)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

TEMPLATE = """
<!doctype html>
<title>Log Monitor</title>
<h1>Recent Logs</h1>
<ul id="logs"></ul>
<script>
async function fetchLogs(){
  const res = await fetch('/recent');
  const data = await res.json();
  const ul = document.getElementById('logs');
  ul.innerHTML = '';
  data.forEach(l => {
    const li = document.createElement('li');
    li.textContent = JSON.stringify(l);
    ul.appendChild(li);
  });
}
setInterval(fetchLogs, 1000);
fetchLogs();
</script>
"""

@app.route("/")
def index():
    return render_template_string(TEMPLATE)

@app.route("/recent")
def recent():
    items = r.xrevrange("logs", "+", "-", count=50)
    out = []
    for i in items:
        out.append(json.loads(i[1]["payload"]))
    return jsonify(out)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
