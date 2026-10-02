# Ai-Assistant

## Stack

* **Frontend:** Node 24, Next.js 16, React 19, TypeScript 7, Tailwind CSS 4, shadcn/ui, LiveKit Components React — `frontend/` :3000
* **Backend / Agent:** FastAPI, Python 3.13, LiveKit Agents framework, uv, Ruff, Pytest — `backend/` :8000
* **Local AI:** Ollama — `localhost:11434`, `gemma3:1b` (Multimodal support for images)
* **Cloud AI:** OpenAI / Gemini (with Vision capabilities for image processing & voice pipelines) — fallback providers

## Core Features & Capabilities

* **1. Chat Feature:** Full-stack text chat interface with persistent context and history.
* **2. Voice Feature:** Real-time conversational voice interaction using LiveKit Voice agents and WebRTC.
* **3. Image Attachment Feature:** Multimodal image/photo handling allowing users to upload or attach images for the AI agent to analyze.

## Commands

```bash
# Frontend
cd frontend
npm install
npm run dev
npm install <package-name>

# Backend / Agent Worker
cd backend
uv sync
uv run python agent.py start   # Start LiveKit Agent worker
uv run fastapi dev             # Start FastAPI server
uv add <package-name>

# Tests
cd backend
pytest