# Даны два массива: [1, 2, 3, 2, 0] и [5, 1, 2, 7, 3, 2]
# Надо вернуть [1, 2, 2, 3] (порядок неважен)


a = [1, 2, 3, 2, 0]
b = [5, 1, 2, 7, 3, 2]


def intersection(a: list, b: list) -> list:
    result = []

    for num in a:
        if num in b:
            result.append(num)
            b.remove(num)

    return result


# Дана строка (возможно, пустая), состоящая из букв A-Z: AAAABBBCCXYZDDDDEEEFFFAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBB
# Нужно написать функцию RLE, которая на выходе даст строку вида: A4B3C2XYZD4E3F3A6B28
# И сгенерирует ошибку, если на вход пришла невалидная строка.
# Пояснения: Если символ встречается 1 раз, он остается без изменений; Если символ повторяется более 1 раза, к нему добавляется количество повторений.


def counter(s: str):
    counter = 1
    i = 1
    res = [s[0]]

    while i < len(s):
        if s[i] != s[i - 1]:
            if counter > 1:
                res.append(str(counter))
                res.append(s[i])
                counter = 1
            else:
                res.append(s[i])
                counter = 1
        else:
            counter += 1
        i += 1
    return "".join(res)


# __________________________________________________________________________________________________________________

import asyncio
from concurrent.futures import ProcessPoolExecutor
from typing import List


class Connect:
    def ready_to_read(self):
        # sync
        return True

    def ready_to_write(self):
        # sync
        return True

    def read(self):
        # sync I/O
        return "some data"

    def write(self, file):
        print("write:", file)


class Transformer:
    @classmethod
    def transform_file(cls, file):
        # CPU-bound work
        # must be picklable (top-level)
        return file.upper()


def worker1(connections: List[Connect]):
    for con in connections:
        if con.ready_to_read():
            file = con.read()
            new_file = Transformer.transform_file(file)
            if con.ready_to_write():
                con.write(new_file)


async def worker2(connections: List[Connect]):
    read_list = set(connections.copy())
    write_list = []
    processing = {}
    while read_list or write_list or processing:
        ready_to_read = [c for c in read_list if c.ready_to_read()]
        ready_to_write = [c for c in write_list if c.ready_to_write()]

        if ready_to_read:
            for con in ready_to_read:
                image = con.read()
                new_image = Transformer.transform_file(image)
                processing[con] = new_image
                read_list.remove(con)
                write_list.append(con)

        if ready_to_write:
            for con in ready_to_write:
                if con in processing:
                    con.write(processing[con])
                    write_list.remove(con)
                    del processing[con]


async def con_handler(con: Connect):
    if await asyncio.to_thread(con.ready_to_read):
        file = await asyncio.to_thread(con.read)
        new_file = asyncio.get_running_loop().run_in_executor(
            ProcessPoolExecutor, Transformer.transform_file(file)
        )
        if await con.ready_to_write():
            await con.write(new_file)


async def async_worker3(connections: List[Connect]):
    tasks = [asyncio.create_task(con_handler(con)) for con in connections]
    await asyncio.gather(*tasks)
