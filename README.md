Test task

Технологический стек
--------------------

Python 3, Django, DRF, celery, docker, PostgreSQL

Запуск
------

~~~
git clone https://github.com/vyacheslav-v-v/testwork-asana.git
cd test-work
~~~

Запуск тестов:
~~~
make autotests
~~~
Создать суперпользователя с логином admin и паролем 123:
~~~
make create-superuser
~~~
Запуск сервера Django:
~~~
make runserver
~~~
По умолчанию отвечает по адресу http://0.0.0.0:8100

Админка
-
http://0.0.0.0:8100/admin/

Для работы необходимо в файле .env в корне проекта указать токен:

`ASANA_ACCESS_TOKEN="Write your token here"`
 