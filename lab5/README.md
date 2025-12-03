# MPU6050 Web Visualizer

This small Flask app streams orientation data from an MPU6050 (connected via I2C) over a WebSocket to a browser client that visualizes the orientation with Three.js.

Prerequisites
- A Raspberry Pi (or other Linux board) with I2C enabled and the MPU6050 wired and powered.
- Python 3.8+ and pip

Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

Run the server (on the Pi)

```bash
python3 server.py
```

Open the visualizer

- On the Pi: http://localhost:3000/
- From another device on the same network: http://<raspberry_pi_ip>:3000/

Debug endpoints

- `GET /last` — returns JSON of the last orientation sample sent over the WebSocket. Useful for verifying the server is producing values without opening the web client.

Notes

- The `smbus2` package requires access to I2C devices. On macOS you won't be able to access the MPU6050; run the server on the Pi.
- If you run the Flask server behind HTTPS, update the client to use `wss://` instead of `ws://`.

Troubleshooting

- If the browser console shows `WebSocket connection failed`, check the Pi's firewall and that the server is running on port `3000`.
- Check the server console for `WebSocket client connected` and orientation JSON output.

Next steps

- (Optional) Add authentication, rate limiting, or switch to `python-socketio` if you prefer Socket.IO features (auto-reconnect, rooms, etc.).
