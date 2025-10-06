import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import List


class Connect:
    def __init__(self, id_):
        self.id = id_

    def ready_to_read(self):
        # sync
        time.sleep(0.1)  # simulate delay
        return True

    def ready_to_write(self):
        # sync
        time.sleep(0.1)
        return True

    def read(self):
        # sync I/O
        print(f"[{self.id}] read()")
        time.sleep(0.5)
        return f"file_from_{self.id}"

    def write(self, file):
        print(f"[{self.id}] write({file})")


class Transformer:
    @classmethod
    def transform_file(cls, file):
        # heavy CPU work imitation
        time.sleep(2)
        return file.upper()


def sync_worker1(connections: List[Connect]):
    for con in connections:
        if con.ready_to_read():
            file = con.read()
            new_file = Transformer.transform_file(file)
            if con.ready_to_write():
                con.write(new_file)


async def right_con_handler(con: Connect, pool: ProcessPoolExecutor):
    loop = asyncio.get_running_loop()
    buffer = None
    while True:
        if buffer is None:
            if await asyncio.to_thread(con.ready_to_read):
                buffer = await asyncio.to_thread(con.read)
                buffer = await loop.run_in_executor(
                    pool, Transformer.transform_file, buffer
                )
        else:
            if await asyncio.to_thread(con.ready_to_write):
                await asyncio.to_thread(con.write, buffer)
                buffer = None
                break
        await asyncio.sleep(0.1)  # чтобы не крутить бесконечный цикл без паузы


async def right_async_worker(connections: List[Connect]):
    with ProcessPoolExecutor() as pool:
        tasks = [
            asyncio.create_task(right_con_handler(con, pool)) for con in connections
        ]
        await asyncio.gather(*tasks)


async def con_handler(con: Connect, pool: ProcessPoolExecutor):
    if await asyncio.to_thread(con.ready_to_read):
        file = await asyncio.to_thread(con.read)
        new_file = await asyncio.get_running_loop().run_in_executor(
            pool, Transformer.transform_file, file
        )  # asyncio.get_running_loop() — возвращает текущий event_loop - он один, новый не создаётся.
        if await asyncio.to_thread(con.ready_to_write):
            await asyncio.to_thread(con.write, new_file)


async def async_worker2(connections: List[Connect]):
    with ProcessPoolExecutor() as pool:
        tasks = [asyncio.create_task(con_handler(con, pool)) for con in connections]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.time()
    asyncio.run(right_async_worker([Connect(i) for i in range(20)]))
    print(f"Right_async done in {time.time() - start} sec")

    start = time.time()
    asyncio.run(async_worker2([Connect(i) for i in range(20)]))
    print(f"Simple_async done in {time.time() - start} sec")

    start = time.time()
    sync_worker1([Connect(i) for i in range(20)])
    print(f"Sync done in {time.time() - start} sec")


def heavy_task(n):
    print(f"Do something with {n}")
    time.sleep(3)
    return f"Changed {n}"


async def heavy_handler(*args, task):
    start = time.time()
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        tasks = [loop.run_in_executor(pool, task, arg) for arg in args]
        res = await asyncio.gather(*tasks)

    elapsed = time.time() - start
    print(f"{res} -> Async \nDone in {elapsed} sec\n")


# asyncio.run(heavy_handler(1, 2, 3, task=heavy_task))


def heavy(task):
    start = time.time()
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(task, [1, 2, 3]))
    elapsed = time.time() - start
    print(f"{results} -> Sync \nDone in {elapsed} sec\n")


# heavy(heavy_task)

# pool.map() — это просто удобная “обёртка”, но под капотом она вызывает pool.submit() для каждой задачи и потом ждёт их через futures


def heavy2(task, *args):
    start = time.time()
    with ProcessPoolExecutor() as pool:
        # Отправляем задачи вручную
        futures = [pool.submit(task, arg) for arg in args]

        # Собираем результаты (как только готовы)
        res = []
        for future in as_completed(futures):
            res.append(future.result())

    elapsed = time.time() - start
    print(f"{res} -> Sync2 \nDone in {elapsed:.2f} sec")


# heavy2(heavy_task, 1, 2, 3)
