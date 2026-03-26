document.addEventListener("DOMContentLoaded", function () {

    const addBtn = document.getElementById("addPostBtn");
    const filterBtn = document.getElementById("filterBtn");
    const logOutBtn = document.getElementById("logOutBtn");
    const postsCont = document.querySelector('.posts')
    const sideBar = document.querySelector('.sidebar')

    // Ссылка на страницу фильтра
    filterBtn.addEventListener("click", () => {
        window.location.assign("TEST.html");
    });

    // Ссылка на страницу добавления объявления
    addBtn.addEventListener("click", () => {
        window.location.assign("feedAdd.html");
    });

    // Выход из аккаунта
    logOutBtn.addEventListener("click", () => {
        // Удаление токена пользователя из текущей сессии
        sessionStorage.removeItem('token');
        window.location.assign("login.html");
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

    // Функция создания карточки объявления
    function createCard(data) { // ! УКАЗАТЬ РЕАЛЬНЫЕ УЗЛЫ JSON !
        const card = document.createElement('div');
        card.className = 'card';

        // Шапка (Аватар и ник)
        const header = document.createElement('div');
        header.className = 'card-header';

        const avatar = document.createElement('div');
        avatar.className = 'avatar post';

        avatar.textContent = data.userName.charAt(0).toUpperCase();
        const nameSpan = document.createElement('span');

        nameSpan.textContent = data.userName;

        header.append(avatar, nameSpan);

        // Основное описание
        const desc = document.createElement('p');
        const firstLine = document.createTextNode(data.description);
        // Создаем элемент переноса строки
        const br = document.createElement('br');
        // Вторая строка текста
        const roleValue = document.createTextNode(`Основная роль: ${data.role}`);

        // Собираем параграф из узлов
        desc.append(firstLine, br, roleValue);

        // Теги игр (вспомогательная функция для создания списка тегов)
        const createTagBox = (items) => {
            const box = document.createElement('div');
            box.className = 'tags';
            items.forEach(text => {
                const span = document.createElement('span');
                span.textContent = text;
                box.appendChild(span);
            });
            return box;
        };

        const gameTags = createTagBox(data.games);

        // Требования
        const reqTitle = document.createElement('p');
        reqTitle.className = 'requirements-title';
        reqTitle.textContent = 'Требования:';

        const reqTags = createTagBox(data.requirements);

        // Блок ответа (Response Box)
        const responseBox = document.createElement('div');
        responseBox.className = 'response-box hidden';

        const responseText = document.createElement('p');
        responseText.textContent = 'Сообщите удобный способ связи с вами';

        const textarea = document.createElement('textarea');
        textarea.placeholder = 'Например: Discord, Telegram...';

        const sendBtn = document.createElement('button');
        sendBtn.className = 'send-btn';
        sendBtn.textContent = 'Отправить';

        responseBox.append(responseText, textarea, sendBtn);

        // Кнопка "Откликнуться"
        const applyBtn = document.createElement('button');
        applyBtn.className = 'apply-btn';
        applyBtn.textContent = 'Откликнуться';

        // Сборка всей карточки
        card.append(header, desc, gameTags, reqTitle, reqTags, responseBox, applyBtn);

        return card;
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
                        container.appendChild(createCard(adData.dbResults[key]));
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
                    document.getElementById('userAvatar').textContent = userData.username.charAt(0).toUpperCase(); // ! УКАЗАТЬ РЕАЛЬНЫЙ УЗЕЛ JSON !
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
            userName: "GamerPro",
            description: "Ищем тиммейта в команду, время с 20:00 до 24:00",
            role: "саппорт",
            games: ["Dota 2", "CS2"],
            requirements: ["18+", "Микрофон"]
        };
        postsCont.appendChild(createCard(adData));
        // Добавлений через запрос к серверу
        loadAdvertisement();
    }

    document.addEventListener("click", (e) => {

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

            // Проверка на заполнение формы
            if (textarea.value.trim() === "") {
              alert("Введите контакт!");
              return;
            }

            applyBtn.textContent = "Отклик отправлен";
            applyBtn.disabled = true;

            // Закрыть текущею форму контактов
            card.querySelector(".response-box").classList.add("hidden");
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