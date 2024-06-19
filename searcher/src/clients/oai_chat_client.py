from core_classes import LLM
from openai import OpenAI


class OAIChatClient(LLM):
    model: str
    client: OpenAI

    def __init__(self, chat_model: str, OPENAI_API_KEY: str):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = chat_model

    def inference(self, messages, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message
