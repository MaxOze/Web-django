$("#name").on("click", function(e) {                                // Срабатывает при нажатии на заголовок 
    const number = document.getElementById('page');
    page_numb = number.innerText                                        // Достает номер страницы из html  
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();         // Токен чтобы post работал
    $.ajax({
        method: 'POST',                                                     // Отправляет POST запрос
        url: "/sort/",                                                      // На URL /sort
        data: JSON.stringify({ input: 'name', page_number: page_numb } ),   // Отправляет JSON с тем на что нажали и номером страницы
        beforeSend: function (xhr){                                         // Вместе с токеном
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
          },
        contentType: "application/json; charset=utf-8",             // Говорит серверу что отправил JSON
        cache: false,                                               // хз зачем
        success: function(response) {                               // Если все норм и прислали ответ
            rewriteTable(response.books, page_numb)                 // Вызывает функцию для перерисовывания таблицы
        }
    })
    return false;
})

$("#author").on("click", function(e) {                                // Срабатывает при нажатии на заголовок 
    const number = document.getElementById('page');
    page_numb = number.innerText                                        // Достает номер страницы из html  
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();         // Токен чтобы post работал
    $.ajax({
        method: 'POST',                                                     // Отправляет POST запрос
        url: "/sort/",                                                      // На URL /sort
        data: JSON.stringify({ input: 'author', page_number: page_numb } ),   // Отправляет JSON с тем на что нажали и номером страницы
        beforeSend: function (xhr){                                         // Вместе с токеном
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
          },
        contentType: "application/json; charset=utf-8",             // Говорит серверу что отправил JSON
        cache: false,                                               // хз зачем
        success: function(response) {                               // Если все норм и прислали ответ
            rewriteTable(response.books, page_numb)                 // Вызывает функцию для перерисовывания таблицы
        }
    })
    return false;
})

$("#price").on("click", function(e) {                                // Срабатывает при нажатии на заголовок 
    const number = document.getElementById('page');
    page_numb = number.innerText                                        // Достает номер страницы из html  
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();         // Токен чтобы post работал
    $.ajax({
        method: 'POST',                                                     // Отправляет POST запрос
        url: "/sort/",                                                      // На URL /sort
        data: JSON.stringify({ input: 'price', page_number: page_numb } ),   // Отправляет JSON с тем на что нажали и номером страницы
        beforeSend: function (xhr){                                         // Вместе с токеном
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
          },
        contentType: "application/json; charset=utf-8",             // Говорит серверу что отправил JSON
        cache: false,                                               // хз зачем
        success: function(response) {                               // Если все норм и прислали ответ
            rewriteTable(response.books, page_numb)                 // Вызывает функцию для перерисовывания таблицы
        }
    })
    return false;
})

function rewriteTable(list, page) {
    for (let i = 5; i > 0; i--) {                           // Удаляет старые строки (отчет в обратную сторону потому что если начинать с 0,
        document.getElementById("table").deleteRow(i);      // Берет таблицу из html и удаляет строку                       то номера строк после удаления одной меняются)
    }
    const table = document.querySelector('tbody');          // Берет из html тело таблицы с которым будет работать дальше
    const thCount = document.querySelectorAll('th');        // Подсчитывает количество заголовков (разное у админа и обычного юзера)

    if(thCount.length === 4) {                      // Если не админ
        for (let i = 0; i < 5; i++) {               // Просто для каждой книги вручную прописывает html код    
            table.innerHTML += `                
            <tr>
                <td>${list[i].name}</td>
                <td>${list[i].author}</td>
                <td>${list[i].price}</td>
                <td><a class="btn" href="tocart/${list[i].id}?page=${page}">Добавить в корзину</a></td>
            </tr>                             `;
        }
    }
    else {                                  // Если админ
        for (let i = 0; i < 5; i++) {       // Просто для каждой книги вручную прописывает html код
            table.innerHTML += `                
            <tr>
                <td>${list[i].name}</td>
                <td>${list[i].author}</td>
                <td>${list[i].price}</td>
                <td>
                    <div class="btn-group">
                        <a href="/edit/${list[i].id}" class="btn">Изменить</a>
                        <a href="/delete/${list[i].id}" class="btn">Удалить</a>
                    </div>
                </td>
                <td><a class="btn" href="/tocart/${list[i].id}?page=${page}">Добавить в корзину</a></td>
            </tr>                             `;
        }
    }
}