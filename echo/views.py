import json

from django.core.paginator import Paginator
from django.http import (HttpResponse, HttpResponseNotFound,
                         HttpResponseRedirect, JsonResponse)
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from .forms import *
from .models import *

sort_by = 'name'        # Параметр сортировки

def start(request):                 # Нужно чтобы просто отправляло на страницу авторизации при пустой ссылке
    return redirect('/signin')


# Домашняя страница
def shop(request):
    books_list = Book.objects.all().order_by(sort_by).values()            # Достаем книги из базы данных, отсортировав
 
    paginator = Paginator(books_list, 5)        # Пагинатор делит книги по 5
    page_number = request.GET.get('page', 1)       # Из URL достаем номер страницы
    page_obj = paginator.get_page(page_number)  # Пагинатор отправляет только нужные для этой страницы книги

    context = { # Все данные которые надо передать в html
        'page_obj': page_obj,                           # Данные о книгах
        'page_number': page_number,                     # Передает номер страницы чтобы потом использовать его в методе с корзиной
        'role': request.session.get('role', 'none'),    # Достает из куки сессии роль; если неавторизован чел, то ставит 'none'
        'name': request.session.get('name', ''),        # Достает из куки сессии имя; если неавторизован чел, то ставит ''
    }

    return render(request, 'index.html', context)   # Отправляет книги, имя пользователя, роль пользователя и кол-во страниц в index.html


