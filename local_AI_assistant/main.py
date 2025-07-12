import signal
from pathlib import Path

from assistant.dialogue_manager import DialogueManager
from assistant.model import LocalLLMRunner

HISTORY_PATH = Path.home() / "local_AI_assistant/history.json"
MODEL_DIR = "/home/v/LLM_source/Mistral-7B"


def signal_handler(sig, frame):
    print("\n[!] Выход...")
    exit(0)


signal.signal(signal.SIGINT, signal_handler)


def main():
    try:
        print("\n[~] Загружаю модель...")
        llm = LocalLLMRunner(model_path=MODEL_DIR)
        dialogue = DialogueManager(HISTORY_PATH)

        print(
            "\n[AI Assistant] Привет! Задай мне вопрос или напиши 'выход' чтобы закончить.\n"
        )

        while True:
            try:
                user_input = input("Вы: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ("выход", "exit", "quit"):
                    break

                # Добавляем сообщение и получаем ответ
                dialogue.add_user_message(user_input)
                response = dialogue.get_response(llm)
                print(f"\nАссистент: {response}\n")

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"[ОШИБКА] {str(e)}")
                continue

    except Exception as e:
        print(f"[КРИТИЧЕСКАЯ ОШИБКА] {str(e)}")
    finally:
        print("\n[!] Завершаю работу...")


if __name__ == "__main__":
    main()
