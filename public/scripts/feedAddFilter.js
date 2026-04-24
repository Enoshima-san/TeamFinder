document.addEventListener("DOMContentLoaded", function () {
  const chips = document.querySelectorAll(".chip");
  const filtersTag = document.getElementsByClassName("filters");
  const publishBtn = document.querySelector(".publish");
  const feedPage = document.getElementById("feed-page");
  const filterBtn = document.getElementById("filter-btn");
  const sideBar = document.querySelector(".sidebar");
  const respPage = document.getElementById("resp-page");
  const ratingPage = document.getElementById("rating-page");
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

  respPage.addEventListener("click", () => {
    window.location.assign("myResponces.html");
  });

  ratingPage.addEventListener("click", () => {
    window.location.assign("rating.html");
  });

  // Выход из аккаунта
  logOutBtn.addEventListener("click", () => {
    // Удаление токена пользователя из текущей сессии
    sessionStorage.removeItem("token");
    window.location.assign("login.html");
  });

  // Ссылка на страницу профиля
  profilePage.addEventListener("click", () => {
    window.location.assign("profile.html");
  });

  // Ссылка на страницу настроек
  hiddEditBtn.addEventListener("click", () => {
    window.location.assign("settings.html");
  });

  // Асинхронная функция запроса данных пользователя к серверу
  async function loadUserData() {
    try {
      const response = await apiRequest("http://localhost:8000/users/me");
      if (response.ok) {
        const userData = await response.json();

        if (document.querySelector(".user")) {
          document.getElementById("userAvatar").textContent = userData.username
            .charAt(0)
            .toUpperCase();
          document.getElementById("userNickName").textContent =
            userData.username;
        }
        console.log("Данные пользователя загружены:", userData);
      } else {
        alert("Ошибка при загрузке данных пользователя");
        console.error("Ошибка при загрузке данных пользователя");
      }
    } catch (error) {
      alert("Ошибка при загрузке данных пользователя");
      console.error("Ошибка при загрузке данных пользователя:", error);
    }
  }

  if (sideBar) {
    // Загрузка реальных данных пользователя с сервера
    loadUserData();
  }

  // Логика дропдаун меню возраста
  if (filtersTag) {
    const ageFromSelect = document.getElementById("ageFrom");
    const ageToSelect = document.getElementById("ageTo");
    const minLimit = 10;
    const maxLimit = 80;

    // Функция заполнения
    function populate(select, start, end, placeholderText) {
      const currentValue = select.value;

      // Очищение и добавление только заглушки
      select.innerHTML = `<option value="" disabled ${!currentValue ? "selected" : ""}>${placeholderText}</option>`;

      for (let i = start; i <= end; i++) {
        const opt = document.createElement("option");
        opt.value = i;
        opt.textContent = i;
        if (i == currentValue) opt.selected = true;
        select.appendChild(opt);
      }
    }

    // Первоначальное заполнение
    populate(ageFromSelect, minLimit, maxLimit, "Возраст от");
    populate(ageToSelect, minLimit, maxLimit, "Возраст до");
    // Логика связки
    ageFromSelect.addEventListener("change", () => {
      const fromValue = parseInt(ageFromSelect.value);
      // "До" не может быть меньше, чем выбранное "От"
      populate(ageToSelect, fromValue, maxLimit, "Возраст до");
    });
    ageToSelect.addEventListener("change", () => {
      const toValue = parseInt(ageToSelect.value);
      // "От" не может быть больше, чем выбранное "До"
      populate(ageFromSelect, minLimit, toValue, "Возраст от");
    });
  }

  // Функция для запросов с токеном авторизации
  async function apiRequestPost(url, options = {}, data) {
    const token = sessionStorage.getItem("token");
    console.log(token);
    if (token)
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json;charset=utf-8",
      };
    options.method = "POST";
    options.body = JSON.stringify(data);
    console.log(options);
    try {
      const response = await fetch(url, options);
      return response;
    } catch (error) {
      alert("Ошибка авторизации");
      console.error("Ошибка авторизации:", error);
      return;
    }
  }

  async function apiRequest(url, options = {}) {
    if (!options._retry) {
      const token = sessionStorage.getItem("token");
      if (token) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token}`,
        };
      }
    }
    try {
      const response = await fetch(url, options);

      if (response.status === 401 && !options._retry) {
        options._retry = true;

        const refreshToken = sessionStorage.getItem("refresh_token");
        if (refreshToken) {
          const refreshResponse = await fetch(
            "http://localhost:8000/auth/refresh",
            {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ refresh: refreshToken }),
            },
          );

          if (refreshResponse.ok) {
            const { access_token, refresh_token } =
              await refreshResponse.json();

            sessionStorage.setItem("token", access_token);
            if (refresh_token) {
              sessionStorage.setItem("refresh_token", refresh_token);
            }

            options.headers = {
              ...options.headers,
              Authorization: `Bearer ${access_token}`,
            };
            return await fetch(url, options);
          } else {
            sessionStorage.removeItem("token");
            sessionStorage.removeItem("refresh_token");
            window.location.href = "/login";
            throw new Error("Session expired");
          }
        }
      }

      return response;
    } catch (error) {
      console.error("Ошибка запроса:", error);
      if (error.message !== "Session expired") {
        alert("Ошибка запроса");
      }
      throw error;
    }
  }

  // Функция для запросов с методом GET с токеном авторизации
  async function apiRequestPost(url, options = {}, data) {
    const token = sessionStorage.getItem("token");
    console.log(token);
    if (token)
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json;charset=utf-8",
      };
    options.method = "POST";
    options.body = JSON.stringify(data);
    console.log(options);
    try {
      const response = await fetch(url, options);
      return response;
    } catch (error) {
      alert("Ошибка авторизации");
      console.error("Ошибка авторизации:", error);
      return;
    }
  }

  // Включение кнопок игр при нажатии
  chips.forEach((chip) => {
    chip.addEventListener("click", () => {
      chips.forEach((c) => c.classList.remove("active"));
      chip.classList.add("active");
    });
  });

  // Отправка объявления
  publishBtn?.addEventListener("click", async () => {
    // сборка данных
    const description = document.querySelector("textarea").value;
    const activeChip = document.querySelector(".chip.active");
    const gameId = activeChip ? activeChip.getAttribute("data-id") : null;

    const dropDownMic = document.getElementById("micSelect");
    const selectedOptionMic = dropDownMic.options[dropDownMic.selectedIndex];

    const dropdownAgeFrom = document.getElementById("ageFrom");
    const selectedOptionAgeFrom =
      dropdownAgeFrom.options[dropdownAgeFrom.selectedIndex];
    const dropdownAgeTo = document.getElementById("ageTo");
    const selectedOptionAgeTo =
      dropdownAgeTo.options[dropdownAgeTo.selectedIndex];

    const mic = selectedOptionMic.value;
    const ageFrom = selectedOptionAgeFrom.value;
    const ageTo = selectedOptionAgeTo.value;

    if (!description.trim()) {
      alert("Введите описание!");
      return;
    }
    // Объект с данными
    const data = {
      type: "team",
      game_id: gameId,
      has_microphone: mic,
      rank_min: parseInt(ageFrom) || 0,
      rank_max: parseInt(ageTo) || 99,
      description: description,
    };
    // Отправка на сервер объявления
    try {
      const response = await apiRequestPost(
        "http://localhost:8000/a/new",
        {},
        data,
      );
      if (response.ok) {
        const result = await response.json();
        const newPostId = result.announcement_id;
        let respondedMyPosts =
          JSON.parse(sessionStorage.getItem("respondedMyPosts")) || [];
        if (newPostId && !respondedMyPosts.includes(newPostId)) {
          respondedMyPosts.push(newPostId);
          sessionStorage.setItem(
            "respondedMyPosts",
            JSON.stringify(respondedMyPosts),
          );
        }
        alert("Объявление опубликовано!");
      } else {
        alert("Ошибка при добавлении объявления");
        console.error("Ошибка при добавлении объявления");
      }
    } catch (error) {
      alert("Ошибка при добавлении объявления");
      console.error("Ошибка при добавлении объявлений:", error);
    }
    console.log(data);
  });

  // Сохранение фильтра
  filterBtn?.addEventListener("click", () => {
    sessionStorage.removeItem("filterTags");
    // сборка данных
    const buttons = document.querySelectorAll(".chip.active");
    const games = Array.from(buttons).map((btn) => btn.textContent.trim());

    const dropDownMic = document.getElementById("micSelect");
    const selectedOptionMic = dropDownMic.options[dropDownMic.selectedIndex];

    const dropdownAgeFrom = document.getElementById("ageFrom");
    const selectedOptionAgeFrom =
      dropdownAgeFrom.options[dropdownAgeFrom.selectedIndex];
    const dropdownAgeTo = document.getElementById("ageTo");
    const selectedOptionAgeTo =
      dropdownAgeTo.options[dropdownAgeTo.selectedIndex];

    const mic = selectedOptionMic.text;
    const ageFrom = selectedOptionAgeFrom.value;
    const ageTo = selectedOptionAgeTo.value;

    // Объект с данными
    const data = {
      games: games,
      ageFrom: ageFrom,
      ageTo: ageTo,
      micro: mic,
    };
    console.log(data);
    // Сохранение фильтра в хранилище сессии
    sessionStorage.setItem("filterTags", JSON.stringify(data));
    alert("Фильтр добавлен!");
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
