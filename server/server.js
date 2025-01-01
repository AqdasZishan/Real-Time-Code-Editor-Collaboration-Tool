const express = require('express');
const http = require('http');
const WebSocket = require('ws');
const path = require('path');
const fs = require('fs');

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });

// Serve the index.html file
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, '../client/public/index.html'));
});

// Serve the client.js file
app.get('/src/client.js', (req, res) => {
    res.sendFile(path.join(__dirname, '../client/src/client.js'));
});

// WebSocket connection
wss.on('connection', function connection(ws) {
    console.log('Client connected');

    // Handle incoming messages
    ws.on('message', function incoming(message) {
        const data = JSON.parse(message);
        if (data.type === 'code') {
            // Determine the language
            let runCommand;
            let fileExtension;
            switch (data.language) {
                case 'python':
                    runCommand = `python run_python.py temp/temp_code.py`;
                    fileExtension = 'py';
                    break;
                case 'java':
                    runCommand = `python run_java.py temp/temp_code.java`;
                    fileExtension = 'java';
                    break;
                default:
                    console.log('Unsupported language');
                    ws.send('Unsupported language');
                    return;
            }

            // Write code to a temporary file with the correct extension
            const tempDir = path.join(__dirname, 'temp');
            if (!fs.existsSync(tempDir)) {
                fs.mkdirSync(tempDir);
            }
            const tempFile = path.join(tempDir, `temp_code.${fileExtension}`);
            fs.writeFileSync(tempFile, data.code);

            // Execute the run command
            const exec = require('child_process').exec;
            exec(runCommand, { cwd: __dirname }, (error, stdout, stderr) => {
                if (error) {
                    console.error(`Execution error: ${error.message}`);
                    ws.send(`Execution error: ${error.message}`);
                    return;
                }
                if (stderr) {
                    console.error(`Runtime error: ${stderr}`);
                    ws.send(`Runtime error: ${stderr}`);
                    return;
                }
                console.log(`Execution result:\n${stdout}`);
                //console.log(stdout);
                //ws.send(`Execution result:`);
                ws.send(stdout);
            });
        }
    });
});

const PORT = process.env.PORT || 5000;
server.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
