document.addEventListener("DOMContentLoaded", function () {
    const chatTabs = document.getElementById('chatTabs');
    const messagesContainer = document.getElementById('messages');
    const chatHeader = document.getElementById('chatHeader');
    const messageInput = document.getElementById('messageInput');
    const sideBar = document.querySelector('.sidebar');
    const feedPage = document.getElementById('feed-page');
    const respPage = document.getElementById('resp-page');
    const ratingPage = document.getElementById('rating-page');
    const logOutBtn = document.getElementById("logOutBtn");
    const chatsPage = document.getElementById("chats-page");
    const sendMsgBtn = document.getElementById("sendMsg-btn");

    let chats = []; // Массив чатов пользователя
    let activeChatId = null; // Текущий чат

    // Ссылка на страницу чата
    chatsPage.addEventListener("click", () => {
        window.location.assign("chat.html");
    });

    // Ссылка на страницу откликов
    respPage.addEventListener("click", () => {
        window.location.assign("myResponces.html");
    });

    // Ссылка на страницу рейтинга
    ratingPage.addEventListener("click", () => {
        window.location.assign("rating.html");
    });

    // Ссылка на страницу ленты
    feedPage.addEventListener("click", () => {
        window.location.assign("feed.html");
    });

    // Выход из аккаунта
    logOutBtn.addEventListener("click", () => {
        // Удаление токена пользователя из текущей сессии
        sessionStorage.removeItem('token');
        window.location.assign("login.html");
    });
    
    // Асинхронная функция запроса данных пользователя к серверу 
    async function loadUserData() {
        try {
            const response = await apiRequest('http://localhost:8000/users/me');
            if (response.ok) {
                const userData = await response.json();
                
                if(document.querySelector('.user')) {
                    document.getElementById('userAvatar').textContent = userData.username.charAt(0).toUpperCase();
                    document.getElementById('userNickName').textContent = userData.username;
                }
                console.log('Данные пользователя загружены:', userData);
            } else {
                console.error('Ошибка при загрузке данных пользователя');
            }
        } catch (error) {
            console.error('Ошибка при загрузке данных пользователя:', error);
        }
    }

   if (sideBar){
        // Пример изменения аватара и ника (ВРЕМЕННО)
        const userData = {
            username: "Krasawa"
        }
        document.getElementById('userAvatar').textContent = userData.username.charAt(0).toUpperCase();
        document.getElementById('userNickName').textContent = userData.username;
        // Загрузка реальных данных пользователя с сервера
        loadUserData();
    }

    // Функция для запросов с токеном авторизации
    async function apiRequest(url, options = {}) {
        const token = sessionStorage.getItem('token');
        console.log(token);
        if (token) options.headers = { ...options.headers, 'Authorization': `Bearer ${token}` };
        try{
            const response = await fetch(url, options);
            return response;
        }
        catch (error) {
            console.error('Ошибка авторизации:', error);
            return;
        }
    }

    // Функция для запросов с методом GET с токеном авторизации
    async function apiRequestPost(url, options = {}, data) {
        const token = sessionStorage.getItem('token');
        console.log(token);
        if (token) options.headers = { ...options.headers, 'Authorization': `Bearer ${token}` };
        options.method = 'POST';
        options.body = JSON.stringify(data);
        console.log(options)
        try{
            const response = await fetch(url, options);
            return response;
        }
        catch (error) {
            console.error('Ошибка авторизации:', error);
            return;
        }
    }

    // Функция создания вкладок чатов пользователя
    function renderChatTabs() {
        chatTabs.innerHTML = '';

        chats.forEach(chat => {
            const tab = document.createElement('div');
            tab.className = 'chat-tab';
            tab.textContent = '@' + chat.name;

            if (chat.id === activeChatId) {
                tab.classList.add('active');
            }

            tab.onclick = () => openChat(chat.id);

            chatTabs.appendChild(tab);
        });
    }

    // Функция создания сообщений пользователя
    function renderMessages(messages) {
        messagesContainer.innerHTML = '';

        messages.forEach(msg => {
            const div = document.createElement('div');
            div.className = 'message ' + (msg.isMine ? 'right' : 'left');
            div.textContent = msg.text;

            messagesContainer.appendChild(div);
        });

        scrollToBottom();
    }

    // Функция запроса определённого чата пользователя с сервера
    async function openChat(chatId) {
        activeChatId = chatId;
        renderChatTabs();

        try {
            const response = await apiRequest(`http://localhost:8000/users/me/chats/${chatId}`);

            if (response.ok) {
                const data = await response.json();

                renderMessages(data.messages);

                const chat = chats.find(c => c.id === chatId);
                chatHeader.textContent = 'Чат с @' + chat.name;
            }
        } catch (e) {
            console.error('Ошибка загрузки сообщений:', e);
        }
    }

    // Функция запроса всех чатов пользователя с сервера
    async function loadChats() {
        try {
            const response = await apiRequest('http://localhost:8000/users/me/chats');

            if (response.ok) {
                const data = await response.json();
                chats = data.chats;

                renderChatTabs();

                if (chats.length > 0) {
                    openChat(chats[0].id);
                }
            }
        } catch (e) {
            console.error('Ошибка загрузки чатов:', e);
        }
    }

    // Отправка сообщения пользователя в чат
    async function sendMessage() {
        const text = messageInput.value.trim();
        if (!text || !activeChatId) return;

        try {
            const response = await apiRequestPost(
                `http://localhost:8000/users/me/chats/${activeChatId}`,
                { headers: { 'Content-Type': 'application/json' } },
                { text }
            );

            if (response.ok) {
                messageInput.value = '';
                openChat(activeChatId); // Перезагрузка чата
            }
        } catch (e) {
            console.error('Ошибка отправки:', e);
        }
    }

    // Отправка сообщения по нажатию кнопки "Enter"
    messageInput.addEventListener('keypress', e => {
        if (e.key === 'Enter') sendMessage();
    });

    // Автоматический скрол вниз чата
    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Ссылка на страницу ленты
    sendMsgBtn.addEventListener("click", (e) => {
        try{
            sendMessage();
        }catch{
            console.error('Ошибка отправки:', e);
        };
    });

    // Загрузка чатов

    if (chatTabs) {
        loadChats();
    }

    document.addEventListener("click", (e) => {
            // Открыть меню аккаунта
        if (e.target.classList.contains("open-settings-btn")) {
            const sidebar = e.target.closest(".sidebar");
            const box = sidebar.querySelector(".account-box");
            // Открыть и закрыть скрытое меню
            box.classList.toggle("hidden");
        }
    });
});

