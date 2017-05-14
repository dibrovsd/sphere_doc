Ресурсы приложения
==================
Настройки путей [Blueprint](http://flask-russian-docs.readthedocs.io/ru/latest/blueprints.html "Русскоязычная документация по Flask Blueprint")


Модуль:
    sphere.auth.blueprint

* Путь `/login/` вызывает `LoginView`

  Системное имя _login_
* Путь `/logout/` вызывает `LogoutView`

  Системное имя _logout_
* Путь `/password_change/` вызывает `PasswordChangeView`

  Системное имя _password_change_
* Путь `/reset_password/` вызывает `PasswordResetView`

  Системное имя _reset_password_
* Путь `/reset_password/complete/<token>/` вызывает `LoginResetCompleteView`

  Системное имя _reset_password_complete_
* Путь `/login_as_user/<email>/` вызывает `LoginInUserView`

  Системное имя _login_as_user_
