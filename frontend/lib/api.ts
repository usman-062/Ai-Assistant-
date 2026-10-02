import { Message, ChatSession } from "@/types";

export async function sendMessage(message: string, sessionId: string, attachments: string[] = []): Promise<Message> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, sessionId, attachments }),
  });

  if (!response.ok) throw new Error("Failed to send message");
  return response.json();
}

export async function getChatHistory(sessionId: string): Promise<Message[]> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/history/${sessionId}`);
  if (!response.ok) throw new Error("Failed to fetch history");
  return response.json();
}

export async function uploadImage(file: File): Promise<string> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) throw new Error("Failed to upload image");
  const data = await response.json();
  return data.url;
}
