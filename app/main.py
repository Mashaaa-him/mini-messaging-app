from flask import Flask, request, render_template, redirect, session, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from string import ascii_uppercase
import random
import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "messaging_app"
socketio = SocketIO(app)

rooms = {}  # keep track of generated rooms 
users = {}  # keep track of users session id

# generate room codes
def gen_room(length):
    code = ""
    while True:
        for _ in range(length):
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
        if create != False:
            print("Creating room....")
            room = gen_room(4)
            print('Chat room:', room, "created!!")
            rooms[room] = {'members': 0, 'messages': []}
        elif join != False: 
            if room not in rooms:
                return render_template("home.html", error="Room doesn't exist, pleae enter valid room ID.", code=code, username=name)
        
        print(rooms)
        session['room'] = room
        session['name'] = name

        return redirect(url_for("room"))
    
    return render_template("home.html", note="Register for a chat room using your username.")


@app.route("/room", methods=["GET", "POST"])
def room():
    room = session.get("room")
    name = session.get("name")
    if room is None or name is None or room not in rooms:
        print(room, "\n", name, "\n", rooms)
        return redirect(url_for("home"))    # use redirect(url_for()) - for easy code maintenance i.e if U want to change the url for home to "/home"
    
    return render_template("room.html", room=room, name=name)


@socketio.on("message")
def message(data):
    name = session.get("name")
    chat = session.get("room")
    msg = data["data"]
    content = {
        "name": name,
        "message": msg,
        "time": data["time"]
    }
    send(content, to=chat)
    print()
    print(name, "\n", msg, "\n", data["time"])

    rooms[chat]["messages"].append(content)


@socketio.on("connect")
def connect(auth=None): # auth is required even if it's None
    chat = session.get("room")  # naming conflict :=(
    name = session.get("name")
    sid = request.sid

    if not name or not chat:
        return
    if chat not in rooms:
        print(f"{chat} room is nonexistent on this end. Disconnecting...")
        return False
    
    join_room(chat)
    time = datetime.datetime.hour # essentially very useless, but acts as a placholder and avoids errors, should def change this
    content = {
        "name" : name,
        "message" : "has joined chat room.",
        "time" : str(time)
    }

    send(content, to=chat)
    users[name] = sid
    rooms[chat]["members"] += 1 # add now because now is when user joined room
    if rooms[chat]["messages"]:
        messages = []
        for msg in rooms[chat]["messages"]:
            """
            
                "name": rooms[chat]["messages"]["name"],
                "message": rooms[chat]["messages"]["message"],
                "time": rooms[chat]["messages"]["time"]
            }"""
            send(msg, to=sid)
            messages.append(msg)
        print("\n", f"Messages: {messages}")
        # send(messages, to=sid)
    print(f"\n{name} joined room {chat} sucessfully!!") 
    print(rooms)

@socketio.on("disconnect")
def disconnect():
    print("Disconnecting...")
    chat = session.get("room")
    name = session.get("name")
    leave_room(room=chat)

    if chat in rooms:
        rooms[chat]["members"] -= 1
        if rooms[chat]["members"] <= 0:
            del rooms[chat]

    time = datetime.datetime.now()
    content = {
        "name" : name,
        "message" : "has left room.",
        "time" : str(time)
    }
    send(content, to=chat)
    print(f"\n{name} left chat room: {chat}.")
    

if __name__ == "__main__":
    socketio.run(app, debug=True)