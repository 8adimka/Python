from telegram import Update
from bot.services.openai_client import OpenAiClient
from bot.dao.topic_repository import TopicRepository
from bot.models.models import Prompt
from bot.dao.interview_repository import InterviewRepository

async def start_handler(update: Update, context):
    user_name = update.message.from_user.username  # Используется для логирования или персонализации
    openai_client = OpenAiClient()
    topic_repo = TopicRepository()
    interview_repo = InterviewRepository()

    try:
        # Получаем приветственное сообщение
        interview_prompt = Prompt.get_prompt_by_name("INTERVIEW_PROMPT")
        welcome_message = openai_client.prompt_model(interview_prompt)

        # Отправляем приветственное сообщение
        await update.message.reply_text(welcome_message)

        # Задаем первый вопрос
        question_prompt = Prompt.get_prompt_by_name("QUESTION_PROMPT")
        first_question = openai_client.prompt_model(question_prompt)

        # Сохраняем первый вопрос
        question = interview_repo.add_question(user_name, first_question)
        
        # Отправляем первый вопрос
        await update.message.reply_text(first_question)

        # Логируем старт интервью с именем пользователя
        print(f"User {user_name} started the interview.")
    except Exception as e:
        print(f"Error occurred: {e}")
        await update.message.reply_text("Произошла ошибка при обработке запроса. Попробуйте позже.")
