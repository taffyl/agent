document.addEventListener('DOMContentLoaded', () => {
    const messagesArea = document.getElementById('messagesArea');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');
    
    // 后端 API 地址
    const API_URL = '/chat/stream'; 

    // 自动调整 textarea 高度
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if(this.value === '') this.style.height = '50px';
    });

    // 监听回车发送
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    async function sendMessage() {
        const prompt = userInput.value.trim();
        if (!prompt) return;

        // 1. 显示用户消息
        appendMessage('user', prompt);
        userInput.value = '';
        userInput.style.height = '50px';
        
        // 2. 禁用输入框和按钮
        setLoading(true);

        // 3. 创建 AI 消息占位符，显示“正在思考中”
        // 修改点：使用新的 HTML 结构显示转圈动画
        const aiMessageDiv = appendMessage('ai', `
            <div class="thinking-container">
                <div class="thinking-spinner"></div>
                <span>正在思考中...</span>
            </div>
        `);
        
        let fullResponse = "";
        let isFirstChunk = true; // 标记是否是第一个数据块

        try {
            // 4. 发起 fetch 请求
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: prompt })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // 5. 处理流式响应
            const reader = response.body.getReader();
            const decoder = new TextDecoder("utf-8");
            
            // 注意：这里不再立即清空 innerHTML，而是等到收到第一个有效数据时再清空

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value, { stream: true });
                
                // 解析 SSE 格式数据 (data: {...})
                const lines = chunk.split('\n');
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const dataStr = line.slice(6);
                        if (dataStr.trim() !== '[DONE]') {
                            // 修改点：如果是第一个数据块，清除“正在思考中”的状态
                            if (isFirstChunk) {
                                aiMessageDiv.innerHTML = "";
                                isFirstChunk = false;
                            }
                            fullResponse += dataStr;
                        }
                    } else if (line.trim() !== '') {
                         // 兼容非标准 SSE
                        if (isFirstChunk) {
                            aiMessageDiv.innerHTML = "";
                            isFirstChunk = false;
                        }
                        fullResponse += line;
                    }
                }

                // 实时渲染 Markdown
                // 只有当有实际内容时才渲染，避免清空加载动画后立即闪白
                if (!isFirstChunk || fullResponse.length > 0) {
                    aiMessageDiv.innerHTML = marked.parse(fullResponse);
                }
                
                scrollToBottom();
            }

        } catch (error) {
            console.error('Error:', error);
            // 出错时也清除加载状态并显示错误
            aiMessageDiv.innerHTML = `<span style="color:red;">请求失败: ${error.message}</span>`;
        } finally {
            setLoading(false);
            scrollToBottom();
        }
    }

    function appendMessage(role, content) {
        const div = document.createElement('div');
        div.className = `message ${role}`;
        if (role === 'ai') {
            div.innerHTML = content; 
        } else {
            div.textContent = content;
        }
        messagesArea.appendChild(div);
        scrollToBottom();
        return div;
    }

    function scrollToBottom() {
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    function setLoading(isLoading) {
        userInput.disabled = isLoading;
        sendBtn.disabled = isLoading;
        if (!isLoading) {
            userInput.focus();
        }
    }
});