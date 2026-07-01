async function enviarPregunta() {
    const inputElement = document.getElementById('userInput');
    const input = inputElement.value;
    const chatBox = document.getElementById('chat-box');
    
    // Mostrar lo que el usuario escribió
    chatBox.innerHTML += `<p><b>Tú:</b> ${input}</p>`;
    inputElement.value = ''; // Limpiar campo
    
    try {
        const response = await fetch('http://127.0.0.1:8000/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta: input })
        });
        
        const data = await response.json();
        // Mostrar respuesta de la IA
        chatBox.innerHTML += `<p><b>IA:</b> ${data.answer || "Respuesta recibida"}</p>`;
    } catch (error) {
        chatBox.innerHTML += `<p style="color:red;">Error de conexión con el backend.</p>`;
    }
}