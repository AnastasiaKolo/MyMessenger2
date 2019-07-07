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

s = running_sum()
a = s.send(None)
print (a)
a = s.send(1)
print (a)
a = s.send(1)
print (a)
a = s.send(2)
print (a)