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
    sessionStorage.removeItem("filterTags");
    sessionStorage.removeItem("respondedPosts");
    sessionStorage.removeItem("respondedMyPosts");
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
        alert(`${data.message}`);
      }
      if (data.type === "error") {
        console.error("Серверная ошибка:", data.message);
        alert(`${data.message}`);
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

    const chat = chats.find((c) => c.conversation_id === activeChatId);
    if (!chat) {
      alert("Чат не найден для реконнекта");
      console.error("Чат не найден для реконнекта");
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

    setupWebSocketHandlers();
  }

  function setupWebSocketHandlers() {
    socket.onopen = () => {
      console.log("WebSocket connected");
    };

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "new_message") {
        addMessage(data);
      }
      if (data.type === "validation_error") {
        alert("Ошибка валидации");
        console.warn("Validation error:", data.message);
      }
      if (data.type === "error") {
        alert("Ошибка сервера");
        console.error("Server error:", data.message);
      }
    };

    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    socket.onclose = (event) => {
      console.log("WebSocket closed:", event.code, event.reason);
    };
  }

  function sendMessage() {
    const text = messageInput.value.trim();
    if (!text || !activeChatId) return;

    if (!socket || socket.readyState !== WebSocket.OPEN) {
      console.warn(
        "WebSocket не активен (readyState:",
        socket?.readyState,
        ")",
      );

      // Пытаемся переподключиться
      reconnectWebSocket();

      // Если после реконнекта всё ещё не готов — откладываем
      if (!socket || socket.readyState !== WebSocket.OPEN) {
        console.error("Не удалось отправить: сокет не готов");
        alert("Соединение потеряно. Попробуйте отправить снова.");
        return;
      }
    }

    socket.send(
      JSON.stringify({
        content: text,
      }),
    );

    console.log("Message sent:", text);
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
    loadChats();
  }
});
