import asyncio
from telegram import Update
from telegram.ext import CallbackContext
from bot.services.openai_client import OpenAiClient
from bot.dao.interview_repository import InterviewRepository
from bot.dao.topic_repository import TopicRepository
from bot.models.models import Prompt
import os

class VoiceHandler:
    def __init__(
        self,
        interview_repo: InterviewRepository,
        topic_repo: TopicRepository,
        openai_client: OpenAiClient,
        max_questions: int,
    ):
        self.interview_repo = interview_repo
        self.topic_repo = topic_repo
        self.openai_client = openai_client
        self.max_questions = max_questions

    async def process(self, update: Update, context: CallbackContext):
        if not update.message or not update.message.voice:
            await update.message.reply_text("Ошибка: голосовое сообщение не найдено.")
            return

        user_name = update.message.from_user.username or "Unknown"

        try:
            # Скачиваем голосовое сообщение
            file_path = await self.download_voice(update.message.voice.file_id, context)
        except FileNotFoundError as e:
            await update.message.reply_text(f"Ошибка: {e}")
            return
        except Exception as e:
            await update.message.reply_text(f"Ошибка при скачивании файла: {e}")
            return

        # Транскрибируем голосовое сообщение
        answer = await self.transcribe_voice(update, context)

        # Получаем последний вопрос пользователя
        last_question = self.interview_repo.get_last_question(user_name)
        if last_question:
            self.interview_repo.add_answer(user_name, last_question.id, answer)
        else:
            await update.message.reply_text("Ошибка: не найден предыдущий вопрос.")

        # Проверяем, нужно ли задать следующий вопрос или завершить интервью
        if self.interview_repo.get_user_questions_count(user_name) >= self.max_questions:
            feedback = self.provide_feedback(user_name)
        else:
            feedback = self.ask_next_question(user_name)

        await update.message.reply_text(feedback)

    async def transcribe_voice(self, update: Update, context: CallbackContext) -> str:
        voice = update.message.voice
        file_id = voice.file_id
        file_path = await self.download_voice(file_id, context)
        return self.openai_client.transcribe(file_path)

    async def download_voice(self, file_id: str, context: CallbackContext) -> str:
        file = await context.bot.get_file(file_id)  # Получаем объект File
        file_path = f"/tmp/{file_id}.ogg"
        
        # Скачиваем файл асинхронно
        await file.download_to_drive(file_path)
        
        # Проверяем, что файл существует
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не был сохранен.")
        
        return file_path

    def ask_next_question(self, user_name: str) -> str:
        prompt_obj = Prompt.get_prompt_by_name("QUESTION_PROMPT")
        if not prompt_obj:
            return "Ошибка: шаблон вопроса не найден."

        # Получаем случайный вопрос из базы данных
        question = self.openai_client.get_random_question_from_db()
        if not question:
            return "Ошибка: не найдены вопросы в базе данных."

        # Заменяем {question_text} на конкретный вопрос
        prompt_text = prompt_obj.text.format(question_text=question.text)

        # Генерируем вопрос с помощью OpenAI
        generated_question = self.openai_client.prompt_model(Prompt(text=prompt_text))
        
        if not generated_question:
            return "Ошибка: не удалось сформулировать вопрос."

        # Сохраняем вопрос в базе данных
        self.interview_repo.add_question(user_name, generated_question)

        return generated_question

    def provide_feedback(self, user_name: str) -> str:
        prompt_obj = Prompt.get_prompt_by_name("FEEDBACK_PROMPT")
        if not prompt_obj:
            return "Ошибка: шаблон отзыва не найден."

        self.interview_repo.finish_interview(user_name)

        return prompt_obj.text
    
    