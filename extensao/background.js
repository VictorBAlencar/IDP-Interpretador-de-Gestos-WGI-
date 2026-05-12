let CURRENT_PORT = 8765;
let BASE_URL = `http://127.0.0.1:${CURRENT_PORT}`;

async function findActivePort() {
    let firstAvailablePort = null;

    for (let port = 8765; port <= 8800; port++) {
        try {
            const response = await fetch(`http://127.0.0.1:${port}/state`);
            if (!response.ok) continue;

            if (firstAvailablePort === null) {
                firstAvailablePort = port;
            }

            const state = await response.json();
            if (state && state.is_tracking) {
                CURRENT_PORT = port;
                BASE_URL = `http://127.0.0.1:${CURRENT_PORT}`;
                console.log(`Servidor WGI encontrado na porta ${CURRENT_PORT}`);
                return;
            }
        } catch (e) {}
    }

    if (firstAvailablePort !== null) {
        CURRENT_PORT = firstAvailablePort;
        BASE_URL = `http://127.0.0.1:${CURRENT_PORT}`;
        console.log(`Servidor WGI encontrado na porta ${CURRENT_PORT}`);
    }
}

findActivePort();

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === "start_tracking" || request.action === "stop_tracking") {
        findActivePort()
            .then(() => fetch(`${BASE_URL}/${request.action}`, {
                method: "POST",
                mode: "cors"
            }))
            .then(response => response.json())
            .then(data => {
                chrome.runtime.sendMessage({ message: data.message }).catch(() => {});
                sendResponse(data);
            })
            .catch(error => {
                console.error("Erro no servidor WGI:", error);
                const data = { message: "Error: WGI server is not running.", error: true };
                chrome.runtime.sendMessage(data).catch(() => {});
                sendResponse(data);
            });
        return true;
    }

    if (request.action === "get_state") {
        findActivePort()
            .then(() => fetch(`${BASE_URL}/state`))
            .then(response => response.json())
            .then(data => sendResponse(data))
            .catch(error => sendResponse({ action: "move", error: true }));
        return true;
    }

    if (request.action === "get_config") {
        findActivePort()
            .then(() => fetch(`${BASE_URL}/config`))
            .then(response => response.json())
            .then(data => sendResponse(data))
            .catch(error => sendResponse(null));
        return true;
    }

    if (request.action === "set_config") {
        findActivePort()
            .then(() => fetch(`${BASE_URL}/config`, {
                method: "POST",
                body: JSON.stringify(request.data),
                headers: { "Content-Type": "application/json" }
            }))
            .then(response => response.json())
            .then(data => sendResponse(data))
            .catch(error => sendResponse(null));
        return true;
    }

    if (request.action === "start_calibration") {
        findActivePort()
            .then(() => fetch(`${BASE_URL}/start_calibration`, {
                method: "POST",
                body: JSON.stringify({ gesture: request.gesture }),
                headers: { "Content-Type": "application/json" }
            }))
            .then(response => response.json())
            .then(data => sendResponse(data))
            .catch(error => sendResponse(null));
        return true;
    }

    if (request.action === "set_wizard_mode") {
        findActivePort()
            .then(() => fetch(`${BASE_URL}/set_wizard_mode`, {
                method: "POST",
                body: JSON.stringify({ active: request.active }),
                headers: { "Content-Type": "application/json" }
            }))
            .then(response => response.json())
            .then(data => sendResponse(data))
            .catch(error => sendResponse(null));
        return true;
    }

    if (request.action === "get_base_url") {
        findActivePort()
            .then(() => sendResponse({ base_url: BASE_URL }))
            .catch(() => sendResponse({ base_url: BASE_URL }));
        return true;
    }
});
