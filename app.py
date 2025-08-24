from flask import Flask, render_template, jsonify, request
import subprocess
import sys
import os
import threading

app = Flask(__name__)

# Track the running game process (if any)
GAME_PROCESS = None
LOCK = threading.Lock()


def launch_game():
    """Start main.py in a separate process if it's not already running."""
    global GAME_PROCESS
    with LOCK:
        # If a process is running and still alive, don't spawn another
        if GAME_PROCESS is not None and GAME_PROCESS.poll() is None:
            return False

        python_exe = sys.executable  # use same interpreter as Flask app
        project_dir = os.path.dirname(os.path.abspath(__file__))
        game_path = os.path.join(project_dir, 'main.py')

        # Spawn the turtle game as a detached process so the UI is responsive
        creationflags = 0
        if os.name == 'nt':
            # On Windows, avoid console window duplication
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

        GAME_PROCESS = subprocess.Popen(
            [python_exe, game_path],
            cwd=project_dir,
            creationflags=creationflags
        )
        return True


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    started = launch_game()
    if started:
        return jsonify({"status": "started"})
    return jsonify({"status": "already_running"}), 409


@app.route('/stop', methods=['POST'])
def stop():
    """Best-effort stop. Note: your turtle script may not handle SIGTERM on all OSes."""
    global GAME_PROCESS
    with LOCK:
        if GAME_PROCESS is None:
            return jsonify({"status": "not_running"}), 409

        if GAME_PROCESS.poll() is None:
            try:
                # Try graceful stop; user can also close the turtle window manually
                if os.name == 'nt':
                    GAME_PROCESS.terminate()
                else:
                    GAME_PROCESS.terminate()
            except Exception:
                pass
            return jsonify({"status": "stopping"})
        else:
            return jsonify({"status": "not_running"}), 409


if __name__ == '__main__':
    # Use debug=False for production; debug=True for development
    app.run(host='127.0.0.1', port=5000, debug=True)
