## App features

**one-to-one person chat.** - *Flask-SocketIO* real-time msg emit to specific user room

**typing indicators.** - *Flask-SocketIO* typing-event

**file uploads.** - *flask* HTTP POST -> save -> store path in msg

**read receipts.** - *flask-SocketIO+DB flag* mark_read event -> update is_read -> notify sender

**unread message count.** *SQLALchemy query* count msgs where receiver_id=user and is_read=false

**the ability to delete messages.** *Flask-SocketIO+DB flag* soft delete (set is_deleted-true)


## BACKEND Tech-stack

flask flask-socketio flask-sqlalchemy eventlet

Registration is via username only, for now.

**HTTP routes:**
Home page (/),
Register username,
List all users,
Get messages between two users,
Upload file endpoint,
Serve uploaded files

**SocketIO event handlers:**
connect / disconnect,
send_message,
typing start/stop,
mark_read,
delete_message

### Database Tables

**users** -
id (primary key),
username (unique)

**messages** -
id (primary key),
sender_id (foreign key → users.id),
receiver_id (foreign key → users.id),
content (text, nullable),
file_path (string, nullable),
timestamp (datetime),
is_read (boolean, default false),
is_deleted (boolean, default false)
## Frontend with simple HTML/CSS/JS 

Plain HTML + CSS + vanilla JavaScript + Socket.IO client

**File uploads** - local folder (static/uploads)