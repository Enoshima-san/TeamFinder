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
            alert('Ошибка авторизации');
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
            alert('Ошибка авторизации');
            console.error('Ошибка авторизации:', error);
            return;
        }
    }

    // Функция создания карточки объявления
    function createCard(data) {
        const card = document.createElement('div');
        card.className = 'card';
        
        const respondedPosts = JSON.parse(sessionStorage.getItem('respondedPosts')) || [];
        const respondedMyPosts = JSON.parse(sessionStorage.getItem('respondedMyPosts')) || [];
        
        const isInteracted = respondedPosts.includes(data.announcement_id) || 
                             respondedMyPosts.includes(data.announcement_id);

        const applyBtnClass = isInteracted ? 'apply-btn hidden' : 'apply-btn';

        const username = data.user.username;
        const gameName = data.game.game_name;
        const micStatus = data.user.has_microphone ? "Есть" : "Нет";

        card.innerHTML = `
        <div class="card-header">
            <div class="postId hidden">${data.announcement_id}</div>
            <div class="avatar post">${username[0].toUpperCase()}</div>
            <span>${username}</span>
        </div>

        <p>${data.description || "Нет описания"}</p>

        <div id="gameTags" class="tags">
            <span>${gameName}</span>
        </div>

        <p class="requirements-title">Требования:</p>

        <div class="tags">
            <span id="ageFromTag">Возраст от ${data.rank_min}</span>
            <span id="ageToTag">Возраст до ${data.rank_max}</span>
            <span id="microTag">Микрофон: ${micStatus}</span>
        </div>

        <div class="response-box hidden">
            <p>Сообщите удобный способ связи с вами</p>
            <textarea placeholder="Например: Discord, Telegram..."></textarea>
            <button class="send-btn">Отправить</button>
        </div>

        <button class="${applyBtnClass}">Откликнуться</button>
        `;
        return card;
    }

    // Функция фильтрации
    function filterPosts(filter) {
     const cards = document.querySelectorAll('.card');
     const filterGamesLower = filter.games.map(g => g.toLowerCase());

     cards.forEach(card => {
         const gameTagsElements = card.querySelectorAll('#gameTags span');
         const gamesArray = Array.from(gameTagsElements).map(span => span.innerText.trim().toLowerCase());

         const ageFromValue = parseInt(card.querySelector('#ageFromTag').innerText.replace(/\D/g, '')) || 0;
         const ageToValue = parseInt(card.querySelector('#ageToTag').innerText.replace(/\D/g, '')) || 0;

         const microText = card.querySelector('#microTag').innerText.toLowerCase();
         const hasMicroInCard = microText.includes('есть') || microText.includes('да');

         const matchesGame = filterGamesLower.length === 0 || 
                             gamesArray.some(game => filterGamesLower.includes(game));

         const matchesAgeFrom = !filter.ageFrom || ageFromValue >= parseInt(filter.ageFrom);
         const matchesAgeTo = !filter.ageTo || ageToValue <= parseInt(filter.ageTo);
        
         const filterMicroRequired = filter.micro === 'Обязательно';
         const matchesMicro = !filterMicroRequired || hasMicroInCard;

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
                postsCont.innerHTML = '';
                adData.forEach(ad => {
                    postsCont.appendChild(createCard(ad));
                });
                const retrievedFilter = JSON.parse(sessionStorage.getItem("filterTags"));
                // Проверка фильтра
                if (retrievedFilter){filterPosts(retrievedFilter)}
                console.log('Объявления загружены:', adData);
                
            } else {
                alert('Ошибка при загрузке объявлений');
                console.error('Ошибка при загрузке объявлений');
            }
        } catch (error) {
            alert('Ошибка при загрузке объявлений');
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
                alert('Ошибка при загрузке данных пользователя');
                console.error('Ошибка при загрузке данных пользователя');
            }
        } catch (error) {
            alert('Ошибка при загрузке данных пользователя');
            console.error('Ошибка при загрузке данных пользователя:', error);
        }
    }

    if (sideBar){
        // Загрузка реальных данных пользователя с сервера
        loadUserData();
    }

    // Добавление объявлений при загрузке страницы ленты
    if (postsCont){
        removeAllChildren(postsCont); 
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
            const postIdElement = card.querySelector(".postId");
            const postId = postIdElement.textContent; // Получаем ID поста
        
            // Проверка на заполнение формы
            if (textarea.value.trim() === "") {
                alert("Введите контакт!");
                return;
            }
            sendBtn.disabled = true;
            // Данные об отклике
            const data = {
                message: textarea.value 
            };
        
            try {
                const response = await apiRequestPost(`http://localhost:8000/a/${postId}/responses/new`, {}, data);

                if (response.ok) {
                    // Получаем текущий список из хранилища или создаем новый
                    let respondedPosts = JSON.parse(sessionStorage.getItem('respondedPosts')) || [];

                    // Добавляем ID, если его там еще нет
                    if (!respondedPosts.includes(postId)) {
                        respondedPosts.push(postId);
                        // Сохраняем обратно в sessionStorage
                        sessionStorage.setItem('respondedPosts', JSON.stringify(respondedPosts));
                    }                
                    card.querySelector(".response-box").classList.add("hidden");
                    applyBtn.textContent = "Отклик отправлен";
                    applyBtn.disabled = true;
                    applyBtn.classList.remove("hidden");
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