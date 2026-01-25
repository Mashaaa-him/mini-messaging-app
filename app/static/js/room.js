var socketio = io();
        
const messages = document.getElementById("messages")

// U want sender's msgs on the let and the rest on the right
const createMessage = (name, msg, time) => {
    const content = `
    <div class="text">
        <hr>
        <span>
            <strong>${name}</strong>: ${msg}    
        </span>
        <span class="muted">
            ${time} 
        </span>
    </div>
    `;
    messages.innerHTML += content;
};

socketio.on("message", (data) => {
    createMessage(data.name, data.message, data.time);
});

const sendMessage = () => {
    const message = document.getElementById("message");
    if (message.value == "") return;
    console.log(message.value)
    const timestamp = new Date().toLocaleString()
    socketio.emit("message", {name: USERNAME, data: message.value, time: timestamp});
    message.value = "";
};
