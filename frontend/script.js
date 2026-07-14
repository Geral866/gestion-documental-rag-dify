async function enviarMensaje() {
    const input = document.getElementById("input-usuario");
    const pregunta = input.value.trim();
    if (!pregunta) return;

    agregarMensaje("usuario", pregunta);
    input.value = "";
    agregarMensaje("bot", "⏳ Consultando...", "loading");

    try {
        const res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pregunta })
        });

        const data = await res.json();

        // Quitar el mensaje de carga
        document.querySelector(".loading")?.remove();

        // Mostrar respuesta
        let contenido = data.respuesta;
        if (data.fuentes && data.fuentes.length > 0) {
            contenido += `<br><small>📄 Fuentes: ${data.fuentes.join(", ")}</small>`;
        }
        agregarMensaje("bot", contenido);

    } catch (error) {
        document.querySelector(".loading")?.remove();
        agregarMensaje("bot", "❌ Error al conectar con el servidor.");
    }
}

function agregarMensaje(tipo, texto, clase = "") {
    const chat = document.getElementById("chat-container");
    const div = document.createElement("div");
    div.className = `mensaje ${tipo} ${clase}`;
    div.innerHTML = texto;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

// Enviar con Enter
document.getElementById("input-usuario")
    ?.addEventListener("keypress", e => {
        if (e.key === "Enter") enviarMensaje();
    });
    
    