document.addEventListener('DOMContentLoaded', function() {
    const btnTestCamera = document.getElementById('btn-test-camera');
    const btnSettings = document.getElementById('btn-settings');
    const extensionStatus = document.getElementById('extension-status');

    // Verificar se a extensão está funcionando
    extensionStatus.textContent = '✓ Extensão Ativa';
    extensionStatus.className = 'status active';

    // Botão de testar câmera
    btnTestCamera.addEventListener('click', async function() {
        try {
            // Abrir a página local via servidor HTTP
            const tab = await chrome.tabs.create({
                url: 'http://localhost:8000/arquiteto.html'
            });

            // Fechar o popup
            window.close();
        } catch (error) {
            console.error('Erro ao abrir página de teste:', error);
            alert('Abra em seu navegador: http://localhost:8000/arquiteto.html');
        }
    });

    // Botão de configurações
    btnSettings.addEventListener('click', function() {
        // Abrir página de configurações (se existir)
        alert('Configurações ainda não implementadas. Em breve!');
    });

    // Verificar permissões da câmera
    navigator.permissions.query({ name: 'camera' }).then(function(result) {
        if (result.state === 'denied') {
            extensionStatus.textContent = '⚠ Permissões necessárias';
            extensionStatus.className = 'status inactive';
        }
    }).catch(function(error) {
        console.log('Erro ao verificar permissões:', error);
    });
});