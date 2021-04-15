**Запуск производился на Ubuntu 20.04.2**

Для запуска приложения необходимо:
    
    1) склонировать проект git clone https://github.com/Beloslav13/django_parser.git
    2) docker-compose build, после сборки docker-compose up
    3) в терминале открыть новую вкладку и зайти в контейнер docker exec -it django_parser_app_1 bash
    4) python manage.py migrate
    5) python manage.py createsuperuser
    6) запустить команду python manage.py parse_log --url http://www.almhuette-raith.at/apache-log/access.log