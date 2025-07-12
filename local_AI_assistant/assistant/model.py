import os
import re

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig


class LocalLLMRunner:
    def __init__(self, model_path: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto",
            quantization_config=quant_config,
            torch_dtype=torch.bfloat16,
        )

    def generate_response(self, prompt: str, max_new_tokens: int = 768) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True).to(
            self.model.device
        )

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=0.3,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.1,
            )

        response = self.tokenizer.decode(
            outputs[0][inputs.input_ids.shape[1] :], skip_special_tokens=True
        )

        response = response.split("Пользователь:")[0].strip()
        self._try_save_code(response)
        print("ОТЛАДКА ОТВЕТА:\n", repr(response))
        return response if response else "[пустой ответ]"

    def _try_save_code(self, response: str):
        match = re.search(r"```(?:python)?\\n(.*?)```", response, re.DOTALL)
        if not match:
            return  # нет кода

        code = match.group(1).strip()
        if not code:
            return

        # Определение имени файла
        first_line = code.splitlines()[0] if code else ""
        if "fastapi" in first_line.lower():
            filename = "main.py"
        elif "flask" in first_line.lower():
            filename = "flask_app.py"
        elif first_line.strip().startswith("def "):
            filename = "function.py"
        else:
            filename = "snippet.py"

        save_dir = os.path.expanduser("~/projects/local_AI_assistant/code_samples")
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, filename)

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code.strip() + "\n")
            print(f"\n💾 Код сохранён в: {file_path}\n")
        except Exception as e:
            print(f"[Ошибка сохранения кода] {e}")
