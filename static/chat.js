async function sendMessage() {
    const message = document.getElementById("userInput").value;
    if (!message) return;

    const chatDiv = document.getElementById("chat");
    chatDiv.innerHTML += `<p class="user-msg"><b>You:</b> ${message}</p>`;
    document.getElementById("userInput").value = "";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: "user1", message })
        });

        const data = await res.json();
        chatDiv.innerHTML += `<p class="bot-msg"><b>Bot:</b> ${data.response}</p>`;
        chatDiv.scrollTop = chatDiv.scrollHeight;
    } catch (err) {
        chatDiv.innerHTML += `<p style="color:red;"><b>Error:</b> Could not reach server.</p>`;
    }
}
