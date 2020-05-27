build-django:
	docker-compose build django

build: build-django

# Создаёт суперпользователя
create-superuser:
	docker-compose run django python manage.py create_admin

# Запуск web-приложения
runserver:
	docker-compose up -d django

# Запускает тесты
autotests:
	docker-compose run --rm django /app/start-autotests.sh


.PHONY: autotests runserver buld build-django create-superuser
