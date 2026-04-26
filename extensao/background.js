// background.js - O "Cérebro" da Extensão WGI

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    const BASE_URL = "http://127.0.0.1:8765";

    //Iniciar ou Parar o Rastreamento com mediapipe
    if (request.action === "start_tracking" || request.action === "stop_tracking") {
        fetch(`${BASE_URL}/${request.action}`, { 
            method: "POST",
            mode: 'cors' 
        })
        .then(response => response.json())
        .then(data => {
            // Envia mensagem de sucesso de volta para o popup.js
            chrome.runtime.sendMessage({ message: data.message }).catch(() => {});
        })
        .catch(error => {
            console.error("Erro no servidor WGI:", error);
            chrome.runtime.sendMessage({ message: "Erro: O servidor WGI (Python) não está rodando." }).catch(() => {});
        });
        return true; // Mantém o canal aberto para a resposta assíncrona
    }

    // usa o get_state para pegar os dados do servidor e o content.js saber onde a mão esta
    if (request.action === "get_state") {
        fetch(`${BASE_URL}/state`)
            .then(response => response.json())
            .then(data => {
                sendResponse(data);
            })
            .catch(error => {
                sendResponse({ action: "move", error: true });
            });
        return true; // Mantém o canal aberto para a resposta assíncrona
    }
});