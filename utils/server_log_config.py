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

import logging.handlers
import sys
import os
from definitions import LOG_PATH

# В директории проекта создать каталог LOG_PATH, в него пишем лог клиента

if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)
logging_file = os.path.join(LOG_PATH, 'server.log')


# Создать регистратор верхнего уровня с именем 'server'
serv_log = logging.getLogger('server')
# Формат сообщений <дата-время> <уровень_важности> <имя_модуля> <сообщение>
_format = logging.Formatter('%(asctime)s %(levelname)-10s %(module)s: %(message)s')

# # Создать обработчик, который выводит сообщения с уровнем
# # CRITICAL в поток stderr
crit_hand = logging.StreamHandler(sys.stderr)
crit_hand.setLevel(logging.CRITICAL)
crit_hand.setFormatter(_format)

# Создать обработчик, который выводит сообщения в файл
# ротация лога каждые 5 минут для проверки
applog_hand = logging.handlers.TimedRotatingFileHandler(logging_file, when='D', interval=1, encoding='utf-8',
                                                        backupCount=10)
applog_hand.setFormatter(_format)
applog_hand.setLevel(logging.DEBUG)

# Добавить несколько обработчиков в регистратор 'server'
serv_log.addHandler(applog_hand)
serv_log.addHandler(crit_hand)
serv_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    # Создаем потоковый обработчик логирования (по умолчанию sys.stderr):
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(logging.DEBUG)
    console.setFormatter(_format)
    serv_log.addHandler(console)
    serv_log.info('Тестовый запуск логирования')
    serv_log.critical('critical!')
    serv_log.error('error!')
    serv_log.warning('warning!')
    serv_log.info('info!')
    serv_log.debug('debug!')
