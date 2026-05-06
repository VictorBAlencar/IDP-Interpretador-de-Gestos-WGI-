document.getElementById('btn-start').addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: "start_tracking" });
    document.getElementById('status').innerText = "Iniciando câmera, por favor aguarde...";
    document.getElementById('loading-container').style.display = "block";
});

document.getElementById('btn-stop').addEventListener('click', () => {
    chrome.runtime.sendMessage({ action: "stop_tracking" });
    document.getElementById('status').innerText = "Parando...";
    document.getElementById('loading-container').style.display = "none";
});

// Ouve as respostas que vêm do Python
chrome.runtime.onMessage.addListener((msg) => {
    if (msg && msg.message) {
        document.getElementById('status').innerText = msg.message;
        document.getElementById('loading-container').style.display = "none";
    }
});

// Verifica o estado do servidor ao abrir o popup e atualiza a mensagem
document.addEventListener('DOMContentLoaded', () => {
    chrome.runtime.sendMessage({ action: "get_state" }, (response) => {
        if (chrome.runtime.lastError) return;
        
        if (response && response.is_tracking) {
            document.getElementById('status').innerText = "Câmera ativa e rastreando!";
        } else if (response && response.error) {
            document.getElementById('status').innerText = "Erro: O servidor WGI (Python) não está rodando.";
        }
    });
});