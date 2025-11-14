import asyncio
import time


# Синхронная версия
def sync_breakfast():
    start = time.time()

    print("🍳 Начали жарить яичницу")
    time.sleep(2)  # Блокируем весь поток!
    print("✅ Яичница готова")

    print("☕ Начали варить кофе")
    time.sleep(3)  # Снова блокируем
    print("✅ Кофе готов")

    end = time.time()
    print(f"🍽️ Завтрак готов за {end - start:.2f} секунд")


# Асинхронная версия
async def async_breakfast():
    start = time.time()

    async def make_eggs():
        print("🍳 Начали жарить яичницу")
        await asyncio.sleep(2)  # Не блокируем, а приостанавливаем корутину
        print("✅ Яичница готова")

    async def make_coffee():
        print("☕ Начали варить кофе")
        await asyncio.sleep(3)
        print("✅ Кофе готов")

    # Запускаем обе задачи одновременно
    await asyncio.gather(make_eggs(), make_coffee())

    end = time.time()
    print(f"🍽️ Завтрак готов за {end - start:.2f} секунд")


print("=== СИНХРОННАЯ ВЕРСИЯ ===")
sync_breakfast()  # Займет ~5 секунд

print("\n=== АСИНХРОННАЯ ВЕРСИЯ ===")
asyncio.run(
    async_breakfast()
)  # Займет ~3 секунды -> время самого долгого ожидания (пока ждем 3 секунды, параллельно ждем ещё и 2 секунды)
# _____________________________________________________________________________________________________________


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


def synk_worker(connections: list[Connect]):
    for con in connections:
        if con.ready_to_read():
            file = con.read()
            new_file = Transformer.transform_file(file)
            if con.ready_to_write():
                con.write(new_file)


async def con_handler(con: Connect, pool):
    pass


async def async_worker(connections: list[Connect]):
    pass


if __name__ == "__main__":
    start = time.time()
    synk_worker([Connect(i) for i in range(20)])
    print(f"Sync done in {time.time() - start:.2f} seconds")
