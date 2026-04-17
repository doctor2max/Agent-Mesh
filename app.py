import threading
import time
import requests
import random
from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

"""
Agent Mesh Backend - Pro Version
--------------------------------
This server acts as a central hub (C2) to control AI agents in a web interface.
It supports real-time communication via Socket.IO and RESTful API for external controls.

Author: AI Assistant
License: MIT
"""

class Config:
    """Configuration settings for the application."""
    HOST = '127.0.0.1'
    PORT = 5000
    DEBUG = False
    API_URL = f"http://{HOST}:{PORT}/api/control"

app = Flask(__name__)
# Enable CORS for cross-origin requests from the web dashboard
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize Socket.IO with threading mode for real-time UI updates
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global dictionary to track agent states locally in the backend
agent_states = {
    "1": "sleeping",
    "2": "sleeping",
    "3": "sleeping",
    "4": "sleeping"
}

# =========================================================
# 1. REST API Endpoints (نقاط نهاية واجهة البرمجة)
# =========================================================

@app.route('/api/control', methods=['POST'])
def control_agent():
    """
    Receives JSON commands to control agents.
    Payload: { "agent_id": str, "action": str, "target_id": str (optional) }
    """
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Content-Type must be application/json"
        }), 400

    data = request.json
    agent_id = data.get('agent_id')
    action = data.get('action')

    if not agent_id or not action:
        return jsonify({"error": "Missing required fields (agent_id, action)"}), 400

    # Update local state if the action is a status change
    if action in ["thinking", "working", "sleeping"]:
        agent_states[agent_id] = action

    # Forward the command to the Frontend via WebSocket
    socketio.emit('ui_command', data)

    print(f"[API] Command Processed: Agent {agent_id} -> {action}")
    return jsonify({
        "status": "success",
        "processed_data": data
    }), 200

@app.route('/api/status', methods=['GET'])
def get_status():
    """Returns the current health status of the server."""
    return jsonify({"status": "online", "timestamp": time.time(), "agent_states": agent_states}), 200

# =========================================================
# 2. WebSocket Events (أحداث سوكيت لاتصال الواجهة)
# =========================================================

@socketio.on('connect')
def handle_connect():
    """Fires when a browser client connects."""
    client_id = request.sid
    print(f"[Socket] Client Connected: {client_id}")
    emit('server_log', {
        'text': 'تم الاتصال بمحرك الأوامر المركزي بنجاح',
        'type': 'success'
    })

@socketio.on('disconnect')
def handle_disconnect():
    print(f"[Socket] Client Disconnected")

# =========================================================
# 3. Directed Sequence Logic (منطق الأوامر المتسلسلة المباشرة)
# =========================================================

def send_command(payload):
    """Helper to send POST requests to the local API."""
    try:
        response = requests.post(Config.API_URL, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"[Logic Error] Failed to send command: {e}")
        return False

def automated_agent_logic():
    """
    Background thread running a direct, fixed sequence of commands.
    Loops indefinitely with a 2-second interval between each step.
    """
    print("[Brain] Starting directed sequence engine...")
    time.sleep(5)  # Initial wait for server stability

    # تعريف السلسلة المطلوبة بدقة
    while True:
        try:
            # 1. الوكيل الأول يعمل
            send_command({"agent_id": "1", "action": "working"})
            time.sleep(2)

            # 2. الوكيل الأول يرسل للوكيل الثاني
            send_command({"agent_id": "1", "action": "connection", "target_id": "2"})
            time.sleep(2)

            # 3. الوكيل الثاني يفكر
            send_command({"agent_id": "2", "action": "thinking"})
            time.sleep(2)

            # 4. الوكيل الثاني يعمل
            send_command({"agent_id": "2", "action": "working"})
            time.sleep(2)

            # 5. الوكيل الثالث يفكر
            send_command({"agent_id": "3", "action": "thinking"})
            time.sleep(2)

            # 6. الوكيل الثاني أنهى العمل (يعود للنوم)
            send_command({"agent_id": "2", "action": "sleeping"})
            time.sleep(2)

            # 7. الوكيل الرابع يعمل
            send_command({"agent_id": "4", "action": "working"})
            time.sleep(2)

            # 8. الوكيل الثالث يعمل
            send_command({"agent_id": "3", "action": "working"})
            time.sleep(2)

            # 9. الوكيل الرابع يتصل بالوكيل الثاني
            send_command({"agent_id": "4", "action": "connection", "target_id": "2"})
            time.sleep(2)

            # 10. الوكيل الثاني يفكر
            send_command({"agent_id": "2", "action": "thinking"})
            time.sleep(2)

            # 11. الوكيل الثاني يعمل
            send_command({"agent_id": "2", "action": "working"})
            time.sleep(2)

            # 12. الوكيل الثاني أنهى العمل
            send_command({"agent_id": "2", "action": "sleeping"})
            time.sleep(2)

            # 13. الوكيل الرابع أنهى العمل
            send_command({"agent_id": "4", "action": "sleeping"})
            time.sleep(2)

            # إعادة تعيين الحالات الأخرى قبل بدء اللوب من جديد لضمان الاستمرارية
            send_command({"agent_id": "1", "action": "sleeping"})
            send_command({"agent_id": "3", "action": "sleeping"})
            print("[Brain] Sequence completed. Restarting...")
            time.sleep(2)

        except Exception as e:
            print(f"[Critical] Logic Error: {e}")
            time.sleep(10)

# =========================================================
# 4. Entry Point (نقطة تشغيل النظام)
# =========================================================

if __name__ == '__main__':
    # Start the background logic thread
    logic_thread = threading.Thread(target=automated_agent_logic, daemon=True)
    logic_thread.start()

    print("\n" + "="*50)
    print("  AGENT MESH SERVER - DIRECTED MODE")
    print(f"  API: http://{Config.HOST}:{Config.PORT}/api/control")
    print("="*50 + "\n")

    # Run the server
    socketio.run(app, host=Config.HOST, port=Config.PORT, debug=Config.DEBUG, allow_unsafe_werkzeug=True)
