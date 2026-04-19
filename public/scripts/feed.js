document.addEventListener("DOMContentLoaded", function () {

    const addBtn = document.getElementById("addPostBtn");
    const filterBtn = document.getElementById("filterBtn");
    const logOutBtn = document.getElementById("logOutBtn");
    const postsCont = document.querySelector('.posts');
    const sideBar = document.querySelector('.sidebar');
    const feedPage = document.getElementById('feed-page');
    const respPage = document.getElementById('resp-page');
    const ratingPage = document.getElementById('rating-page');
    const chatsPage = document.getElementById("chats-page");
    const profilePage = document.getElementById("profile-page");
    const hiddEditBtn = document.getElementById("hiddenEdit");

    // Ссылка на страницу фильтра
    filterBtn.addEventListener("click", () => {
        window.location.assign("feedFilter.html");
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

    // Ссылка на страницу ленты
    feedPage.addEventListener("click", () => {
        window.location.assign("feed.html");
    });

    // Ссылка на страницу добавления объявления
    addBtn.addEventListener("click", () => {
        window.location.assign("feedAdd.html");
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

    // Функция для запросов с методом GET с токеном авторизации
    async function apiRequestPost(url, options = {}, data) {
        const token = sessionStorage.getItem('token');
        console.log(token);
        if (token) options.headers = { ...options.headers, 'Authorization': `Bearer ${token}`, "Content-Type": "application/json;charset=utf-8"};
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

    // Функция создания карточки объявления
    function createCard(data) { // ! УКАЗАТЬ РЕАЛЬНЫЕ УЗЛЫ JSON !
        const card = document.createElement('div');
        card.className = 'card'
        card.innerHTML = `
        <div class="card-header">
            <div class="postId hidden">${data.postId}</div>
            <div class="avatar post">${data.userName[0].toUpperCase()}</div>
            <span>${data.userName}</span>
        </div>

        <p>
            ${data.description}
        </p>

        <div id="gameTags" class="tags">
            ${data.games.map(game => `<span>${game}</span>`).join('')}
        </div>

        <p class="requirements-title">Требования:</p>

        <div class="tags">
            <span id="ageFromTag">Возраст от ${data.ageFrom}</span>
            <span id="ageToTag">Возраст до ${data.ageTo}</span>
            <span id="microTag">Наличие микрофона : ${data.micro}</span>
        </div>

        <div class="response-box hidden">
            <p>Сообщите удобный способ связи с вами</p>
            <textarea placeholder="Например: Discord, Telegram..."></textarea>
            <button class="send-btn">Отправить</button>
        </div>

        <button class="apply-btn">Откликнуться</button>
        `;


        return card;
    }

    // Функция фильтрации
    function filterPosts(filter) {
        const cards = document.querySelectorAll('.card');

        cards.forEach(card => {
            // Получение текстовых данных
            const gameTagsElements = card.querySelectorAll('#gameTags span');
            const gamesArray = Array.from(gameTagsElements).map(span => span.innerText.trim());
            // Извлечение возраста из тегов
            const ageFromText = card.querySelector('#ageFromTag').innerText;
            const ageFromValue = parseInt(ageFromText.replace(/\D/g, '')) || 0;

            const ageToText = card.querySelector('#ageToTag').innerText;
            const ageToValue = parseInt(ageToText.replace(/\D/g, '')) || 0;
            // Проверерка наличия микрофона по тексту тега
            const microText = card.querySelector('#microTag').innerText.toLowerCase();
            const hasMicro = microText.includes('обязательно')

            // Логика фильтрации:
            const matchesGame =  filter.games.length === 0 || gamesArray.some(game => filter.games.includes(game));
            const matchesAgeFrom = !filter.ageFrom || ageFromValue >= parseInt(filter.ageFrom);
            const matchesAgeTo = !filter.ageTo || ageToValue <= parseInt(filter.ageTo);
            const matchesMicro =  hasMicro;
            // Показать или скрыть
            if (matchesGame && matchesAgeFrom && matchesAgeTo && matchesMicro) {
                card.style.display = "block";
            } else {
                card.style.display = "none";
            }
        });
    }
    // Асинхронная функция запроса объявлений к серверу 
    async function loadAdvertisement(){
        try {
            // Запрос всех объявлений с сервера
            const response = await apiRequest('http://localhost:8000/a');
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
                
            } else {
                console.error('Ошибка при загрузке объявлений');
            }
        } catch (error) {
            console.error('Ошибка при загрузке объявлений:', error);
        }
    }

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

    // Добавление объявлений при загрузке страницы ленты
    if (postsCont){
        removeAllChildren(postsCont); 
        // Пример объявлений (ВРЕМЕННО)
        const adData = {
            postId: "sdaw23",
            userName: "GamerPro",
            description: "Ищем тиммейта в команду, время с 20:00 до 24:00",
            games: ["Dota 2", "CS2"],
            ageFrom: '10',
            ageTo: '30',
            micro: 'обязательно'
        };
        // Пример фильтра (ВРЕМЕННО)
        const filterExample = {
            games: ["Dota 2"],
            ageFrom: '10',
            ageTo: '35',
            micro: 'обязательно'
        };
        postsCont.appendChild(createCard(adData));
        const retrievedFilter = JSON.parse(sessionStorage.getItem("filterTags"));
        // Проверка фильтра
        if (retrievedFilter){filterPosts(retrievedFilter)}
        else{filterPosts(filterExample)}
        loadAdvertisement();
    }

    document.addEventListener("click", async (e) => {

        // Открыть форму контактов
        if (e.target.classList.contains("apply-btn")) {
            const card = e.target.closest(".card");
            const box = card.querySelector(".response-box");

            // Закрыть другие формы контактов
            document.querySelectorAll(".response-box").forEach(b => {
              if (b !== box) b.classList.add("hidden");
            });

            box.classList.toggle("hidden");
        }

        // Отправка отклика
        if (e.target.classList.contains("send-btn")) {
            const card = e.target.closest(".card");
            const textarea = card.querySelector("textarea");
            const applyBtn = card.querySelector(".apply-btn");
            const sendBtn = card.querySelector(".send-btn");
            const postId = card.querySelector(".postId");

            // Проверка на заполнение формы
            if (textarea.value.trim() === "") {
              alert("Введите контакт!");
              return;
            }
            sendBtn.disabled = true;
            // Данные об отклике
            const data = {
                userName: document.getElementById('userNickName').textContent,
                postId: postId.textContent,
                connection: textarea.value 
            }
            console.log(data);
            try {
            const response = await apiRequestPost('http://localhost:8000/resp-to-post', {}, data); // ! СМЕНИТЬ ЭНДПОИНТ !
            if (response.ok) {
                card.querySelector(".response-box").classList.add("hidden");
                applyBtn.textContent = "Отклик отправлен";
                applyBtn.disabled = true;
            } else {
                sendBtn.disabled = false;
                console.error('Ошибка при отправке отклика');
            }
            } catch (error) {
                sendBtn.disabled = false;
                console.error('Ошибка при отправке отклика:', error);
            }
        }

            // Открыть меню аккаунта
        if (e.target.classList.contains("open-settings-btn")) {
            const sidebar = e.target.closest(".sidebar");
            const box = sidebar.querySelector(".account-box");
            // Открыть и закрыть скрытое меню
            box.classList.toggle("hidden");
        }
    });

});