/* document.addEventListener("DOMContentLoaded", function () {
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
    const profilePage = document.getElementById("profile-page");
    const hiddEditBtn = document.getElementById("hiddenEdit");


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

    // Ссылка на страницу профиля
    profilePage.addEventListener("click", () => {
        window.location.assign("profile.html");
    });

    // Выход из аккаунта
    logOutBtn.addEventListener("click", () => {
        // Удаление токена пользователя из текущей сессии
        sessionStorage.removeItem('token');
        window.location.assign("login.html");
    });

    // Ссылка на страницу настроек
    hiddEditBtn.addEventListener("click", () => {
        window.location.assign("settings.html");
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
*/
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

document.addEventListener("DOMContentLoaded", function () {
  const chatTabs = document.getElementById("chatTabs");
  const messagesContainer = document.getElementById("messages");
  const chatHeader = document.getElementById("chatHeader");
  const messageInput = document.getElementById("messageInput");
  const sideBar = document.querySelector(".sidebar");
  const feedPage = document.getElementById("feed-page");
  const respPage = document.getElementById("resp-page");
  const ratingPage = document.getElementById("rating-page");
  const logOutBtn = document.getElementById("logOutBtn");
  const chatsPage = document.getElementById("chats-page");
  const sendMsgBtn = document.getElementById("sendMsg-btn");

  let chats = [];
  let activeChatId = null;
  let socket = null;
  let currentUserId = null;

  chatsPage?.addEventListener("click", () =>
    window.location.assign("chat.html"),
  );
  respPage?.addEventListener("click", () =>
    window.location.assign("myResponces.html"),
  );
  ratingPage?.addEventListener("click", () =>
    window.location.assign("rating.html"),
  );
  feedPage?.addEventListener("click", () =>
    window.location.assign("feed.html"),
  );

  logOutBtn?.addEventListener("click", () => {
    sessionStorage.removeItem("token");
    if (socket) socket.close();
    window.location.assign("login.html");
  });

  async function apiRequest(url, options = {}) {
    const token = sessionStorage.getItem("token");
    if (token)
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`,
      };

    try {
      return await fetch(url, options);
    } catch (error) {
      console.error("Ошибка запроса:", error);
      alert("Ошибка запроса");
    }
  }

  function renderChatTabs() {
    chatTabs.innerHTML = "";
    chats.forEach((chat) => {
      const tab = document.createElement("div");
      tab.className = "chat-tab";
      if (chat.conversation_id === activeChatId) tab.classList.add("active");

      tab.textContent = `Чат ${chat.interlocutor}`;

      tab.onclick = () => openChat(chat.conversation_id);
      chatTabs.appendChild(tab);
    });
  }

  function renderMessages(messages) {
    messagesContainer.innerHTML = "";
    messages.forEach((msg) => {
      // Подстраиваем под формат БД (content, sender_id)
      addMessage({
        sender_id: msg.sender_id,
        content: msg.content,
      });
    });
  }

  function addMessage(msg) {
    const div = document.createElement("div");

    const isMine = msg.sender_id === currentUserId;
    div.className = "message " + (isMine ? "right" : "left");

    div.textContent = msg.content || msg.text;

    if (msg.created_at) {
      const time = new Date(msg.created_at).toLocaleTimeString();
      div.title = time;
    }

    messagesContainer.appendChild(div);
    scrollToBottom();
  }

  function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  async function openChat(conversation_id) {
    activeChatId = conversation_id;

    // Извлекаем ID объявления из хранилища
    const chat = chats.find((c) => c.conversation_id === conversation_id);
    if (!chat) {
      alert("Чат не найден в списке");
      console.error("Чат не найден в списке");
      return;
    }
    const annId = chat.announcement_id;

    // HTTP запрос истории
    try {
      const response = await apiRequest(
        `http://localhost:8000/chats/${conversation_id}`,
      );
      if (response.ok) {
        const data = await response.json();
        renderMessages(data.messages);
        chatHeader.textContent = `Чат: ${data.interlocutor}`;
      }
    } catch (e) {
      alert("Ошибка загрузки истории");
      console.error("Ошибка загрузки истории:", e);
    }

    // WebSocket соединение
    const token = sessionStorage.getItem("token").replace("Bearer ", "");

    // URL по схеме: /ws/chat/{ann_id}/{conv_id}
    const wsUrl = `ws://localhost:8000/ws/chat/${annId}/${conversation_id}?token=${token}`;

    if (socket) socket.close();
    socket = new WebSocket(wsUrl);
    setupWebSocketHandlers();

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "new_message") {
        addMessage(data);
      }
      if (data.type === "validation_error") {
        console.warn("Ошибка валидации:", data.message);
        alert(`⚠️ ${data.message}`);
      }
      if (data.type === "error") {
        console.error("Серверная ошибка:", data.message);
        alert(`❌ ${data.message}`);
      }
    };
  }

  async function loadChats() {
    try {
      const response = await apiRequest("http://localhost:8000/chats");
      if (response.ok) {
        const data = await response.json();

        chats = data.map((chat) => ({
          conversation_id: chat.conversation_id,
          announcement_id: chat.announcement_id,
          interlocutor: chat.interlocutor,
          last_message_at: chat.last_message_at,
        }));

        renderChatTabs();

        if (chats.length > 0 && !activeChatId) {
          openChat(chats[0].conversation_id, chats[0].interlocutor);
        }
      }
    } catch (e) {
      alert("Ошибка загрузки чатов");
      console.error("Ошибка загрузки чатов:", e);
    }
  }

  function reconnectWebSocket() {
    if (!activeChatId) return;

    // Находим чат, чтобы взять announcement_id
    const chat = chats.find((c) => c.conversation_id === activeChatId);
    if (!chat) {
      alert("Чат не найден для реконнекта");
      console.error("❌ Чат не найден для реконнекта");
      return;
    }

    const token = sessionStorage.getItem("token")?.replace("Bearer ", "");
    const wsUrl = `ws://localhost:8000/ws/chat/${chat.announcement_id}/${activeChatId}?token=${token}`;

    console.log("🔄 Reconnecting to:", wsUrl);

    // Закрываем старый сокет, если есть
    if (socket) {
      socket.onclose = null; // убираем старый обработчик, чтобы не было дублей
      socket.close();
    }

    // Создаём новый
    socket = new WebSocket(wsUrl);

    setupWebSocketHandlers(); // 👈 вынеси обработчики в отдельную функцию
  }

  function setupWebSocketHandlers() {
    socket.onopen = () => {
      console.log("✅ WebSocket connected");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "new_message") {
        addMessage(data);
      }
      if (data.type === "validation_error") {
        alert("Ошибка валидации");
        console.warn("⚠️ Validation error:", data.message);
      }
      if (data.type === "error") {
        alert("Ошибка сервера");
        console.error("❌ Server error:", data.message);
      }
    };

    socket.onerror = (error) => {
      console.error("❌ WebSocket error:", error);
    };

    socket.onclose = (event) => {
      console.log("🔌 WebSocket closed:", event.code, event.reason);
      // Не пытаемся реконнектить здесь, чтобы не было бесконечного цикла
      // Реконнект будет при следующей попытке отправить сообщение
    };
  }

  function sendMessage() {
    const text = messageInput.value.trim();
    if (!text || !activeChatId) return;

    // 🔹 1. Проверяем, жив ли сокет
    if (!socket || socket.readyState !== WebSocket.OPEN) {
      console.warn(
        "⚠️ WebSocket не активен (readyState:",
        socket?.readyState,
        ")",
      );

      // Пытаемся переподключиться
      reconnectWebSocket();

      // Если после реконнекта всё ещё не готов — откладываем
      if (!socket || socket.readyState !== WebSocket.OPEN) {
        console.error("❌ Не удалось отправить: сокет не готов");
        alert("⚠️ Соединение потеряно. Попробуйте отправить снова.");
        return;
      }
    }

    // 🔹 2. Отправляем в ПРАВИЛЬНОМ формате (как ждёт бэкенд!)
    // Бэкенд ждёт: { "content": "текст" }
    // НЕ надо: type, chatId, text — это лишнее
    socket.send(
      JSON.stringify({
        content: text, // ← только content!
      }),
    );

    console.log("✅ Message sent:", text);
    messageInput.value = "";
  }
  messageInput?.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
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
      const response = await apiRequest("http://localhost:8000/users/me");

      if (response.ok) {
        const userData = await response.json();
        currentUserId = userData.user_id || userData.id;
        if (document.querySelector(".user")) {
          document.getElementById("userAvatar").textContent = userData.username
            .charAt(0)
            .toUpperCase();

          document.getElementById("userNickName").textContent =
            userData.username;
        }
      }
    } catch (error) {
      alert("Ошибка пользователя")
      console.error("Ошибка пользователя:", error);
    }
  }

  if (sideBar) {
    loadUserData();
  }

  if (chatTabs) {
    // connectWebSocket();
    loadChats();
  }
});
