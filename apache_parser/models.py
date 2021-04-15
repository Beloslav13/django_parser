from django.db import models


class BaseLogData(models.Model):

    HTTP_METHODS = [
        ('GET', 'Метод GET'),
        ('POST', 'Метод POST'),
        ('PUT', 'Метод PUT'),
        ('PATCH', 'Метод PATCH'),
        ('DELETE', 'Метод DELETE'),
    ]

    ip_address = models.CharField(max_length=255, verbose_name='IP адресс')
    created_log = models.DateTimeField(verbose_name='Дата лога')
    http_method = models.CharField(choices=HTTP_METHODS, max_length=255, db_index=True, verbose_name='HTTP метод')
    url = models.TextField(verbose_name='URL')
    response_code = models.IntegerField(verbose_name='Код ответа', db_index=True)
    response_size = models.CharField(max_length=255, verbose_name='Размер ответа')

    class Meta:
        abstract = True


class ApacheLogData(BaseLogData):

    def __str__(self):
        return f'Лог id {self.pk}, дата лога {self.created_log}'

    class Meta:
        verbose_name = 'Apache лог'
        verbose_name_plural = 'Apache логи'
