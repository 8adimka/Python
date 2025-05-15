import time
import random
import pyperclip
import requests
from pynput.keyboard import Controller, Key
import sys
import logging
from typing import Optional
from dotenv import load_dotenv
import os
from pynput import keyboard as kb

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='deepseek_solver.log'
)

keyboard = Controller()

class DeepSeekSolver:
    def __init__(self):
        self.API_URL = "https://api.deepseek.com/v1/chat/completions"
        self.API_KEY = self._get_api_key()
        self.last_request_time = 0
        self.RATE_LIMIT_DELAY = 3  # Delay between requests in seconds
        self.TYPING_DELAY_BASE = 0.1  # Base delay for typing

    def _get_api_key(self) -> str:
        """Safely retrieves the API key"""
        load_dotenv()
        key = os.getenv("DEEPSEEK_API_KEY")
        if not key:
            raise ValueError("API key not found in environment variables")
        return key

    def send_to_api(self, prompt: str) -> Optional[str]:
        """Sends a request to the API with error handling"""
        current_time = time.time()
        if current_time - self.last_request_time < self.RATE_LIMIT_DELAY:
            sleep_time = self.RATE_LIMIT_DELAY - (current_time - self.last_request_time)
            time.sleep(sleep_time)

        headers = {
            "Authorization": f"Bearer {self.API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [{
                "role": "user",
                "content": f"{prompt}\n\nSolve the task. The answer should contain only the solution without explanations."
            }],
            "temperature": 0.7,
            "max_tokens": 2000
        }

        try:
            response = requests.post(
                self.API_URL,
                json=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 402:
                logging.error("Payment required. Check your API subscription.")
                return None
                
            response.raise_for_status()
            result = response.json()
            
            if not result.get('choices'):
                logging.error("Invalid API response format: 'choices' field not found.")
                return None
                
            choice = result['choices'][0]
            if not choice.get('message'):
                logging.error("Invalid API response format: 'message' field not found.")
                return None
                
            self.last_request_time = time.time()
            return choice['message'].get('content', '')
            
        except requests.exceptions.RequestException as e:
            logging.error(f"API Request failed: {e}")
            return None
        except Exception as e:
            logging.error(f"Unexpected error while processing API response: {e}")
            return None

    def human_like_typing(self, text: str) -> None:
        """Simulates human-like typing with errors"""
        if not text:
            return

        # Start typing with a slight initial delay
        time.sleep(random.uniform(0.5, 1.5))

        for char in text:
            try:
                # Simulate varying typing speeds
                delay = random.uniform(0.05, 0.15)
                time.sleep(delay)
                
                keyboard.press(char)
                keyboard.release(char)

                # Randomly introduce errors
                if random.random() < 0.02:
                    # Backspace a random number of characters (max 3)
                    backspaces = random.randint(1, min(3, len(text) - (text.index(char) + 1)))
                    for _ in range(backspaces):
                        keyboard.press(Key.backspace)
                        keyboard.release(Key.backspace)
                        time.sleep(random.uniform(0.08, 0.12))
                    
                    # Re-type the correct character and add some noise
                    correct_chars = [char]
                    # Add random lowercase letters as typos
                    correct_chars += [random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(random.randint(1, 2))]
                    
                    for c in correct_chars:
                        keyboard.press(c)
                        keyboard.release(c)
                        time.sleep(random.uniform(0.08, 0.12))
                        
            except Exception as e:
                logging.error(f"Typing error: {e}")
                continue

    def get_clipboard(self) -> Optional[str]:
        """Safely retrieves text from clipboard"""
        try:
            text = pyperclip.paste().strip()
            return text if text else None
        except Exception as e:
            logging.error(f"Clipboard error: {e}")
            return None

    def process_task(self) -> None:
        """Main task processing method"""
        logging.info("Hotkey activated, checking clipboard...")
        task = self.get_clipboard()
        
        if not task:
            logging.warning("No text found in clipboard")
            return

        logging.info(f"Task found: {task[:50]}...")  # Log the start of the task
        solution = self.send_to_api(task)
        
        if solution:
            logging.info("Received solution, typing...")
            self.human_like_typing(solution)
            logging.info("Typing completed successfully")
        else:
            logging.error("Failed to obtain solution from API")

def main():
    print("""\nDeepSeek Solver (Ctrl+Alt+S)
----------------------------------
1. Copy the task to the clipboard
2. Press Ctrl+Alt+S to solve it
3. Ensure the cursor is in the desired field
----------------------------------""")

    # Explicitly set the path to the .env file
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        logging.warning(".env file not found, using system environment variables")

    solver = DeepSeekSolver()
    
    from pynput import keyboard as kb
    
    def on_activate():
        solver.process_task()

    hotkey = kb.GlobalHotKeys({
        '<ctrl>+<alt>+s': on_activate,
        '<ctrl>+<shift>+<space>': on_activate
    })

    try:
        with hotkey:
            logging.info("Service started. Waiting for hotkey...")
            hotkey.join()
    except KeyboardInterrupt:
        logging.info("Service stopped by user")
    except Exception as e:
        logging.critical(f"Fatal error: {e}")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()
    