document.addEventListener("DOMContentLoaded", function () {

    const logOutBtn = document.getElementById("logOutBtn");
    const sideBar = document.querySelector('.sidebar')
    const buttonSaveSetting = document.getElementById("save-btn-setting");
    

    // Выход из аккаунта
    logOutBtn.addEventListener("click", () => {
        // Удаление токена пользователя из текущей сессии
        sessionStorage.removeItem('token');
        window.location.assign("login.html");
    });

    // Функция для запросов с токеном авторизации
    async function apiRequest(url, options = {}) {
        const token = sessionStorage.getItem('token');
        console.log(token);
        if (token) options.headers = { ...options.headers, 'Authorization': `Bearer ${token}` }; // ! ИЗМЕНИТЬ НА НЕОБХОДИМЫЕ ПАРАМЕТРЫ ЗАПРОСА !
        try{
            const response = await fetch(url, options);
            return response;
        }
        catch (error) {
            console.error('Ошибка авторизации:', error);
            return;
        }
    }

    // Асинхронная функция запроса данных пользователя к серверу 
    async function loadUserData() {
        try {
            const response = await apiRequest('http://localhost:8000/user-data'); // ! ЗАГЛУШКА - ДОБАВИТЬ АКТУАЛЬНЫЙ ЭНДПОИНТ !
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

    document.addEventListener("click", (e) => {

        // Открыть форму контактов
            // Открыть меню аккаунта
        if (e.target.classList.contains("open-settings-btn")) {
            const sidebar = e.target.closest(".sidebar");
            const box = sidebar.querySelector(".account-box");
            // Открыть и закрыть скрытое меню
            box.classList.toggle("hidden");
        }
    });

    document
    .getElementById("SettingForm")
    ?.addEventListener("submit", async function (e) {
        e.preventDefault();

        const nickname = document.getElementById("nickname").value;
        const description = document.getElementById("description").value;
        // Требование данных
        if (nickname == "") {
          alert("Ник пользователя не может быть пустым");
          return;
        }
        // Формирование пакета данных пользователя
        const data = {
          username: nickname,
          description: description,
         };
        // Попытка отправки данных на сервер
        try {
        // Формирование запроса
         const response = await fetch("http://localhost:8000/auth/Setting", {
            method: "POST",
            headers: {
            "Content-Type": "application/json;charset=utf-8",
            },
            body: JSON.stringify(data),
        });
        // Ожидание ответа от сервера
        const result = await response.json();
         // Проверка ответа от сервера
         if (response.ok) {
           alert("Сохранено");
         } else {
         alert("Ошибка");
        }
        alert(result.message);
         // Вывод ошибки
        } catch (error) {
         alert("Ошибка соединения с сервером");
         console.error(error);
        }
    });

    // Сохранение настроек
    buttonSaveSetting?.addEventListener("click", async function () {

        const nickname = document.getElementById("nickname").value;
        const description = document.getElementById("description").value;
        // Требование данных
        if (nickname == "") {
         alert("Ник пользователя не может быть пустым");
        return;
        }
        // Формирование пакета данных пользователя
        const data = {
            username: nickname,
            description: description,
        };
        // Попытка отправки данных на сервер
        try {
        // Формирование запроса
        const response = await fetch("http://localhost:8000/auth/Setting", {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
            },
            body: JSON.stringify(data),
        });
        // Ожидание ответа от сервера
        const result = await response.json();
        // Проверка ответа от сервера
        if (response.ok) {
            alert("Сохранено");
        } else {
            alert("Ошибка");
        }
        alert(result.message);
        // Вывод ошибки
        } catch (error) {
            alert("Ошибка соединения с сервером");
            console.error(error);
        }    
    });
});
