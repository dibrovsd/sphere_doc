Ресурсы приложения
==================
Настройки путей [Blueprint](http://flask-russian-docs.readthedocs.io/ru/latest/blueprints.html "Русскоязычная документация по Flask Blueprint")


Модуль:
    sphere.auth.blueprint

* _login_ : `/login/` вызывает `LoginView`. 
* _logout_ : `/logout/` вызывает `LogoutView`. 
* _password_change_ : `/password_change/` вызывает `PasswordChangeView`. 
* _reset_password_ : `/reset_password/` вызывает `PasswordResetView`. 
* _reset_password_complete_ : `/reset_password/complete/<token>/` вызывает `LoginResetCompleteView`. 
* _login_as_user_ : `/login_as_user/<email>/` вызывает `LoginInUserView`. 
* _set_settings_ajax_ : `/set_settings_ajax/` вызывает `SetSettingsAjax`. 