# Создание книг
def create(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role == 'none':
        return redirect('/signin')          # Если не зареган то отправляет авторизовываться

    if request.method == 'POST':            # Если форма уже заполнена
        form = BookForm(request.POST)       # Достает из формы данные  
        if form.is_valid():                 # Проверяет валидность данных
            book = form.save()              # Если норм то сохраняет в базу данных

            return redirect("/")            # И возвращает на домашнюю страницу
    else:
        form = BookForm()                   # Если форма не заполнялась или заполнилась некорректно, снова откроет пустую форму

    return render(request, "create.html", {'form': form})


# Изменение данных книги
def edit(request, id):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role != 'admin':
        return redirect('/shop?page=1')         # Если не админ то не может менять книги

    if Book.objects.filter(id=id).exists():            # Проверяет есть ли такая книга в базе данных
        book = Book.objects.get(id=id) 

        if request.method == 'POST':                        # Если форма заполнена
            form = BookForm(request.POST, instance=book)    # Достает из формы данные
            if form.is_valid():                             # Проверяет валидность данных
                book = form.save()                          # Если норм то пересохраняет в базу данных

                return redirect("/")                        # И возвращает на домашнюю страницу
        else:
            form = BookForm(instance=book)                  # Если нет то снова открывает форму с исходными данными книгами

        return render(request, "edit.html", {'form': form})

    return redirect("/")                # Если такой книги нет то перекидывает на главную


# Удаление книги
def delete(request, id):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role != 'admin':
        return redirect('/shop?page=1')         # Если не админ то не может удалять книги

    if Book.objects.filter(id=id).exists():            # Проверяет есть ли такая книга в базе данных
        book = Book.objects.get(id=id).delete();           # Проверяет есть ли такая книга в базе данных и удаляет если есть

    return redirect("/")                                 # Возвращает на главную страницу в любом случае


# Регистрация
def signUp(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role != 'none':
        return redirect('/shop?page=1')         # Если уже авторизован то отправляет на главную страницу

    if request.method == 'POST':                            # Если форма заполнена
        form = UserSignUpForm(request.POST)                 # Берет данны из формы
        if form.is_valid():
            user = User()
            user.name = form.cleaned_data['name']           # Достает данные из формы
            user.email = form.cleaned_data['email']         # Достает данные из формы
            user.login = form.cleaned_data['login']         # Достает данные из формы
            user.password = form.cleaned_data['password']   # Достает данные из формы
            user.role = Role.objects.get(id=1)              # Дает ему роль обычного юзера (админ только один с логином и паролем admin)
            user = user.save()                              # Сохраняет нового юзера в базу

            return redirect('/signin')
    else:
        form = UserSignUpForm()                             # Если первый раз страниц открыта то выводит пустую форму

    return render(request, 'sign_up.html', {'form': form})


# Авторизация
def signIn(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role != 'none':
        return redirect('/shop?page=1')         # Если уже авторизован то отправляет на главную страницу

    if request.method == 'POST':                        # Если форма заполнена
        form = UserSignInForm(request.POST)             # Достает данные из формы
        if form.is_valid():                             # Если форма норм заполнена
            if User.objects.filter(login=form.cleaned_data['login']).exists():      # Проверяет есть ли чел с таким логином
                user = User.objects.get(login=form.cleaned_data['login'])           # Если есть то достает его из базы данных
                if (user.password == form.cleaned_data['password']):                # Сверяет его пароль с введеным паролем
                    request.session['name'] = user.name                 # Создает в сессии имя пользователя
                    request.session['role'] = user.role.name            # Создает в сессии роль пользователя
                    request.session['cart'] = list()                    # Создает в сессии корзину
                    return redirect('/')                                # Отправляет на главную страницу
                else:
                    result = 'Неправильный пароль'          # Если пароль неправильный
            else:
                result = 'Несуществующий логин'             # Если такого логина нет
            form = UserSignInForm()                         # Если что то не так то просто выводит пустую форму

            return render(request, 'sign_in.html', {'form': form, 'result': result})    # Передает форму и сообщение если что то не так
    else:
        result = ' '
        form = UserSignInForm()         # Выводит пустую форму если зашли на страницу в первый раз

        return render(request, 'sign_in.html', {'form': form, 'result': result})    # result - это строчка которая пустая если все норм или пишет в чем ошибся пользователь


# Выход из учетной записи
def logout(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role != 'none':
        del request.session['role']         # Если был авторизован то удаляет все данные из сессии и отправляет на авторизацию
        del request.session['name']
        del request.session['cart']
    return redirect('/signin')
    

# Профиль
def profile(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role == 'none':
        return redirect('/signin')      # Если не зареган то отправляет авторизовываться

    user = User.objects.get(name=request.session['name'])           # Достает из сессии имя пользователя
    if request.method == 'POST':                                    # Если нажали изменить данные
        form = UserEditForm(request.POST, instance=user)            # Достает из формы данные
        if form.is_valid():                                         # Если данные валидны
            user.name = form.cleaned_data['name']                   # Достает из формы данные
            user.email = form.cleaned_data['email']                 # Достает из формы данные
            user = user.save()                                      # Сохраняет данные о пользователе в базу
            request.session['name'] = form.cleaned_data['name']     # Меняет имя пользователя в сессии

            return redirect('/profile')                             # Снова открывает эту страницу с обновленными данными
    else:
        form = UserEditForm(instance=user)          # Если открыли только открыли то показывает форму с теми данными которые есть
    
    return render(request, "profile.html", {'form': form})


# Добавление в корзину
def toCart(request, id):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role == 'none':
        return redirect('/signin')      # Если не зареган то отправляет авторизовываться

    if Book.objects.filter(id=id).exists():         # Проверяет есть ли такая книга
        cart = request.session['cart']              # Берет корзину из сессии
        cart.append(id)                             # Добавляет в корзину id книги
        request.session['cart'] = cart              # Засовывает корзину обратно в сессию
        page_number = request.GET.get('page')       # Смотрит с какой страницы был сделан запрос на эту книгу чтобы потом вернуть на нее обратно

    return redirect("/shop?page="+page_number)      # Возвращает на нужную страницу


# Корзина
def cart(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role == 'none':
        return redirect('/signin')              # Если не зареган то отправляет авторизовываться

    cart = request.session['cart']              # Достает из сессии корзину
    books = list()                              # Список для книг
    fullprice = 0                               # Переменная для подсчета полной цены корзины
    for id in cart:                             # Для каждого id книги из корзины:
        book = Book.objects.get(id=id)              # Берет из базы книгу по id
        books.append(book)                          # Добавляет ее в список
        fullprice = fullprice + book.price          # Добавляет ее цену

    if request.method == 'POST':                                        # Если нажали "сделать заказ"
        order = Order()                                                 # Создает заказ
        order.user = User.objects.get(name=request.session['name'])     # Ищет юзера который этот заказ сделал по имени из сессии
        order.price = fullprice                                         # Добавляет полную цену заказа
        order.save()                                                    # Сохраняет заказ в таблицу orders

        for id in cart:                                     # Для каждого id книги из корзины:
            orderBook = OrderBook()                         # Создает отношение заказ-книга (для таблицы которая связывает заказ и книги)
            orderBook.order = Order.objects.last()          # Берет id заказа который мы последним (только что)
            orderBook.book = Book.objects.get(id=id)        # Связывает его с id книги
            orderBook.save()                                # Сохраняет в таблицу orders_books

        request.session['cart'] = list()                # Очищает корзину

        return render(request, 'success.html')          # Перенаправляет на страницу с сообщение об успешном заказе

    context = {
        'books': books,                         # Достает из куки корзину пользователя
        'name': request.session['name'],        # Достает из куки сессии имя
        'fullprice': fullprice,
    }

    return render(request, 'cart.html', context)


# Заказы
def orders(request):
    role = request.session.get('role', 'none')  # Берет из сессии роль пользователя, если он не зареган то ставит none
    if role == 'none':
        return redirect('/signin')              # Если не зареган то отправляет авторизовываться

    user = User.objects.get(name=request.session['name'])   # Достает из сессии юзера который делает заказ
    userOrders = Order.objects.filter(user=user)            # Достает заказы этого юзера
    orders = dict()                                         # Словарь который потом пойдет в html
    i = 1                    # Переменная для номера заказа                            
    for item in userOrders:                                 # Для каждого заказа:
        order = OrderBook.objects.filter(order=item)            # Достает все соотношения заказ-книга
        books = list()                                          # Список книг для каждого заказа
        for book in order:                                      # Для каждого этого отношения:
            books.append(book.book)                                 # Добавляет книги из заказа

        orders['# ' + str(i) + ' ' + str(item.price) + ' | ' + str(item.date)[:19]] = books     # Добавляет словарь книг к заказу в список заказов
        i = i + 1                                                                                # Где ключ будет в заголовке с датой и ценой заказа
                                                                                                 # А значение это книги которые в заказе
    return render (request, 'orders.html', {'orders': orders})


# AJAX проверяющий не занят ли логин
def checkLogin(request):
    recieved_data = json.loads(request.body)        # Десериализует из JSONа данные
    input = recieved_data["input"]                  # Достает из данных input

    response = { 'is_taken': User.objects.filter(login=input).exists() }     # Засовывает в ответ true/false есть ли такой логин в базе

    return JsonResponse(response)


# AJAX для фильтрации таблицы
def sort(request):
    recieved_data = json.loads(request.body)        # Десериализует из JSONа данные
    input = recieved_data["input"]                  # Достает из данных по какому критерию сортировать
    page = recieved_data["page_number"]                    # Достает из данных номер страницы
    
    global sort_by
    sort_by = input                                                     # Меняем параметр сортировки (во всей программе)
    books_list = Book.objects.all().order_by(sort_by).values()          # Достаем книги из базы данных
    paginator = Paginator(books_list, 5)                                # Пагинатор делит книги по 5
    books = paginator.get_page(page)                                    # Пагинатор отправляет только нужные для этой страницы книги
    
    response = { 'books': list(books) }           # Засовывает в ответ книги в нужном порядке (превращает в лист, потому что не может передать класс Page)

    return JsonResponse(response)