import { z } from "zod";

export const MessageSchema = z.object({
  id: z.string(),
  role: z.enum(["user", "assistant"]),
  content: z.string(),
  timestamp: z.string(),
  attachments: z.array(z.string()).optional(),
});

export type Message = z.infer<typeof MessageSchema>;

export interface ChatSession {
  id: string;
  title: string;
  createdAt: string;
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
}
