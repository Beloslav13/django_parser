import datetime
from time import strptime

from django.core.management.base import BaseCommand, CommandError

from apache_parser.models import ApacheLogData
from apache_parser.utils import request_apache_log

import logging

logger = logging.getLogger('logfile_error')


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            '--url',
            dest='url',
            type=str,
        )

    def get_datetime(self, created_log):
        """
        Получает нормализованную дату и время создания лога.
        """
        _month = created_log.split('/')[1]
        month = strptime(_month, '%b').tm_mon
        month = '0' + str(month) if month < 10 else str(month)
        created_log = created_log.replace(_month, month).replace('/', '-').replace(':', ' ').split()
        _date = created_log.pop(0).split('-')
        _date = f'{_date[2]}-{_date[1]}-{_date[0]}'
        _time = ':'.join(created_log)
        created_log = f'{_date} {_time}'
        created_log = datetime.datetime.fromisoformat(created_log).astimezone()
        return created_log

    def normalize_data(self, f, result):
        """
        Нормальзует данные для дальнешей записи в объект.
        """
        log_data = f.split()
        ip_address = log_data.pop(0)
        created_log = log_data.pop(2).replace('[', '')
        http_method = log_data.pop(3).replace('"', '')
        log_url = log_data.pop(3)
        response_code = log_data.pop(4)
        response_size = log_data.pop(4)

        created_log = self.get_datetime(created_log)

        result.append({
            'ip_address': ip_address,
            'created_log': created_log,
            'http_method': http_method,
            'log_url': log_url,
            'response_code': response_code,
            'response_size': response_size,
        })

        return result

    def create_logs(self, result):
        """
        Создает в БД объекты логов.
        """
        for res in result:
            try:
                ApacheLogData.objects.create(
                    ip_address=res['ip_address'],
                    created_log=res['created_log'],
                    http_method=res['http_method'],
                    url=res['log_url'],
                    response_code=res['response_code'],
                    response_size=res['response_size']
                )
            except Exception as exc:
                logger.error(f'Error: {exc}')

    def parse_and_create_logs(self):
        """
        Главная функция парсинга и создания логов.
        """
        with open('apache_log.log', 'r') as file:
            result = []
            i = 0
            for f in file:
                if i > 0:
                    # Подготовка к записи
                    result = self.normalize_data(f, result)
                i += 1

        # Запись(создание) логов
        self.create_logs(result)

    def handle(self, *args, **options):
        url = options.get('url', None)

        if url is None:
            raise CommandError('`url` required')

        response = request_apache_log(url)
        with open('apache_log.log', 'wb') as file:
            file.write(response.content)

        self.parse_and_create_logs()
