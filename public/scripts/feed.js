const postsContainer = document.getElementById("posts");
const addBtn = document.getElementById("addPostBtn");
const filterBtn = document.getElementById("filterBtn");

// Ссылка на страницу фильтра
filterBtn.addEventListener("click", () => {
    window.location.assign("TEST.html");
});

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