// !!!!!! ПРИМЕР РАБОТЫ ЧАТА БЕЗ СЕРВЕРА !!!!!!
// !!! РАСКОММИТИТЬ ЕСЛИ НУЖНО ПОСМОТРЕТЬ ИНТЕРФЕЙС !!!
/**
// ДАННЫЕ
const chats = [
    {
        id: 1,
        name: "@Игрок1",
        messages: [
            { text: "Привет!", type: "left" },
            { text: "Го играть?", type: "right" }
        ]
    },
    {
        id: 2,
        name: "@Игрок2",
        messages: [
            { text: "Ты в команде?", type: "left" }
        ]
    },
    {
        id: 3,
        name: "@Игрок3",
        messages: []
    }
];

let activeChat = 0;

// РЕНДЕР ТАБОВ
function renderTabs() {
    const tabs = document.getElementById('chatTabs');
    tabs.innerHTML = '';

    chats.forEach((chat, index) => {
        const tab = document.createElement('div');
        tab.className = 'chat-tab' + (index === activeChat ? ' active' : '');
        tab.textContent = chat.name;

        tab.onclick = () => {
            activeChat = index;
            renderTabs();
            renderChat();
        };

        tabs.appendChild(tab);
    });
}

// РЕНДЕР ЧАТА
function renderChat() {
    const chat = chats[activeChat];
    document.getElementById('chatHeader').textContent = "Чат с " + chat.name;

    const messages = document.getElementById('messages');
    messages.innerHTML = '';

    chat.messages.forEach(msg => {
        const div = document.createElement('div');
        div.className = 'message ' + msg.type;
        div.textContent = msg.text;
        messages.appendChild(div);
    });

    scrollToBottom();
}

// ОТПРАВКА
function sendMessage() {
    const input = document.getElementById('messageInput');
    const text = input.value.trim();
    if (!text) return;

    chats[activeChat].messages.push({
        text,
        type: 'right'
    });

    input.value = '';
    renderChat();
}

// ENTER
document.getElementById('messageInput').addEventListener('keypress', e => {
    if (e.key === 'Enter') sendMessage();
});

function scrollToBottom() {
    const container = document.getElementById('messages');
    container.scrollTop = container.scrollHeight;
}

// INIT
renderTabs();
renderChat();
 */

