
# server.py
from flask import Flask, send_from_directory, jsonify
from flask_sock import Sock
import json, threading
from imu import orientation_stream

app = Flask(__name__, static_folder='static')
sock = Sock(app)

# store last sample sent for debugging / HTTP inspection
last_sample = {}

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/app.js')
def appjs():
    return send_from_directory('static', 'app.js')

# Each client gets its own stream loop
@sock.route('/ws')
def ws(ws):
    global last_sample
    print("WebSocket client connected")
    try:
        for sample in orientation_stream(hz=60):
            # update last-sent sample (useful for HTTP debug endpoint)
            last_sample = sample
            print(sample)
            ws.send(json.dumps(sample))
    except Exception as e:
        # client likely disconnected; log and exit
        print("WebSocket connection closed or error:", e)

if __name__ == '__main__':
    # Listen on all interfaces so other devices can connect
    app.run(host='0.0.0.0', port=3000, debug=True)


@app.route('/last')
def last():
    """Return the last orientation sample sent over the websocket.

    Useful for testing/debugging without opening a websocket client.
    """
    return jsonify(last_sample)
