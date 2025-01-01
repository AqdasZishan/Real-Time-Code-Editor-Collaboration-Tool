const codeEditor = ace.edit("code-editor");
codeEditor.setTheme("ace/theme/twilight");
//codeEditor.session.setMode("ace/mode/python");

const languageSelect = document.getElementById('language-select');

// Function to update code editor mode and highlighter
function updateCodeEditorMode(newLanguage) {
    // Change the mode
    codeEditor.setOption("mode", `ace/mode/${newLanguage.toLowerCase()}`);
    
    // Update the highlighter
    codeEditor.getSession().setMode(`ace/mode/${newLanguage.toLowerCase()}`);
    
    // Refresh the editor
    codeEditor.resize();
}

// Initial setup
updateCodeEditorMode('python');

// Event listener for language select
languageSelect.addEventListener('change', function() {
    const selectedLanguage = this.value;
    
    // Update the code editor mode and highlighter
    updateCodeEditorMode(selectedLanguage);
});

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
    const outputDiv = document.getElementById('view');
    outputDiv.textContent = event.data;
};
