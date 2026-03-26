document.getElementById("PRFormFirst").addEventListener("submit", async function (e) {
    e.preventDefault();

    const email = document.getElementById("email").value;
    const codeInput = document.getElementById("code");
    const btnCode = document.getElementById("btn-code");
    const btnEmail = document.getElementById("btn-email");

    btnEmail?.addEventListener("click", async function () {
        if (email === "") {
            alert("Заполните все поля");
            return;
        }
        else {
            codeInput.disabled = false;
            btnCode.disabled = false;
        }
    });

    btnCode?.addEventListener("click", async function () {
        const code = document.getElementById("code").value;

        // Формирование пакета данных пользователя
        const data = {
            email: email,
            code: code,
        };
        // Попытка отправки данных на сервер
        try {
        // Формирование запроса
        const response = await fetch("http://localhost:8000/auth/PasswordRecoveryFirst", {
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
            alert("Верный код");
            // Переход на страницу входа
            window.location.assign("PasswordRecoverySecond.html");
        } else {
            alert("Неверный код");
        }

        alert(result.message);
        // Вывод ошибки
        } catch (error) {
            alert("Ошибка соединения с сервером");
            console.error(error);
        }
    });
});

document
  .getElementById("PRFormSecond")
  ?.addEventListener("submit", async function (e) {
    e.preventDefault();

    const newpassword = document.getElementById("password").value;
    const newpasswordAgain = document.getElementById("passwordAgain").value;
    // Требование данных
    if (newpassword === "" || newpasswordAgain === "") {
      alert("Введите пароль");
      return;
    }
    // Проверка пароля
    if (newpassword !== newpasswordAgain) {
      alert("Пароли не совпадают");
      return;
    }
    // Формирование пакета данных пользователя
    const data = {
      newpassword: password,
      newpasswordAgain: passwordAgain,
    };
    // Попытка отправки данных на сервер
    try {
      // Формирование запроса
      const response = await fetch("http://localhost:8000/auth/PasswordRecoverySecond", {
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
        sessionStorage.setItem("token", result.token);
        alert("Смена пароля завершена");
        // Переход на новую страницу
        window.location.assign("login.html");
      } else {
        alert("Ошибка смены пароля");
      }

      alert(result.message);
      // Вывод ошибки
    } catch (error) {
      alert("Ошибка соединения с сервером");
      console.error(error);
    }
  });
