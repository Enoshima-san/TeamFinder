// Страница входа пользователя
document.getElementById("emailBtn")?.addEventListener("click", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    // Требование данных
    if (login === "") {
      alert("Введите email");
      return;
    }
    // Формирование пакета данных пользователя
    const data = {
      email: email
    };
    // Попытка отправки данных на сервер
    try {
      // Формирование запроса
      const response = await fetch("http://localhost:8000/auth/email", { // !!! СМЕНИТЬ ЭНДПОИНТ !!!
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
        document.getElementById("codeBtn").disabled = false;
        alert("Введите код подтверждения из email");
      } else {
        alert("Ошибка отправки");
      }
      // Вывод ошибки
    } catch (error) {
      alert("Ошибка соединения с сервером");
      console.error(error);
    }
  });

  document.getElementById("codeBtn")?.addEventListener("click", async function (e) {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const code = document.getElementById("code").value;
    // Требование данных
    if (code === "") {
      alert("Введите email");
      return;
    }
    // Формирование пакета данных пользователя
    const data = {
        email: email,
        code: code
    };
    // Попытка отправки данных на сервер
    try {
      // Формирование запроса
      const response = await fetch("http://localhost:8000/auth/code", { // !!! СМЕНИТЬ ЭНДПОИНТ !!!
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
        alert("Введён верный код");
        window.location.assign("recoverySecond.html");
      } else {
        alert("Ошибка отправки");
      }
      // Вывод ошибки
    } catch (error) {
      alert("Ошибка соединения с сервером");
      console.error(error);
    }
  });

  document.getElementById("recoverySecond")?.addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const passAgain = document.getElementById("passwordAgain").value;
    // Требование данных
    if (email === "" || passAgain === "" || password === "") {
      alert("Заполните все поля");
      return;
    }
    // Формирование пакета данных пользователя
    const data = {
      email: email,
      password: password,
      passAgain: passAgain
    };
    // Попытка отправки данных на сервер
    try {
      // Формирование запроса
      const response = await fetch("http://localhost:8000/auth/change", { // !!! СМЕНИТЬ ЭНДПОИНТ !!!
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
        alert("Пароль успешно сменён!");
        // Переход на страницу входа
        window.location.assign("login.html");
      } else {
        alert("Ошибка авторизации");
      }
      // Вывод ошибки
    } catch (error) {
      alert("Ошибка соединения с сервером");
      console.error(error);
    }
  });
