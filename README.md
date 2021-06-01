Test task

Technology stack
----------------

Python 3, Django, DRF, celery, docker, PostgreSQL

Start
---

~~~
git clone https://github.com/vyacheslav-v-v/testwork-asana.git
cd testwork-asana
~~~

Start tests:
~~~
make autotests
~~~
Create superuser with login `admin` and password `123`:
~~~
make create-superuser
~~~
Start Django server:
~~~
make runserver
~~~
By default, replies at http://0.0.0.0:8100

Admin
-
http://0.0.0.0:8100/admin/

Asana token should be specified in the .env file at the root of the project:

`ASANA_ACCESS_TOKEN="Write your token here"`
