from django import forms

from .models import *


# Форма нужна чтобы удобно отправлять ее в views и не писать лишний код в html файлах
# Заодно и валидация

# Форма для создания и редактирования книг
class BookForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    author = forms.CharField(max_length=200)
    price = forms.FloatField()

    class Meta:
        model = Book
        fields = ['name', 'author', 'price']


# Форма для авторизации
class UserSignInForm(forms.ModelForm):
    login = forms.CharField(max_length=100)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['login', 'password']


# Форма для регистрации
class UserSignUpForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=100)
    login = forms.CharField(max_length=100)
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['name', 'email', 'login', 'password']


# Форма для редактирования данных пользователя
class UserEditForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    email = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['name', 'email']
    