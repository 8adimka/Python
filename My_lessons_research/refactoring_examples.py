"""Refactoring examples: плохой код и исправленный вариант.

В одном файле показан большой пример плохого кода, содержащий несколько
запахов: длинный метод, длинный список параметров, избыточные комментарии,
дублирование кода, "ленивый" класс (т.е. класс, который ничего не делает
или смешивает ответственность), посредник и т.д.

Ниже — сначала плохой код (для анализа), затем идеальная версия.
"""

from typing import Any, Dict, List, Optional

# ----------------------------- ПЛОХОЙ КОД -----------------------------


class UserServiceLazy:
    # Класс слишком ленивый: он хранит состояние и делает всё в одном месте
    def __init__(
        self, db_url: str, timeout: int, retries: int, log: Optional[Any] = None
    ):
        # сохраняем параметры, хотя используем не все
        self.db_url = db_url
        self.timeout = timeout
        self.retries = retries
        self.log = log

    def get_users(
        self,
        raw: str,
        filter_min_age: int,
        sort_desc: bool,
        limit: int,
        show: bool,
        extra_flag: bool,
        callback=None,
    ):
        # Очень длинный метод. Комментарии ниже описывают каждую мелочь.
        # 1) парсинг входных данных
        users = []
        lines = raw.split("\n")
        for ln in lines:
            if not ln:
                continue
            # поддерживаем несколько разделителей
            if "," in ln:
                name, age = ln.split(",")
            elif ":" in ln:
                name, age = ln.split(":")
            else:
                name = ln
                age = "0"
            try:
                age_i = int(age)
            except Exception:
                age_i = 0
            users.append({"name": name.strip(), "age": age_i})

        # 2) дублирующаяся логика фильтрации по возрасту
        filtered = []
        for u in users:
            if u["age"] >= filter_min_age:
                filtered.append(u)
        # повторы: делаем почти то же самое
        filtered2 = []
        for u in filtered:
            if u["age"] >= filter_min_age:
                filtered2.append(u)

        # 3) сортировка
        if sort_desc:
            filtered2.sort(key=lambda x: x["age"], reverse=True)
        else:
            filtered2.sort(key=lambda x: x["age"])  # дублирование лямбда

        # 4) ограничение и показ результатов — смешиваем бизнес-логику с выводом
        result = filtered2[:limit]
        if show:
            for u in result:
                print("User:", u["name"], "age=", u["age"])  # вывод в теле метода

        # 5) посредник: вызываем callback если есть
        if callback:
            callback(result)

        # 6) бессмысленное ветвление по флагу
        if extra_flag:
            # делаем какую-то лишнюю работу
            s = 0
            for u in result:
                s += u["age"]  # суммируем, но ничего не делаем с результатом

        return result


# --------------------------- ИСПРАВЛЕННЫЙ КОД --------------------------

# Удобные маленькие функции: парсинг, фильтрация, сортировка, отображение


def parse_users(raw: str) -> List[Dict[str, Any]]:
    """Парсинг входной строки в список пользователей.

    Ожидается, что каждая запись на новой строке: "name,age" или "name:age".
    Неверный возраст трактуется как 0.
    """
    users: List[Dict[str, Any]] = []
    for ln in raw.splitlines():
        ln = ln.strip()
        if not ln:
            continue
        if "," in ln:
            parts = ln.split(",", 1)
        elif ":" in ln:
            parts = ln.split(":", 1)
        else:
            parts = [ln, "0"]
        name = parts[0].strip()
        try:
            age = int(parts[1].strip())
        except Exception:
            age = 0
        users.append({"name": name, "age": age})
    return users


def filter_by_min_age(
    users: List[Dict[str, Any]], min_age: int
) -> List[Dict[str, Any]]:
    """Возвращает пользователей с возрастом >= min_age."""
    return [u for u in users if u.get("age", 0) >= min_age]


def sort_users_by_age(
    users: List[Dict[str, Any]], descending: bool = True
) -> List[Dict[str, Any]]:
    """Сортирует пользователей по возрасту."""
    return sorted(users, key=lambda u: u.get("age", 0), reverse=descending)


def limit_users(
    users: List[Dict[str, Any]], limit: Optional[int]
) -> List[Dict[str, Any]]:
    if limit is None:
        return users
    return users[:limit]


def format_user(u: Dict[str, Any]) -> str:
    return f"{u.get('name')} — {u.get('age')}"


class UserService:
    """Чистая реализация сервиса пользователей.

    - Не хранит ненужного состояния.
    - Методы маленькие и однозначные.
    - Для вывода используется отдельная функция.
    """

    def __init__(self) -> None:
        pass

    def get_users(
        self,
        raw: str,
        *,
        min_age: int = 0,
        descending: bool = True,
        limit: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        users = parse_users(raw)
        users = filter_by_min_age(users, min_age)
        users = sort_users_by_age(users, descending)
        users = limit_users(users, limit)
        return users

    def show_users(self, users: List[Dict[str, Any]]) -> None:
        for u in users:
            print(format_user(u))


# ------------------------------- DEMO ---------------------------------

if __name__ == "__main__":
    sample = """Alice,12
Bob,9
Charlie:15
Daisy,notanumber
EmptyLine,
Eve,30
"""

    print("--- ПЛОХОЙ КОД: вызов UserServiceLazy.get_users ---")
    lazy = UserServiceLazy(db_url="sqlite://tmp", timeout=5, retries=2)
    bad = lazy.get_users(
        sample, filter_min_age=10, sort_desc=True, limit=10, show=True, extra_flag=True
    )

    print("\n--- ИСПРАВЛЕННЫЙ КОД: UserService ---")
    svc = UserService()
    users = svc.get_users(sample, min_age=10, descending=True, limit=10)
    svc.show_users(users)
