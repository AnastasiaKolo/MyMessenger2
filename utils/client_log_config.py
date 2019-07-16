# -*- coding: utf8 -*-
# Для проекта «Мессенджер» реализовать логирование с использованием модуля logging:
# 1. В директории проекта создать каталог log, в котором для клиентской и серверной сторон
#    в отдельных модулях формата client_log_config.py и server_log_config.py создать логгеры;
# 2. В каждом модуле выполнить настройку соответствующего логгера по следующему алгоритму:
# -  Создание именованного логгера;
# -  Сообщения лога должны иметь следующий формат: '<дата-время> <уровень_важности> <имя_модуля> <сообщение>';
# -  Журналирование должно производиться в лог-файл;
# -  На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.
# 3. Реализовать применение созданных логгеров для решения двух задач:
# -  Журналирование обработки исключений try/except. Вместо функции print() использовать журналирование и
#    обеспечить вывод служебных сообщений в лог-файл;
# -  Журналирование функций, исполняемых на серверной и клиентской сторонах при работе мессенджера.
import logging
import sys
import os
from definitions import LOG_PATH

# В директории проекта создать каталог LOG_PATH, в него пишем лог клиента

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
logging_file = os.path.join(LOG_PATH, 'client.log')


# Создать регистратор верхнего уровня с именем 'client'
cli_log = logging.getLogger('client')
# Формат сообщений <дата-время> <уровень_важности> <имя_модуля> <сообщение>
_format = logging.Formatter('%(asctime)s %(levelname)-10s %(module)s: %(message)s')

# # Создать обработчик, который выводит сообщения с уровнем
# # CRITICAL в поток stderr
crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.CRITICAL)
crit_hand.setFormatter(_format)

# Создать обработчик, который выводит сообщения в файл
applog_hand = logging.FileHandler(logging_file, encoding='utf-8')
applog_hand.setFormatter(_format)
applog_hand.setLevel(logging.DEBUG)

# Добавить несколько обработчиков в регистратор 'client'
cli_log.addHandler(applog_hand)
cli_log.addHandler(crit_hand)
cli_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.DEBUG)
    console.setFormatter(_format)
    cli_log.addHandler(console)
    cli_log.info('Тестовый запуск логирования')
    cli_log.critical('critical!')
    cli_log.error('error!')
    cli_log.warning('warning!')
    cli_log.info('info!')
    cli_log.debug('debug!')
