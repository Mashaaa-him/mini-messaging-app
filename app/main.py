from flask import Flask, request, render_template, redirect, session
from flask_socketio import join_room, leave_room, send, SocketIO

app = Flask(__name__)
app.config["SECRET_KEY"] = "messaging_app"
socketio = SocketIO(app)

@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("home.html")

if __name__ == "__main__":
    socketio.run(app, debug=True)