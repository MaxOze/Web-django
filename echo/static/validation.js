const form = document.getElementById('form')                // Просто достаем все нужные штуки из html
const firstname = document.getElementById('id_name')            // Мы их берем по id который написан в теге
const email = document.getElementById('id_email')
const login = document.getElementById('id_login')
const password = document.getElementById('id_password')
const radioFirstname = document.getElementById('name')
const radioEmail = document.getElementById('email')
const radioLogin = document.getElementById('login')
const radioPassword = document.getElementById('password')

// Обработчик нажатия на кнопку
form.addEventListener('submit', e => {                      // Срабатывает при нажатии на кнопку
    if(radioFirstname.checked || radioEmail.checked ||      // Проверяет какие штуки чекнуты
        radioLogin.checked || radioPassword.checked) {
        e.preventDefault();     // Если хоть одно условие не выполнено, нажатие на кнопку отменяется
    }
    // Если все кнопки чекнуты то регистрирует пользователя
});

// Проверка имени (не пустое)
$(document).ready(function() {
    $('#id_name').on("input", function(e) {                                     // Срабатвает при каждом вводе в строку
        if(firstname.value.trim() == null || firstname.value.trim() === "") {   // Проверяет не пустое ли
            radioFirstname.checked = false;
        } else {
            radioFirstname.checked = true;      // Если все норм то отмечает кнопку
        }
    })
})

// Проверка email (соответствует регулярному выражению и не пустое)
$(document).ready(function() {
    $('#id_email').on("input", function(e) {    // Срабатвает при каждом вводе в строку
        if(!isEmail(email.value.trim())) {      // В отдельной функции(внизу) сверяет по регулярнмоу выражению
            radioEmail.checked = false;
        } else {
            radioEmail.checked = true;      // Если все норм то отмечает кнопку
        }
    })
})

// Проверка логина (не занят и не пустой)
$(document).ready(function() {
    $('#id_login').on("input", function(e) {                            // Срабатвает при каждом вводе в строку                 
        if(login.value.trim() == null || login.value.trim() === "") {   // Проверяет если пустой
            radioLogin.checked = false;
        } else {
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();     // Токен нужен просто чтобы работало
            $.ajax({
                method: 'POST',                                             // Отправляет POST запрос
                url: "/check/",                                             // На URL /check
                data: JSON.stringify({ 'input': $('#id_login').val() } ),   // Отправляет JSON с логином который ввели
                beforeSend: function (xhr){                                 // Вместе с токеном
                    xhr.setRequestHeader('X-CSRFToken', csrftoken);
                  },
                contentType: "application/json; charset=utf-8",             // Говорит серверу что отправил JSON
                cache: false,                                               // хз зачем
                success: function(response) {                               // Если все норм и прислали ответ
                    if (response.is_taken == true) {                        // Проверяет занят ли пароль
                        radioLogin.checked = false;
                    }
                    else {
                        radioLogin.checked = true;          // Если все норм то отмечает кнопку
                    }
                }
            })
            return false;
        }
    })
})

// Проверка пароля (больше 6 знаков)
$(document).ready(function() {
    $('#id_password').on("input", function(e) {
        if(password.value.trim() == null || password.value.trim().length < 7) {     // Проверяет не пустой и больше 6 знаков
            radioPassword.checked = false;
        } else {
            radioPassword.checked = true;           // Если все норм то отмечает кнопку
        }
    })
})

// функция проверяющая email по регулярному выражению
function isEmail(email) {
    return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
}