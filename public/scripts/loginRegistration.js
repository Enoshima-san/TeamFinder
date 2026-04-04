// Страница входа пользователя
document
  .getElementById("loginForm")
  ?.addEventListener("submit", async function (e) {
    e.preventDefault();

    const login = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    // Требование данных
    if (login === "" || password === "") {
      alert("Введите логин и пароль");
      return;
    }
    // Формирование пакета данных пользователя
    const data = {
      login: login,
      password: password,
    };
    // Попытка отправки данных на сервер
    try {
      // Формирование запроса
      const response = await fetch("http://localhost:8000/auth/login", {
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
        // Сохранение токена на текущею сессию
        sessionStorage.setItem("token", result.access_token);
        alert("Авторизация завершена");
        // Переход на новую страницу
        window.location.assign("feed.html");
      } else {
        alert("Ошибка авторизации");
      }

      alert(result.message);
      // Вывод ошибки
    } catch (error) {
      alert("Ошибка соединения с сервером");
      console.error(error);
    }
  });
// Страница регистрации пользователя
document
  .getElementById("registerForm")
  ?.addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const nickname = document.getElementById("nickname").value;
    const password = document.getElementById("password").value;
    // Требование данных
    if (email === "" || nickname === "" || password === "") {
      alert("Заполните все поля");
      return;
    }
    // Формирование пакета данных пользователя
    const data = {
      email: email,
      username: nickname,
      password: password,
    };
    // Попытка отправки данных на сервер
    try {
      // Формирование запроса
      const response = await fetch("http://localhost:8000/auth/registration", {
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
        alert("Регистрация завершена");
        // Переход на страницу входа
        window.location.assign("login.html");
      } else {
        alert("Ошибка авторизации");
      }

      alert(result.message);
      // Вывод ошибки
    } catch (error) {
      alert("Ошибка соединения с сервером");
      console.error(error);
    }
  });
