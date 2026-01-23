from flask import Flask, request, render_template, redirect, session, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from string import ascii_uppercase
import random

app = Flask(__name__)
app.config["SECRET_KEY"] = "messaging_app"
socketio = SocketIO(app)

rooms = {}  # keep track of generated rooms 


# generate room codes
def gen_room(length):
    code = ""
    while True:
        for _ in length:
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break   
    return code


@app.route("/", methods=["POST", "GET"])
def home():
    session.clear() # to "allow" users to join other chat rooms
    if request.method == "POST":
        name = request.form.get("username") # if 'name' not found null is returned
        code = request.form.get("code")
        join = request.form.get("join", False) # if 'join' not found False is returned
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a username", code=code)
        
        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", username=name)
        
        room = code
        print(code)
        if create:
            room = gen_room(4)
            rooms[room] = {'members': 0, 'messages': []}
        elif join != False: 
            if room not in rooms:
                return render_template("home.html", error="Room doesn't exist, pleae enter valid room ID.", code=code, username=name)
        
        print(room)
        session['room'] = room
        session['name'] = name

        return redirect(url_for("room"))
    
    return render_template("home.html")


@app.route("/room", methods=["GET", "POST"])
def room():
    return render_template("room.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)