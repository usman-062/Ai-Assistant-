import ollama
from openai import OpenAI
import google.generativeai as genai
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class AIProvider:
    def __init__(self):
        # Initialize Cloud Clients
        if settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
        else:
            self.openai_client = None

        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
        else:
            self.gemini_client = None

    async def generate_text(self, prompt: str, history: list = None):
        """Generates a text response, prioritizing Ollama."""
        try:
            # Try Local Ollama first
            response = ollama.chat(
                model=settings.DEFAULT_MODEL,
                messages=[{'role': 'user', 'content': prompt}] if not history else history + [{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
        except Exception as e:
            logger.warning(f"Ollama failed: {e}. Falling back to Cloud AI.")
            return await self._fallback_generate_text(prompt, history)

    async def analyze_image(self, image_path: str, prompt: str):
        """Analyzes an image using Ollama multimodal or Cloud AI fallback."""
        try:
            # Ollama Multimodal
            with open(image_path, 'rb') as f:
                img_data = f.read()

            response = ollama.generate(
                model=settings.DEFAULT_MODEL,
                prompt=prompt,
                images=[img_data]
            )
            return response['response']
        except Exception as e:
            logger.warning(f"Ollama Vision failed: {e}. Falling back to Cloud AI.")
            return await self._fallback_analyze_image(image_path, prompt)

    async def _fallback_generate_text(self, prompt: str, history: list):
        if self.openai_client:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content

        # Simple fallback if no keys provided
        return "I'm sorry, I'm currently unable to reach my AI brain. Please ensure Ollama is running or API keys are configured."

    async def _fallback_analyze_image(self, image_path: str, prompt: str):
        # Implementation for OpenAI/Gemini vision would go here
        return "Vision fallback not fully implemented, but I can see you're trying to analyze an image!"

ai_provider = AIProvider()
