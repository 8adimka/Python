from sqlalchemy.orm import Session
from bot.models.models import Question
from bot.models.models import Answer
from bot.database import get_db

class InterviewRepository:
    def __init__(self):
        self.db: Session = next(get_db())

    def add_question(self, user_name: str, question_text: str):
        question = Question(user_name=user_name, text=question_text)
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question
    
    def get_user_answers(self, user_name: str):
        """
        Возвращает все ответы пользователя.
        :param user_name: Имя пользователя.
        :return: Список ответов пользователя.
        """
        return self.db.query(Answer).filter(Answer.user_name == user_name).all()

    def get_user_questions_count(self, user_name: str) -> int:
        return (
            self.db.query(Question)
            .filter(Question.user_name == user_name)
            .count()
        )
    
    def get_last_question(self, user_name: str):
        return (
            self.db.query(Question)
            .filter(Question.user_name == user_name)
            .order_by(Question.id.desc())
            .first()
        )

    def add_answer(self, user_name: str, question_id: int, answer_text: str):
        answer = Answer(user_name=user_name, question_id=question_id, text=answer_text)
        self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer

    def get_user_questions(self, user_name: str):
        return self.db.query(Question).filter(Question.user_name == user_name).all()
