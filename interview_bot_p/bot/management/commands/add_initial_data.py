from django.core.management.base import BaseCommand
from bot.models.models import Question, Prompt
from bot.database import SessionLocal
from sqlalchemy.exc import IntegrityError

class Command(BaseCommand):
    help = "Добавляет начальные данные (вопросы и промпты) в базу данных"

    def handle(self, *args, **kwargs):
        try:
            db = SessionLocal()

            # Добавляем вопросы
            questions = [{"category": "Technical skill - Core language knowledge", "text": "Какие встроенные типы данных есть в Python?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Как обрабатывать ошибки в Python?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Какие типы импорта вы знаете и чем они отличаются?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "В чем разница между модулем и пакетом?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Что такое области видимости и как они работают в Python?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Как Python понимает, где искать модули и пакеты?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Как обрабатывать циклические импорты?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "В чем разница между итератором и генератором?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Какие проблемы решают контекстные менеджеры?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Какие проблемы решают декораторы?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Какие проблемы решают аннотации типов?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Что такое утиная типизация и как Python следует ей?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Как можно управлять доступом к данным экземпляра класса (с помощью дескрипторов)?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Как Python проверяет тип значения перед присваиванием?", "user_name": "default_user"},
        {"category": "Technical skill - Core language knowledge", "text": "Что такое метакласс и его варианты использования? Когда их не стоит использовать?", "user_name": "default_user"},
        {"category": "Technical skill - Advanced language knowledge", "text": "Что такое GIL и его назначение?", "user_name": "default_user"},
        {"category": "Technical skill - Advanced language knowledge", "text": "Почему один процесс Python не может одновременно использовать все ядра CPU? Есть ли обходные пути?", "user_name": "default_user"},
        {"category": "Technical skill - Advanced language knowledge", "text": "Вы выберете потоки или процессы для выполнения вычислений, связанных с CPU, на нескольких ядрах CPU? А что насчет IO-bound задач? Объясните почему.", "user_name": "default_user"},
        {"category": "Technical skill - Advanced language knowledge", "text": "Чем корутины (асинхронное программирование) отличаются от потоков и процессов? Каковы их варианты использования?", "user_name": "default_user"},
        {"category": "Technical skill - Advanced language knowledge", "text": "Что значит быть потокобезопасным? Как обычно достигается потокобезопасность?", "user_name": "default_user"},
        {"category": "Technical skill - Advanced language knowledge", "text": "Как вы общаетесь между разными процессами (например, отправка или получение данных из другого процесса) при использовании многопроцессорности?", "user_name": "default_user"},
        {"category": "Language ecosystem", "text": "Какова цель инструментов управления зависимостями?", "user_name": "default_user"},
        {"category": "Language ecosystem", "text": "Какова цель инструментов изоляции окружения (virtualenv, pyenv и т.д.)?", "user_name": "default_user"},
        {"category": "Language ecosystem", "text": "Что такое пакет Python?", "user_name": "default_user"},
        {"category": "Language ecosystem", "text": "Какие инструменты управления зависимостями вы знаете/используете? В чем их различия?", "user_name": "default_user"},
        {"category": "Language ecosystem", "text": "Когда вам могут понадобиться инструменты изоляции окружения в проекте?", "user_name": "default_user"},
        {"category": "Language ecosystem", "text": "Каковы преимущества разделения кода на пакеты?", "user_name": "default_user"},
        {"category": "Language ecosystem", "text": "Каковы преимущества форматировщиков кода (yapf, black)?", "user_name": "default_user"},
        {"category": "Language ecosystem", "text": "Каковы преимущества линтеров и инструментов статического анализа кода (prospector, pylint и т.д.)?", "user_name": "default_user"},
        {"category": "Language ecosystem", "text": "Какова цель статических анализаторов типов? Когда вы их запускаете?", "user_name": "default_user"},
        {"category": "Language ecosystem", "text": "Что такое PEP и его назначение?", "user_name": "default_user"},
        {"category": "Testing", "text": "Какие типы тестов вы знаете и какие проблемы они решают?", "user_name": "default_user"},
        {"category": "Testing", "text": "Каковы ключевые различия между ними?", "user_name": "default_user"},
        {"category": "Testing", "text": "Какие шаблоны/техники позволяют изолировать зависимости в ваших тестах?", "user_name": "default_user"},
        {"category": "Testing", "text": "В чем разница между mock и stub? А fake?", "user_name": "default_user"},
        {"category": "Testing", "text": "Как вы можете изолировать сторонние зависимости (например, REST/gRPC/email и т.д.) в ваших тестах?", "user_name": "default_user"},
        {"category": "Testing", "text": "Какой подход к разработке программного обеспечения позволяет писать тестируемый код с самого начала?", "user_name": "default_user"},
        {"category": "Testing", "text": "Как TDD позволяет писать лучший код?", "user_name": "default_user"},
        {"category": "Testing", "text": "Объясните подход/поток TDD.", "user_name": "default_user"},
        {"category": "Testing", "text": "Какова цель BDD?", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Можете ли вы написать простой запрос на две таблицы (объединение двух таблиц)?", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Какие типы JOIN вы знаете?", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "В чем разница между JOIN и UNION?", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Что такое нормализация и денормализация данных и их плюсы и минусы?", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Что такое агрегационная функция? Как фильтровать результаты, возвращаемые агрегационной функцией?", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Что такое транзакция?", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Опишите свойства ACID транзакций.", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Что такое индексы?", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Каковы варианты использования для RDBMS?", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Какие уровни изоляции транзакций вы знаете? Опишите, какие проблемы они решают.", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Что такое оконные функции и их назначение?", "user_name": "default_user"},
        {"category": "Storage & Databases - Relational Databases", "text": "Опишите варианты использования индексов и их плюсы/минусы.", "user_name": "default_user"},
        {"category": "Storage & Databases - Python ORM", "text": "Что такое ORM и его назначение?", "user_name": "default_user"},
        {"category": "Storage & Databases - Python ORM", "text": "Как использовать ORM с новой базой данных?", "user_name": "default_user"},
        {"category": "Storage & Databases - Python ORM", "text": "Как использовать ORM с существующей базой данных?", "user_name": "default_user"},
        {"category": "Storage & Databases - Python ORM", "text": "Каковы соображения производительности при использовании ORM?", "user_name": "default_user"},
        {"category": "Storage & Databases - Python ORM", "text": "Каковы типичные варианты использования ORM? Почему?", "user_name": "default_user"},
        {"category": "Storage & Databases - Python ORM", "text": "Когда лучше не использовать ORM? Почему?", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Поддерживаемые платформы.", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Внедрение зависимостей (регистрация сервисов, время жизни сервисов, проверка области видимости).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Конфигурация (типы провайдеров, иерархия, опции).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Middleware (что это такое, встроенные middleware и т.д.).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Маршрутизация (на основе соглашений, атрибутов, смешанная, области).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Обработка исключений и диагностика (health checks, фильтры исключений, логирование).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Сериализация (Newtonsoft.Json, System.Text.Json).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Модели хостинга (Kestrel, http.sys, IIS, Nginx, in-proc vs out-proc).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Конвейер запросов (в зависимости от модели хостинга).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Фильтры (типы, порядок).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Привязка модели и валидация.", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Безопасность (аутентификация и авторизация, распространенные уязвимости, управление секретами).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Фоновые задачи с использованием hosted services.", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Интеграционные тесты (настройка WebApplicationFactory, WithWebHostBuilder, mock authentication).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Blazor (модели хостинга - WebAssembly, Client/Server-Side, привязка данных, жизненный цикл, обработка событий, управление состоянием).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Web", "text": "Глобализация и локализация.", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Опишите основные аспекты наблюдаемости (логирование, трассировка, мониторинг).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Сравнение обычного текстового и JSON-логирования.", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Зачем нужен мониторинг? Что мониторить?", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Что такое метрики в контексте мониторинга? Типы метрик (счетчик, датчик и т.д.).", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Зачем нужна трассировка? Как она помогает в устранении неполадок?", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Что такое health checks и как их реализовать?", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Что такое протоколы OpenTracing/OpenTelemetry?", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Опишите подходы к логированию в распределенных системах.", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Опишите подходы к доставке логов в распределенных системах.", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Опишите подходы к мониторингу в распределенных системах.", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Как пользовательские метрики могут помочь? Как их реализовать?", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Какая техника позволяет связать сообщение трассировки с сообщениями логов?", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Опишите централизованные решения для логирования? Например, ELK, DataDog и т.д.", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Опишите решения для мониторинга? Например, Prometheus, DataDog и т.д.", "user_name": "default_user"},
        {"category": "Frameworks (ASP.NET Core) - Monitoring, troubleshooting and maintenance", "text": "Опишите решения для трассировки? Например, Zipkin, Jaeger и т.д.", "user_name": "default_user"}]

            for q_data in questions:
                # Проверяем, существует ли вопрос с таким текстом
                existing_question = db.query(Question).filter_by(text=q_data["text"]).first()
                if not existing_question:
                    question = Question(category=q_data["category"], text=q_data["text"], user_name=q_data["user_name"])
                    db.add(question)

            # Добавляем промпты
            prompts = [
                {
                    "name": "QUESTION_PROMPT",
                    "text": """
                        Это продолжение общения не надо здороваться или реагировать на это сообщение, мы просто продолжаем общаться и ты задаёшь следующий вопрос.
                        Вот исходный вопрос для собеседования на Python Junior: {question_text}
                        Задай его, придумав интересную ситуацию с каким-нибудь реальным известным
                        приложением, в контексте которого и будет задаваться вопрос.
                        Стиль общения: Общайся с кандидатом на "ты". Это должна быть беседа двух хороших друзей.
                    """
                },
                {
                    "name": "FEEDBACK_PROMPT",
                    "text": """
                        Проанализируй вопросы на собеседовании для позиции Junior Python Developer и те ответы, которые на каждый
                        из них дал кандидат. Давай обратную связь по его ответам. Оцени собеседование в общем, скажи получается ли он работу или ему надо подготовиться ещё.
                    """
                },
                {
                    "name": "INTERVIEW_PROMPT",
                    "text": """
                        Весело и тепло поприветствуй кандидата на собеседовании, а также расскажи ему о правилах интервью.
                        Тебе не нужно здесь ничего спрашивать у кандидата, мы просто здороваемся и знакомимся.
                        Стиль общения: Общайся с кандидатом на "ты". Это должна быть беседа двух хороших друзей.
                    """
                },
                {
                    "name": "ANSWER_FEEDBACK_PROMPT",
                    "text": """
                        Это продолжение общения не надо здороваться или реагировать на это сообщение, просто продолжаем общаться.
                        Проанализируй ответ кандидата на вопрос: "{question_text}". Ответ кандидата: "{answer_text}".
                        Давай обратную связь: что было правильно, что можно улучшить, и какие рекомендации ты можешь дать.
                        Стиль общения: Общайся с кандидатом на "ты". Это должна быть беседа двух хороших друзей.
                    """
                }
            ]

            for p_data in prompts:
                # Проверяем, существует ли промпт с таким именем
                existing_prompt = db.query(Prompt).filter_by(name=p_data["name"]).first()
                if not existing_prompt:
                    prompt = Prompt(name=p_data["name"], text=p_data["text"])
                    db.add(prompt)

            db.commit()
            self.stdout.write(self.style.SUCCESS("Данные успешно добавлены в базу данных!"))
        except IntegrityError as e:
            db.rollback()  # Откатываем изменения при ошибке
            self.stdout.write(self.style.ERROR(f"Ошибка при добавлении данных: {e}"))
        finally:
            db.close()

