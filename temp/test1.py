# def range1(start, stop):
#     while start < stop:
#         yield start
#         start += 1
#
# def g():
#     print('started')
#     x = 42
#     yield x
#     print('yielded once')
#     x += 1
#     yield x
#     print('yielded twice, done')
#
#
#
# a = range(1, 100)
# print(a)
# print(type(a))
# print(sum(a))
#
# it = g()
# print('...')
# for x in it:
#     print(x)


# from itertools import groupby
#
# def sorted_runs(xs):
#     indices = range(len(xs) - 1)
#
#     def is_increasing(idx):
#         return xs[idx] < xs[idx + 1]
#
#     return groupby(indices, is_increasing)
#
# xs = [1, 2, 3, 5, 2, 0, 3, 1]
# for is_increasing, group in sorted_runs(xs):
#     print(
#         '<' if is_increasing else '>',
#         sum(1 for _ in group),
#     )

def running_sum():
    acc = 0
    while True:
        acc += yield acc

# s = running_sum()
# a = s.send(None)
# print (a)
# a = s.send(1)
# print (a)
# a = s.send(1)
# print (a)
# a = s.send(2)
# print (a)
#
# list1 = ['1', '2', '3']
# str1 = ','.join(list1)
# print(str1)
class MyException(Exception):
    pass


class Chats:
    def __init__(self):
        self.chats = []
        self.add_chat('ALL')

    def add_chat(self, chat_name):
        chat_clients = []
        if len(self.chats) == 10:
            raise MyException('More than 10 chats are not supported')
        if chat_name in self.chats:
            raise MyException('Chat already exists')
        self.chats.append(chat_name)

    def send_chat_list(self):
        '''returns packed server response with chat list'''
        str_chats = ','.join(self.chats)
        msg = {
            'response': 215,
            'alert': 'Sending chat list',
            'chat_list': str_chats
        }
        return msg

chats = Chats()
print(chats.chats)
for i in range(20):
    try:
        chats.add_chat(f'Chat{i}')
    except MyException:
        pass


print(chats.send_chat_list())

msg = {
        'response': 215,
        'time': 123,
        'alert': 'some alert'
        }
print(msg['response'])
print('response' in msg.keys())
# print(msg['nnn'])
#
# string1 = 'Connected'
# string2 = string1
# print(string2)
# string1 = ''
# print(string2)