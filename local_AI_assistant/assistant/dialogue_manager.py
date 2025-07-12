import json
from pathlib import Path
from typing import Dict, List


class DialogueManager:
    def __init__(self, history_path: Path, max_history: int = 30):
        self.history_path = history_path
        self.max_history = max_history
        self.history: List[Dict[str, str]] = []
        self.summary: str = ""
        self._load_history()

    def _load_history(self):
        try:
            if self.history_path.exists():
                with open(self.history_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.history = data.get("messages", [])
                    self.summary = data.get("summary", "")
        except Exception as e:
            print(f"[WARNING] Ошибка загрузки истории: {e}")

    def _save_history(self):
        try:
            self.history_path.parent.mkdir(exist_ok=True)
            with open(self.history_path, "w", encoding="utf-8") as f:
                json.dump(
                    {"messages": self.history, "summary": self.summary},
                    f,
                    ensure_ascii=False,
                    indent=2,
                )
        except Exception as e:
            print(f"[WARNING] Ошибка сохранения истории: {e}")

    def add_user_message(self, text: str):
        self.history.append({"role": "user", "content": text})

    def add_assistant_message(self, text: str):
        self.history.append({"role": "assistant", "content": text})
        self._save_history()

    def build_prompt(self) -> str:
        prompt = [
            "Ты — AI ассистент. Если тебя просят написать код, обязательно отвечай в markdown-блоке ```python ... ```. "
            "Вот пример:\n\n"
            "Пользователь: Напиши функцию на Python, которая возвращает квадрат числа.\n"
            "Ассистент: ```python\ndef square(x):\n    return x * x\n```"
        ]

        if self.summary:
            prompt.append("[Сводка предыдущей беседы]:")
            prompt.append(self.summary.strip())

        prompt.append("Текущий диалог:")

        for msg in self.history[-self.max_history :]:
            role = "Пользователь" if msg["role"] == "user" else "Ассистент"
            prompt.append(f"{role}: {msg['content'].strip()}")

        prompt.append("Ассистент:")
        return "\n".join(prompt)

    def is_near_limit(
        self, prompt: str, tokenizer, max_tokens: int = 8192, buffer: int = 512
    ) -> bool:
        try:
            tokens = tokenizer(prompt, return_tensors="pt")["input_ids"][0]
            return len(tokens) >= (max_tokens - buffer)
        except Exception as e:
            print(f"[WARNING] Не удалось измерить длину токенов: {e}")
            return False

    def summarize(self, llm, max_summary_tokens: int = 256):
        print("[~] Генерирую выжимку из истории...")
        try:
            summary_prompt = (
                "Ты — ассистент. Составь краткое содержание следующей беседы "
                "(основные вопросы пользователя и ключевые ответы):\n\n"
            )
            for msg in self.history:
                role = "Пользователь" if msg["role"] == "user" else "Ассистент"
                summary_prompt += f"{role}: {msg['content'].strip()}\n"

            summary_prompt += "\nСводка:"
            summary = llm.generate_response(
                summary_prompt, max_tokens=max_summary_tokens
            ).strip()

            if summary:
                self.summary = summary
                self.history = []  # очищаем подробную историю
                self._save_history()
                print("[✓] Выжимка обновлена.")
            else:
                print("[!] Пустой результат выжимки.")
        except Exception as e:
            print(f"[ОШИБКА] Не удалось создать summary: {e}")

    def get_response(self, llm) -> str:
        prompt = self.build_prompt()

        if self.is_near_limit(prompt, llm.tokenizer):
            self.summarize(llm)
            prompt = self.build_prompt()

        response = llm.generate_response(prompt)
        self.add_assistant_message(response)
        return response
