document.addEventListener("DOMContentLoaded", function () {
    const tabResponses = document.getElementById("tabResponses");
    const tabMyResponses = document.getElementById("tabMyResponses");
    const sideBar = document.querySelector('.sidebar');
    const feedPage = document.getElementById('feed-page');
    const postsCont = document.querySelector('.resp-cont');
    const respBtn = document.getElementById('tabResponses');
    const myRespBtn = document.getElementById('tabMyResponses');
    const respPage = document.getElementById('resp-page');
    const ratingList = document.getElementById("players-list");
    const ratingPage = document.getElementById('rating-page');
    const chatsPage = document.getElementById("chats-page");
    const logOutBtn = document.getElementById("logOutBtn");
    const profilePage = document.getElementById("profile-page");
    const hiddEditBtn = document.getElementById("hiddenEdit");

    // Ссылка на страницу ленты
    feedPage.addEventListener("click", () => {
        window.location.assign("feed.html");
    });

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

    // Функция удаления всех подузлов указанного узла
    function removeAllChildren(parentElement) {
        while (parentElement.firstChild) {
            parentElement.removeChild(parentElement.firstChild);
        }
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

    // Создание карточек откликов
    function createCard(data) {
        const card = document.createElement('div');
        card.className = 'cardResp';
        const userId = data.user_id;
        const status = data.status || "Ожидает";

        card.innerHTML = `
          <p class="cardText">
            Отклик на объявление: <strong>${data.announcement_id}</strong>
          </p>
          <p class="contact">Статус: ${status}</p>
          <p class="contact">ID пользователя: ${userId}</p>
        `;
        return card;
    }

    function createMyCard(data) {
        const card = document.createElement('div');
        card.className = 'cardResp';
        const userId = data.user_id;
        const status = data.status || "Ожидает";

        card.innerHTML = `
          <p class="cardText">
            Вы откликнулись на объявление: <strong>${data.announcement_id}</strong>
          </p>
          <p class="contact">Статус: ${status}</p>
          <p class="contact">ID пользователя: ${userId}</p>
        `;
        return card;
    }
    // Создание карточки рейтинга
    function createRating(data, index) {
        const card = document.createElement("div");
        card.className = "player-card";
        const nick = data.nickname || "Unknown";
        const firstLetter = nick[0] || "?";
        const rank = index + 1;
        const discipline = data.disclipline ? data.disclipline[0] : "Dota 2";

        card.innerHTML = `
          <div class="player-info">
            <span class="rank-number">${rank}.</span>
            <div class="player-avatar">${firstLetter}</div>
            <span>${nick}</span>
          </div>
          <div class="player-rank">
            <span>${discipline}</span>
            <span>${data.total_money || "$ 0"}</span>
            <span>Побед: ${data.stats?.wins || 0}</span>
          </div>
        `;
        return card;
    }

    // Асинхронная функция запроса откликов к серверу 
    async function loadResponces() {
        const storedIds = JSON.parse(sessionStorage.getItem('respondedMyPosts')) || [];
        console.log("ID в хранилище:", storedIds);

        if (storedIds.length === 0) {
            console.warn("Хранилище пустое");
            return;
        }

        try {
            postsCont.innerHTML = '';
            for (const annId of storedIds) {
                console.log(`Запрос для ID: ${annId}`);
                const response = await apiRequest(`http://localhost:8000/a/${annId}/responses/`);

                if (response.ok) {
                    const responses = await response.json();
                    console.log(`Ответ сервера для ${annId}:`, responses);

                    if (Array.isArray(responses) && responses.length > 0) {
                        responses.forEach(item => {
                            postsCont.appendChild(createCard(item));
                        });
                    } else {
                        console.log(`Для ID ${annId} откликов не найдено (массив пуст)`);
                    }
                } else {
                    console.error(`Сервер вернул ошибку ${response.status} для ID ${annId}`);
                }
            }
        } catch (error) {
            console.error('Критическая ошибка:', error);
        }
    }


    // Загрузка откликов
    async function loadMyResponces(){
        const storedIds = JSON.parse(sessionStorage.getItem('respondedPosts')) || [];

        if (storedIds.length === 0) {
            postsCont.innerHTML = '<p>Вы еще не взаимодействовали с объявлениями.</p>';
            return;
        }

        try {
            postsCont.innerHTML = '';

            for (const annId of storedIds) {
                const response = await apiRequest(`http://localhost:8000/a/${annId}/responses/`);

                if (response.ok) {
                    const responses = await response.json();
                    console.log(responses);

                    if (Array.isArray(responses)) {
                        responses.forEach(item => {
                            console.log(item);
                            postsCont.appendChild(createMyCard(item));
                        });
                    }
                }
            }
        } catch (error) {
            console.error('Ошибка при загрузке откликов из хранилища:', error);
        }
    } 
    // Загрузка рейтинга игроков
    async function loadRating(){
        try {
            const response = await apiRequest('http://localhost:8000/api/external/cyber-sport-ru/dota-2');
            if (response.ok) {
                const data = await response.json(); 
                ratingList.innerHTML = '';
                if (Array.isArray(data)) {
                    data.forEach((player, index) => {
                        ratingList.appendChild(createRating(player, index));
                    });
                }

                console.log('Результаты загружены:', data);
                
            } else {
                console.error('Ошибка при загрузке рейтинга');
            }
        } catch (error) {
            console.error('Ошибка при загрузке рейтинга:', error);
        }
    }    
    // Подгрузка данных сайдбара
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
        // Загрузка реальных данных пользователя с сервера
        loadUserData();
    }
    if (postsCont){
        loadResponces();
    }
    if (ratingList){
        loadRating();       
    }

// Переключение на "Отклики"
    tabResponses?.addEventListener("click", () => {
      tabResponses.classList.add("active");
      tabMyResponses.classList.remove("active");
      removeAllChildren(postsCont); 
        loadResponces();
    });

// Переключение на "Мои отклики"
    tabMyResponses?.addEventListener("click", () => {
      tabMyResponses.classList.add("active");
      tabResponses.classList.remove("active");
      removeAllChildren(postsCont); 
        loadMyResponces();
    });

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