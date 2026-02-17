from google import genai
from app.core.settings import Settings


class GeminiProvider:
    def __init__(self, settings: Settings):
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.ai_model

    def generate(self, messages, temperature=0.7):
        prompt = ""

        for msg in messages:
            role = msg.role
            content = msg.content
            prompt += f"{role}: {content}\n"

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text
