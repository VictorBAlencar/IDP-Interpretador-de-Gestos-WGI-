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
    document.getElementById('status').innerText = msg.message;
    document.getElementById('loading-container').style.display = "none";
});