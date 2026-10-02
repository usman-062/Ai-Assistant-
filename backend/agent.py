import asyncio
from livekit.agents import JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from app.core.config import settings

async def entrypoint(ctx: JobContext):
    # Initialize the voice assistant
    # Note: In a real production app, we'd integrate with the AIProvider logic
    # For the LiveKit Agent, we use their specialized plugins.

    initial_ctx = llm.ChatContext().append(
        role="system",
        text="You are a helpful AI Assistant. Your voice is friendly and concise."
    )

    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
        chat_ctx=initial_ctx,
    )

    await ctx.connect()
    assistant.start(ctx.room)

    await assistant.say("Hello! I am your AI Assistant. How can I help you today?")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
