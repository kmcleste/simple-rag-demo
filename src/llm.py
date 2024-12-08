# llm.py
from openai import OpenAI
from typing import Optional


class LLMBackend:
    def __init__(
        self,
        model: str = "hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4",
        temperature: float = 0.7,
    ):
        self.client = OpenAI(api_key="fake-key", base_url="http://127.0.0.1:8001/v1")
        self.model = model
        self.temperature = temperature

    def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=1000,
        )

        return response.choices[0].message.content
