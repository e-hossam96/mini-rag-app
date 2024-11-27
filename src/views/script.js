document.addEventListener('DOMContentLoaded', () => {
    // Include marked and DOMPurify CDN links
    const markedScript = document.createElement('script');
    markedScript.src = 'https://cdn.jsdelivr.net/npm/marked/marked.min.js';
    document.head.appendChild(markedScript);

    const domPurifyScript = document.createElement('script');
    domPurifyScript.src = 'https://cdn.jsdelivr.net/npm/dompurify@3.0.3/dist/purify.min.js';
    document.head.appendChild(domPurifyScript);

    // Wait for scripts to load
    Promise.all([
        new Promise(resolve => { markedScript.onload = resolve; }),
        new Promise(resolve => { domPurifyScript.onload = resolve; })
    ]).then(() => {
        const apiBase = "http://localhost:8000/api/v1";
        const projectNameInput = document.getElementById('project-name');
        const fileUploadInput = document.getElementById('file-upload');
        const fileList = document.getElementById('file-list');
        const uploadBtn = document.getElementById('upload-btn');
        const processBtn = document.getElementById('process-btn');
        const vectorizeBtn = document.getElementById('vectorize-btn');
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        const chatMessages = document.getElementById('chat-messages');

        // File upload handling
        fileUploadInput.addEventListener('change', handleFileSelect);

        function handleFileSelect(event) {
            fileList.innerHTML = '';
            const files = event.target.files;
            for (let file of files) {
                const fileItem = document.createElement('div');
                fileItem.textContent = file.name;
                fileList.appendChild(fileItem);
            }
        }

        // Validate project name
        function validateProjectName() {
            const projectName = projectNameInput.value.trim();
            if (!projectName) {
                alert('Please enter a project name');
                return false;
            }
            return projectName;
        }

        // Upload files
        uploadBtn.addEventListener('click', async () => {
            const projectName = validateProjectName();
            if (!projectName) return;

            const files = fileUploadInput.files;
            if (files.length === 0) {
                alert('Please select files to upload');
                return;
            }

            // For multiple files, we'll upload one by one
            for (let file of files) {
                const formData = new FormData();
                formData.append('file', file);

                try {
                    const response = await fetch(`${apiBase}/data/upload/${projectName}`, {
                        method: 'POST',
                        body: formData
                    });

                    const result = await response.json();

                    if (response.ok) {
                        console.log('File uploaded:', result);
                        // Use result.file_id, result.asset_id, result.project_id if needed
                        alert(result.signal || 'Upload Succeeded');
                    } else {
                        // Handle validation errors or other issues
                        alert(result.signal || 'Upload failed');
                    }
                } catch (error) {
                    console.error('Upload error:', error);
                    alert('Error uploading files');
                }
            }
        });

        // Process files
        processBtn.addEventListener('click', async () => {
            const projectName = validateProjectName();
            if (!projectName) return;

            try {
                const response = await fetch(`${apiBase}/data/process/${projectName}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        process_chunk_size: 2048,
                        process_overlap_size: 64,
                        process_do_reset: true,
                        // process_file_id: null  // Process all files if null
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    // Success case
                    alert(`Processing succeeded. 
                    Processed ${result.num_files} files. 
                    Created ${result.num_chunks} chunks.`);
                } else {
                    // Error case
                    alert(result.signal || 'Processing failed');
                }
            } catch (error) {
                console.error('Process error:', error);
                alert('Error processing files');
            }
        });

        // Vectorize
        vectorizeBtn.addEventListener('click', async () => {
            const projectName = validateProjectName();
            if (!projectName) return;

            try {
                const response = await fetch(`${apiBase}/nlp/index/push/${projectName}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        do_reset: true
                    })
                });

                const result = await response.json();

                if (response.ok) {
                    alert(result.signal || 'Project vectorized successfully');
                } else {
                    alert(result.signal || 'Vectorization failed');
                }
            } catch (error) {
                console.error('Vectorize error:', error);
                alert('Error vectorizing project');
            }
        });

        // Chat functionality
        sendBtn.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });

        async function sendMessage() {
            const projectName = validateProjectName();
            if (!projectName) return;

            const messageText = chatInput.value.trim();
            if (!messageText) return;

            // Display user message
            const userMessageEl = document.createElement('div');
            userMessageEl.classList.add('user-message');
            userMessageEl.textContent = messageText;
            chatMessages.appendChild(userMessageEl);

            // Clear input
            chatInput.value = '';

            try {
                const response = await fetch(`${apiBase}/nlp/index/answer/${projectName}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        text: messageText,
                        limit: 4
                    })
                });

                const result = await response.json();

                // Display bot message
                const botMessageEl = document.createElement('div');
                botMessageEl.classList.add('bot-message');

                if (response.ok) {
                    // Sanitize and parse markdown
                    botMessageEl.innerHTML = DOMPurify.sanitize(marked.parse(result.answer || 'No response from the system.'));

                    // Optional: You might want to log or use additional information
                    console.log('Prompt used:', result.prompt);
                    console.log('Chat history:', result.chat_history);
                } else {
                    // Handle error case
                    botMessageEl.textContent = result.signal || 'Error processing your message.';
                }

                chatMessages.appendChild(botMessageEl);

                // Scroll to bottom
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } catch (error) {
                console.error('Chat error:', error);
                const errorMessageEl = document.createElement('div');
                errorMessageEl.classList.add('bot-message');
                errorMessageEl.textContent = 'Error processing your message.';
                chatMessages.appendChild(errorMessageEl);
            }
        }
    });
});