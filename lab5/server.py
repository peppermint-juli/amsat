
# server.py
from flask import Flask, send_from_directory
from flask_sock import Sock
import json, threading
from imu import orientation_stream

app = Flask(__name__, static_folder='static')
sock = Sock(app)

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/app.js')
def appjs():
    return send_from_directory('static', 'app.js')

# Each client gets its own stream loop
@sock.route('/ws')
def ws(ws):
    for sample in orientation_stream(hz=60):
        print(sample)
        ws.send(json.dumps(sample))

if __name__ == '__main__':
    # Listen on all interfaces so other devices can connect
    app.run(host='0.0.0.0', port=5000, debug=True)
