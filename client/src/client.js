const codeEditor = ace.edit("code-editor");
codeEditor.setTheme("ace/theme/twilight");
codeEditor.session.setMode("ace/mode/python");

const languageSelect = document.getElementById('language-select');
const runButton = document.getElementById('run-button');

runButton.addEventListener('click', () => {
    const code = codeEditor.getValue();
    const language = languageSelect.value;

    const message = {
        type: 'code',
        code: code,
        language: language
    };

    ws.send(JSON.stringify(message));
});

const ws = new WebSocket(`ws://${window.location.host}`);

ws.onopen = function() {
    console.log('Connected to server');
};

ws.onmessage = function(event) {
    console.log('Received from server:', event.data);
    const outputDiv = document.getElementById('output');
    outputDiv.textContent = event.data;
};
