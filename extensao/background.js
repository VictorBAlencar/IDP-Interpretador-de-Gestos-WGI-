// background.js - O "Cérebro" da Extensão WGI

let CURRENT_PORT = 8765;
let BASE_URL = `http://127.0.0.1:${CURRENT_PORT}`;

async function findActivePort() {
    for (let port = 8765; port <= 8800; port++) {
        try {
            const response = await fetch(`http://127.0.0.1:${port}/`);
            if (response.ok) {
                CURRENT_PORT = port;
                BASE_URL = `http://127.0.0.1:${CURRENT_PORT}`;
                console.log(`Servidor WGI encontrado na porta ${CURRENT_PORT}`);
                return;
            }
        } catch (e) {}
    }
}

// Inicia a busca pela porta correta assim que a extensão for carregada
findActivePort();

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
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