// !!!! СКРИПТ ЧЕРЕЗ WEB SOCKET !!!!
/*
document.addEventListener("DOMContentLoaded", function () {
    const chatTabs = document.getElementById('chatTabs');
    const messagesContainer = document.getElementById('messages');
    const chatHeader = document.getElementById('chatHeader');
    const messageInput = document.getElementById('messageInput');
    const sideBar = document.querySelector('.sidebar');
    const feedPage = document.getElementById('feed-page');
    const respPage = document.getElementById('resp-page');
    const ratingPage = document.getElementById('rating-page');
    const logOutBtn = document.getElementById("logOutBtn");
    const chatsPage = document.getElementById("chats-page");
    const sendMsgBtn = document.getElementById("sendMsg-btn");

    let chats = [];
    let activeChatId = null;
    let socket = null;

    chatsPage?.addEventListener("click", () => window.location.assign("chat.html"));
    respPage?.addEventListener("click", () => window.location.assign("myResponces.html"));
    ratingPage?.addEventListener("click", () => window.location.assign("rating.html"));
    feedPage?.addEventListener("click", () => window.location.assign("feed.html"));

    logOutBtn?.addEventListener("click", () => {
        sessionStorage.removeItem('token');
        if (socket) socket.close();
        window.location.assign("login.html");
    });

    async function apiRequest(url, options = {}) {
        const token = sessionStorage.getItem('token');
        if (token) options.headers = { ...options.headers, 'Authorization': `Bearer ${token}` };

        try {
            return await fetch(url, options);
        } catch (error) {
            console.error('Ошибка запроса:', error);
        }
    }

    //  WEBSOCKET 
    function connectWebSocket() {
        const token = sessionStorage.getItem('token');

        socket = new WebSocket(`ws://localhost:8000/ws?token=${token}`);

        socket.onopen = () => {
            console.log('WebSocket подключен');
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);

            // Новое сообщение
            if (data.type === 'message') {
                if (data.chatId === activeChatId) {
                    addMessage(data.message);
                }
            }

            // История чата
            if (data.type === 'history') {
                renderMessages(data.messages);
            }

            // Обновление чатов
            if (data.type === 'chats') {
                chats = data.chats;
                renderChatTabs();
            }
        };

        socket.onclose = () => {
            console.log('WebSocket закрыт');
        };

        socket.onerror = (error) => {
            console.error('WebSocket ошибка:', error);
        };
    }

    function renderChatTabs() {
        chatTabs.innerHTML = '';

        chats.forEach(chat => {
            const tab = document.createElement('div');
            tab.className = 'chat-tab';
            tab.textContent = '@' + chat.name;

            if (chat.id === activeChatId) {
                tab.classList.add('active');
            }

            tab.onclick = () => openChat(chat.id);

            chatTabs.appendChild(tab);
        });
    }

    function renderMessages(messages) {
        messagesContainer.innerHTML = '';

        messages.forEach(msg => addMessage(msg));
    }

    function addMessage(msg) {
        const div = document.createElement('div');
        div.className = 'message ' + (msg.isMine ? 'right' : 'left');
        div.textContent = msg.text;

        messagesContainer.appendChild(div);
        scrollToBottom();
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function openChat(chatId) {
        activeChatId = chatId;
        renderChatTabs();
        messagesContainer.innerHTML = '';

        // подписка на чат
        socket.send(JSON.stringify({
            type: 'join',
            chatId: chatId
        }));

        const chat = chats.find(c => c.id === chatId);
        chatHeader.textContent = 'Чат с @' + chat.name;
    }

    async function loadChats() {
        try {
            const response = await apiRequest('http://localhost:8000/users/me/chats');

            if (response.ok) {
                const data = await response.json();
                chats = data.chats;

                renderChatTabs();

                if (chats.length > 0) {
                    openChat(chats[0].id);
                }
            }
        } catch (e) {
            console.error('Ошибка загрузки чатов:', e);
        }
    }

    function sendMessage() {
        const text = messageInput.value.trim();
        if (!text || !activeChatId || !socket) return;

        socket.send(JSON.stringify({
            type: 'message',
            chatId: activeChatId,
            text: text
        }));

        messageInput.value = '';
    }

    messageInput?.addEventListener('keypress', e => {
        if (e.key === 'Enter') sendMessage();
    });

    sendMsgBtn?.addEventListener("click", () => {
        sendMessage();
    });

    document.addEventListener("click", (e) => {
        if (e.target.classList.contains("open-settings-btn")) {
            const sidebar = e.target.closest(".sidebar");
            const box = sidebar.querySelector(".account-box");
            box.classList.toggle("hidden");
        }
    });

    async function loadUserData() {
        try {
            const response = await apiRequest('http://localhost:8000/users/me');

            if (response.ok) {
                const userData = await response.json();

                if (document.querySelector('.user')) {
                    document.getElementById('userAvatar').textContent =
                        userData.username.charAt(0).toUpperCase();

                    document.getElementById('userNickName').textContent =
                        userData.username;
                }
            }
        } catch (error) {
            console.error('Ошибка пользователя:', error);
        }
    }

    if (sideBar) {
        loadUserData();
    }

    if (chatTabs) {
        connectWebSocket();
        loadChats();       
    }
});
*/