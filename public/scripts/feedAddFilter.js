document.addEventListener("DOMContentLoaded", function () {
  const chips = document.querySelectorAll('.chip');
  const filtersTag = document.getElementsByClassName('filters')
  const publishBtn = document.querySelector('.publish');
  const feedPage = document.getElementById('feed-page');
  const filterBtn = document.getElementById('filter-btn')
  const sideBar = document.querySelector('.sidebar');
  const respPage = document.getElementById('resp-page');
  const ratingPage = document.getElementById('rating-page');
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
        sessionStorage.removeItem('token');
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

  // Логика дропдаун меню возраста
  if (filtersTag)
  {
    const ageFromSelect = document.getElementById('ageFrom');
    const ageToSelect = document.getElementById('ageTo');
    const minLimit = 10;
    const maxLimit = 80;

        // Функция заполнения
    function populate(select, start, end, placeholderText) {
        const currentValue = select.value;

        // Очищение и добавление только заглушки
        select.innerHTML = `<option value="" disabled ${!currentValue ? 'selected' : ''}>${placeholderText}</option>`;

        for (let i = start; i <= end; i++) {
            const opt = document.createElement('option');
            opt.value = i;
            opt.textContent = i;
            if (i == currentValue) opt.selected = true;
            select.appendChild(opt);
        }
    }

    // Первоначальное заполнение
    populate(ageFromSelect, minLimit, maxLimit, "Возраст от");
    populate(ageToSelect, minLimit, maxLimit, "Возраст до")
    // Логика связки
    ageFromSelect.addEventListener('change', () => {
        const fromValue = parseInt(ageFromSelect.value);
        // "До" не может быть меньше, чем выбранное "От"
        populate(ageToSelect, fromValue, maxLimit, "Возраст до");
    })
    ageToSelect.addEventListener('change', () => {
        const toValue = parseInt(ageToSelect.value);
        // "От" не может быть больше, чем выбранное "До"
        populate(ageFromSelect, minLimit, toValue, "Возраст от");
    });
  }

    // Функция для запросов с токеном авторизации
    async function apiRequest(url, options = {}, data) {
        const token = sessionStorage.getItem('token');
        console.log(token);
        if (token) options.headers = { ...options.headers, 'Authorization': `Bearer ${token}` };
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

  // Включение кнопок игр при нажатии
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chip.classList.toggle('active');
    });
  });

  // Отправка объявления
  publishBtn?.addEventListener('click', async () => {
    // сборка данных
    const description = document.querySelector('textarea').value;
    const buttons = document.querySelectorAll('.chip.active');
    const games = Array.from(buttons).map(btn => btn.textContent.trim());
    
    const dropDownMic = document.getElementById("micSelect");
    const selectedOptionMic = dropDownMic.options[dropDownMic.selectedIndex];

    const dropdownAgeFrom = document.getElementById("ageFrom");
    const selectedOptionAgeFrom = dropdownAgeFrom.options[dropdownAgeFrom.selectedIndex];
    const dropdownAgeTo = document.getElementById("ageTo");
    const selectedOptionAgeTo = dropdownAgeTo.options[dropdownAgeTo.selectedIndex];

    const mic = selectedOptionMic.text;
    const ageFrom = selectedOptionAgeFrom.value;
    const ageTo = selectedOptionAgeTo.value;
    
    if (!description.trim()) {
      alert('Введите описание!');
      return;
    }
    // Объект с данными (!ИЗМЕНИТЬ ИМЕНА ЕСЛИ НУЖНО!)
    const data = {
      games: games,
      age_from: ageFrom,
      age_to: ageTo,
      micro: mic,
      desc: description
    };
    // Отправка на сервер объявления
    try {
        const response = await apiRequest('http://localhost:8000/add-new', {} ,data); // ! ВСТАВИТЬ ЭНДПОИНТ !
        if (response.ok) {
            alert('Объявление опубликовано!');
            
        } else {
            console.error('Ошибка при добавлении объявления');
        }
      } catch (error) {
          console.error('Ошибка при добавлении объявлений:', error);
      }
    console.log(data)
  });

  // Сохранение фильтра
  filterBtn?.addEventListener('click', () => {
    // сборка данных
    const buttons = document.querySelectorAll('.chip.active');
    const games = Array.from(buttons).map(btn => btn.textContent.trim());
    
    const dropDownMic = document.getElementById("micSelect");
    const selectedOptionMic = dropDownMic.options[dropDownMic.selectedIndex];

    const dropdownAgeFrom = document.getElementById("ageFrom");
    const selectedOptionAgeFrom = dropdownAgeFrom.options[dropdownAgeFrom.selectedIndex];
    const dropdownAgeTo = document.getElementById("ageTo");
    const selectedOptionAgeTo = dropdownAgeTo.options[dropdownAgeTo.selectedIndex];

    const mic = selectedOptionMic.text;
    const ageFrom = selectedOptionAgeFrom.value;
    const ageTo = selectedOptionAgeTo.value;

    // Объект с данными (!ИЗМЕНИТЬ ИМЕНА ЕСЛИ НУЖНО!)
    const data = {
      games: games,
      ageFrom: ageFrom,
      ageTo: ageTo,
      micro: mic,
    };
    // Сохранение фильтра в хранилище сессии
    sessionStorage.setItem("filterTags", JSON.stringify(data));
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