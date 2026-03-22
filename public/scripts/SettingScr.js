// Переход на ввод нового пароля
document
  .getElementById("SettingForm")
  ?.addEventListener("submit", async function (e) {
    e.preventDefault();

    const nickname = document.getElementById("nickname").value;
    const description = document.getElementById("description").value;
    // Требование данных
    if (nickname === "") {
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
