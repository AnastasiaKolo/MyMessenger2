from subprocess import Popen, CREATE_NEW_CONSOLE

p_list = []  # Список клиентских процессов

while True:
    user = input("Запустить X клиентов (1-9) / Закрыть клиентов (x) / Выйти (q) ")

    if user == 'q':
        break
    elif user.isdigit():
        for _ in range(int(user)):
            # Флаг CREATE_NEW_CONSOLE нужен для ОС Windows,
            # чтобы каждый процесс запускался в отдельном окне консоли
            p_list.append(Popen('python client.py',
                                creationflags=CREATE_NEW_CONSOLE))

        print(' Запущено %s клиентов' % user)
    elif user == 'x':
        for p in p_list:
            p.kill()
        p_list.clear()
