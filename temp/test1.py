# def main():
#     str = input()
#     a = int(str.split(' ')[0])
#     b = int(str.split(' ')[1])
#     c = a + b
#     print(c)

# def main():
#     with open('output.txt', 'w') as outfile, open('input.txt', 'r', encoding='utf-8') as infile:
#         str_input = infile.readline()
#         a = int(str_input.split(' ')[0])
#         b = int(str_input.split(' ')[1])
#         c = a + b
#         outfile.write(str(c))
#
# if __name__ == '__main__':
#     main()


# array sorting
# with open("input.txt", "r") as f:
#     n = int(f.readline())
#     a = [int(i) for i in f.readline().split()]
#
# a.sort()
#
# with open("output.txt", "w") as f:
#     f.write(" ".join(str(i) for i in a))

    # Дан массив a  из  n  целых чисел.Напишите
    # программу, которая  найдет число, которое
    # чаще других встречается  в  массиве.
    # Ограничение  времени 2    секунды    Ограничение
    # памяти    256   Mb   Ввод   стандартный   ввод
    # или    input.txt    Вывод    стандартный    вывод
    # или    output.txt
# from collections import Counter
#
# with open("input.txt", "r") as f:
#     n = int(f.readline())
#     a = [int(i) for i in f.readline().split()]
#
# b = Counter(a).most_common(1)[0][0]
#
# with open("output.txt", "w") as f:
#     f.write(str(b))

with open("input.txt", "r") as f:
    n = int(f.readline())
    a = [int(i) for i in f.readline().split()]

def sequence(n):
    a = 0
    b = 1
    c = 2
    for _ in range(n):
        a, b, c = b, c, c + a
    return a

b = [sequence(item) for item in a]
str_ = ' '.join(str(e) for e in b)

with open("output.txt", "w") as f:
    f.write(str_)