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
            questions = [
                {"category": "ООП", "text": "Что такое объектно-ориентированное программирование и его основные принципы?", "user_name": "default_user"},
                {"category": "ООП", "text": "В чем заключается разница между наследованием и композицией?", "user_name": "default_user"},
                {"category": "ООП", "text": "Как реализуется полиморфизм в Python и какие его преимущества?", "user_name": "default_user"},
                {"category": "Исключения", "text": "Как правильно использовать конструкцию `try-except-finally`?", "user_name": "default_user"},
                {"category": "Коллекции", "text": "Как устроен словарь (dict) в Python и каким образом он обрабатывает коллизии хешей?", "user_name": "default_user"},
                {"category": "Коллекции", "text": "Что такое хеш-функция и как она влияет на производительность словаря?", "user_name": "default_user"},
                {"category": "Многопоточность", "text": "Как создать новый поток в Python, используя модуль `threading`?", "user_name": "default_user"},
                {"category": "Многопоточность", "text": "Чем отличается вызов метода `start()` у потока от вызова `run()` напрямую?", "user_name": "default_user"},
            ]

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
                    из них дал кандидат. Давай обратную связь по его ответам.
                """
            },
            {
                "name": "INTERVIEW_PROMPT",
                "text": """
                    Весело и тепло поприветствуй кандидата на собеседовании, а также расскажи ему о правилах интервью.
                    Стиль общения: Общайся с кандидатом на "ты". Это должна быть беседа двух хороших друзей.
                """
            },
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
