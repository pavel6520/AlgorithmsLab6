from functools import reduce

global table_len

def generate_file(num: int):
    import random
    from string import ascii_letters, digits
    allowed_chars = ascii_letters + digits
    with open('keys.txt', 'w') as file:
        for _ in range(num):
            file.write(''.join(random.choice(allowed_chars) for i in range(6)) + '\n')


def excludive(s: str) -> int:
    r = [44, 49, 123, 64, 72, 98]
    return reduce(lambda a, x: a + x, [ord(s[i]) ^ r[i] for i in range(6)])


def div_method(k: int) -> int:
    return k % table_len


def mul_method(k: int) -> int:
    from math import modf, sqrt
    A: float = (sqrt(5.0) - 1.0) / 2.0
    M: float = table_len
    return int(list(modf(list(modf(k * A))[0] * M))[1])


def linear(hashed_key, i, size) -> int:
    c = 223
    return int((hashed_key + c * i) % size)


def square(hashed_key, i, size) -> int:
    c = 223.0
    d = 3.0
    return int((hashed_key + c * i + d * (i ** 2)) % size)


def create_table(hasher, accessor, size):
    distribution = []
    array = [None for _ in range(size)]
    for line in open('keys.txt', 'r'):
        i = 0
        key = hasher(excludive(line.strip('\n')))

        while True:
            index: int = accessor(key, i, size)
            if array[index] == None:
                array[index] = 1
                distribution.append(i + 1)
                break
            else:
                i += 1
                if accessor(key, 0, size) == accessor(key, i, size):
                    print(f'Collision for key {line}')
                    break
    return distribution


def create_dump(data: dict):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.append(['Количество ключей'] + [i for i in range(10, 1001, 10)])
    div_lin = ['Деления/линейная']
    div_sqr = ['Деления/квадратичная']
    mul_lin = ['Умножения/линейная']
    mul_sqr = ['Умножения/квадратичная']
    for _, value in data.items():
        div_lin.append(value[0])
        div_sqr.append(value[1])
        mul_lin.append(value[2])
        mul_sqr.append(value[3])
    ws.append(div_lin)
    ws.append(div_sqr)
    ws.append(mul_lin)
    ws.append(mul_sqr)
    wb.save("data_dump.xlsx")


if __name__ == '__main__':
    table_len = 1000
    result = {}

    from functools import reduce

    for elem_num in range(10, 1001, 10):
        generate_file(elem_num)
        result[elem_num] = [
            reduce(lambda a, x: a + x, create_table(div_method, linear, table_len)) / elem_num,
            reduce(lambda a, x: a + x, create_table(div_method, square, table_len)) / elem_num,
            reduce(lambda a, x: a + x, create_table(mul_method, linear, table_len)) / elem_num,
            reduce(lambda a, x: a + x, create_table(mul_method, square, table_len)) / elem_num]

    create_dump(result)