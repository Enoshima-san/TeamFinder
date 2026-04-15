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
        card.className = 'cardResp'
        card.innerHTML = `
        <p class="cardText">
            Пользователь ${data.userName} откликнулся на вашу заявку
          </p>
          <p class="contact">Способ связи: ${data.contact}</p>
        `;
        return card;
    }

    function createMyCard(data) {
        const card = document.createElement('div');
        card.className = 'cardResp'
        card.innerHTML = `
        <p class="cardText">
            Вы откликнулись на заявку пользователя ${data.userName}
          </p>
          <p class="contact">Способ связи: ${data.contact}</p>
        `;
        return card;
    }
    // Создание карточки рейтинга
    function createRating(data){
        const card = document.createElement("div");
        card.className = "player-card";
            card.innerHTML = `
          <div class="player-info">
            <span class="rank-number">${data.top}.</span>
            <div class="player-avatar">${data.nickName[0]}</div>
            <span>${data.nickName}</span>
          </div>
          <div class="player-rank">
            <span>${data.game}</span>
            <span>${data.rank}</span>
            <span>${data.role}</span>
          </div>
        `;
        return card;
    }

    // Асинхронная функция запроса откликов к серверу 
    async function loadResponces(){
        try {
            respBtn.disabled = true;
            myRespBtn.disabled = true;
            const response = await apiRequest('http://localhost:8000/resp-to-me'); // ! ЭНДПОИНТЫ !
            if (response.ok) {
                const adData = await response.json();

                const keys = Object.keys(adData.dbResults); // ! УКАЗАТЬ РЕАЛЬНЫЙ УЗЕЛ JSON !
                    
                if (keys != null)
                {   // Добавление объявлений по каждой штуке из массива
                    for (const key of keys) {
                        postsCont.appendChild(createCard(adData.dbResults[key]));
                    }
                }
                console.log('Результаты из БД:', adData.dbResults);
                
                respBtn.disabled = false;
                myRespBtn.disabled = false;
            } else {
                console.error('Ошибка при загрузке откликов');
                respBtn.disabled = false;
                myRespBtn.disabled = false;
            }
        } catch (error) {
            console.error('Ошибка при загрузке откликов:', error);
            respBtn.disabled = false;
            myRespBtn.disabled = false;
        }
    }

    // Загрузка откликов
    async function loadMyResponces(){
        try {
            respBtn.disabled = true;
            myRespBtn.disabled = true;
            const response = await apiRequest('http://localhost:8000/my-resp'); // ! ЭНДПОИНТЫ !
            if (response.ok) {
                const adData = await response.json();

                const keys = Object.keys(adData.dbResults); // ! УКАЗАТЬ РЕАЛЬНЫЙ УЗЕЛ JSON !
                    
                if (keys != null)
                {   // Добавление отлков по каждой штуке из массива
                    for (const key of keys) {
                        postsCont.appendChild(createMyCard(adData.dbResults[key]));
                    }
                }
                console.log('Результаты из БД:', adData.dbResults);
                respBtn.disabled = false;
                myRespBtn.disabled = false;
                
            } else {
                console.error('Ошибка при загрузке откликов');
                respBtn.disabled = false;
                myRespBtn.disabled = false;
            }
        } catch (error) {
            console.error('Ошибка при загрузке откликов:', error);
            respBtn.disabled = false;
            myRespBtn.disabled = false;
        }
    } 
    // Загрузка рейтинга игроков
    async function loadRating(){
        try {
            const response = await apiRequest('http://localhost:8000/rating'); // ! ЭНДПОИНТЫ !
            if (response.ok) {
                const adData = await response.json(); // ! ДАННЫЕ ДОЛЖНЫ БЫТЬ СОРТИРОВАНЫ ПО РЕЙТИНГУ В НИЗХОДЯЩЕМ ПОРЯДКЕ !

                const keys = Object.keys(adData.dbResults); // ! УКАЗАТЬ РЕАЛЬНЫЙ УЗЕЛ JSON !
                    
                if (keys != null)
                {   // Добавление отлков по каждой штуке из массива
                    for (const key of keys) {
                        ratingList.appendChild(createRating(adData.dbResults[key]));
                    }
                }
                console.log('Результаты из БД:', adData.dbResults);
                
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
        // Пример изменения аватара и ника (ВРЕМЕННО)
        const userData = {
            username: "Krasawa"
        }
        document.getElementById('userAvatar').textContent = userData.username.charAt(0).toUpperCase();
        document.getElementById('userNickName').textContent = userData.username;
        // Загрузка реальных данных пользователя с сервера
        loadUserData();
    }
    if (postsCont){
        removeAllChildren(postsCont); 
        // Пример откликов (ВРЕМЕННО)
        const adData = {
            userName: "RealChel",
            contact: "Max"
        };

        postsCont.appendChild(createCard(adData));
        loadResponces();
    }
    if (ratingList){
        // Пример рейтинга
        const data = {
            top: 1,
            nickName: "RandomChel",
            game: "Dota 2",
            rank: "2543",
            role: "support"
        }
        ratingList.appendChild(createRating(data));
        loadRating();       
    }

// Переключение на "Отклики"
    tabResponses?.addEventListener("click", () => {
      tabResponses.classList.add("active");
      tabMyResponses.classList.remove("active");
      removeAllChildren(postsCont); 
        // Пример откликов (ВРЕМЕННО)
        const adData = {
            userName: "RealChel",
            contact: "Max"
        };

        postsCont.appendChild(createCard(adData));
        loadResponces();
    });

// Переключение на "Мои отклики"
    tabMyResponses?.addEventListener("click", () => {
      tabMyResponses.classList.add("active");
      tabResponses.classList.remove("active");
      removeAllChildren(postsCont); 
        // Пример откликов (ВРЕМЕННО)
        const adData = {
            userName: "RealChel",
            contact: "Max"
        };

        postsCont.appendChild(createMyCard(adData));
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