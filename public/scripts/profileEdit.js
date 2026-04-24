document.addEventListener("DOMContentLoaded", function () {
  const feedPage = document.getElementById("feed-page");
  const profielInfo = document.querySelector(".profile-info");
  const sideBar = document.querySelector(".sidebar");
  const respPage = document.getElementById("resp-page");
  const ratingPage = document.getElementById("rating-page");
  const chatsPage = document.getElementById("chats-page");
  const logOutBtn = document.getElementById("logOutBtn");
  const editBtn = document.getElementById("editBtn");
  const profilePage = document.getElementById("profile-page");
  const editSaveBtn = document.getElementById("editSave");
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

  // Функция для запросов с токеном авторизации
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
  async function apiRequestPatch(url, options = {}, data) {
    const token = sessionStorage.getItem("token");
    console.log(token);
    if (token)
      options.headers = {
        ...options.headers,
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json;charset=utf-8",
      };
    options.method = "PATCH";
    options.body = JSON.stringify(data);
    console.log(options);
    try {
      const response = await fetch(url, options);
      return response;
    } catch (error) {
      alert("Ошибка авторизации:");
      console.error("Ошибка авторизации:", error);
      return;
    }
  }

  editBtn?.addEventListener("click", () => {
    window.location.assign("settings.html");
  });

  editSaveBtn?.addEventListener("click", async () => {
    const newUserName = document.getElementById("newUserName").value;
    const newBio = document.getElementById("newBio").value;
    const user_id = sessionStorage.getItem("user_id");
    const data = {
      user_id: user_id,
      username: newUserName,
      about_me: newBio,
    };
    console.log(data);
    try {
      const response = await apiRequestPatch(
        `http://localhost:8000/users/${user_id}`,
        {},
        data,
      );
      if (response.ok) {
        alert("Настройки сохранены!");
      } else {
        alert("Ошибка при сохранении настроек");
        console.error("Ошибка при сохранении настроек");
      }
    } catch (error) {
      alert("Ошибка при сохранении настроек");
      console.error("Ошибка при сохранении настроек:", error);
    }
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
          sessionStorage.setItem("user_id", userData.user_id);
        }
        console.log("Данные пользователя загружены:", userData);
      } else {
        console.error("Ошибка при загрузке данных пользователя");
      }
    } catch (error) {
      console.error("Ошибка при загрузке данных пользователя:", error);
    }
  }

  async function loadProfileData() {
    try {
      const response = await apiRequest("http://localhost:8000/users/me");
      if (response.ok) {
        const userData = await response.json();

        if (profielInfo) {
          document.getElementById("profileAvatar").textContent =
            userData.username.charAt(0).toUpperCase();
          document.getElementById("profileName").textContent =
            userData.username;
          document.getElementById("userDesc").textContent = userData.about_me;
          const isoDate = userData.registration_date;
          const date = new Date(isoDate);
          document.getElementById("userDate").textContent =
            date.toLocaleDateString("ru-RU");
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
    loadUserData();
  }

  if (profielInfo) {
    loadProfileData();
  }

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
