import anthropic
import openai
from typing import List, Dict, Optional
from app.core.config import settings
from app.utils.protocols import find_relevant_protocol
import tiktoken


class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        if self.provider == "anthropic":
            self.client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
            self.model = settings.LLM_MODEL
        elif self.provider == "openai":
            self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            self.model = settings.LLM_MODEL or "gpt-4-turbo-preview"

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            if self.provider == "anthropic":
                # Rough estimation for Claude (1 token ≈ 4 characters)
                return len(text) // 4
            else:
                encoding = tiktoken.encoding_for_model("gpt-4")
                return len(encoding.encode(text))
        except Exception:
            # Fallback estimation
            return len(text) // 4

    def trim_conversation_history(
        self, messages: List[Dict[str, str]], max_tokens: int
    ) -> List[Dict[str, str]]:
        """Trim conversation history to fit within token limit"""
        total_tokens = sum(self.count_tokens(msg["content"]) for msg in messages)

        if total_tokens <= max_tokens:
            return messages

        # Keep system message and recent messages
        trimmed = []
        current_tokens = 0

        # Always keep system message if present
        if messages and messages[0]["role"] == "system":
            trimmed.append(messages[0])
            current_tokens += self.count_tokens(messages[0]["content"])
            messages = messages[1:]

        # Add messages from most recent, working backwards
        for msg in reversed(messages):
            msg_tokens = self.count_tokens(msg["content"])
            if current_tokens + msg_tokens <= max_tokens:
                trimmed.insert(1 if trimmed and trimmed[0]["role"] == "system" else 0, msg)
                current_tokens += msg_tokens
            else:
                break

        return trimmed

    def create_system_prompt(
        self,
        user_info: Optional[Dict] = None,
        memories: Optional[List[str]] = None,
        protocols: Optional[str] = None,
    ) -> str:
        """Create system prompt with context"""
        base_prompt = """You are Disha, India's first AI health coach. You are warm, empathetic, and knowledgeable about health and wellness.

**Your Role:**
- Provide personalized health guidance and support
- Help users understand their health concerns
- Offer evidence-based wellness advice
- Be a supportive companion on their health journey

**Communication Style:**
- Warm and conversational, like chatting with a trusted friend on WhatsApp
- Use simple, easy-to-understand language
- Show empathy and understanding
- Ask follow-up questions to better understand concerns
- Be encouraging and supportive
- Use appropriate emojis occasionally to be friendly (but don't overdo it)

**Important Guidelines:**
- You are NOT a replacement for professional medical care
- For serious symptoms, always recommend consulting a healthcare provider
- For emergencies (severe chest pain, difficulty breathing, etc.), advise calling emergency services
- Be honest about the limitations of AI health coaching
- Focus on prevention, lifestyle, and general wellness
- Provide information, not diagnosis

**Safety First:**
- If symptoms suggest serious condition: recommend immediate medical attention
- If user is in crisis: provide crisis helpline numbers and urge professional help
- Never provide specific medication dosages or change existing prescriptions
"""

        # Add user context
        if user_info:
            user_context = "\n**User Information:**\n"
            if user_info.get("name"):
                user_context += f"- Name: {user_info['name']}\n"
            if user_info.get("age"):
                user_context += f"- Age: {user_info['age']}\n"
            if user_info.get("gender"):
                user_context += f"- Gender: {user_info['gender']}\n"
            if user_info.get("medical_conditions"):
                user_context += f"- Medical Conditions: {', '.join(user_info['medical_conditions'])}\n"
            if user_info.get("medications"):
                user_context += f"- Current Medications: {', '.join(user_info['medications'])}\n"
            if user_info.get("allergies"):
                user_context += f"- Allergies: {', '.join(user_info['allergies'])}\n"
            base_prompt += user_context

        # Add memories
        if memories:
            memory_context = "\n**What You Remember About This User:**\n"
            for memory in memories:
                memory_context += f"- {memory}\n"
            base_prompt += memory_context

        # Add relevant protocols
        if protocols:
            base_prompt += f"\n**Relevant Medical Protocols:**\n{protocols}\n"

        return base_prompt

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        user_info: Optional[Dict] = None,
        memories: Optional[List[str]] = None,
        user_message: Optional[str] = None,
    ) -> str:
        """Generate AI response"""
        try:
            # Find relevant protocols
            protocols = ""
            if user_message:
                protocols = find_relevant_protocol(user_message)

            # Create system prompt
            system_prompt = self.create_system_prompt(user_info, memories, protocols)

            # Prepare messages
            if self.provider == "anthropic":
                # Trim conversation to fit context window
                available_tokens = settings.MAX_CONTEXT_TOKENS - self.count_tokens(system_prompt)
                trimmed_messages = self.trim_conversation_history(messages, available_tokens)

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=settings.MAX_RESPONSE_TOKENS,
                    system=system_prompt,
                    messages=trimmed_messages,
                )
                return response.content[0].text

            elif self.provider == "openai":
                # Prepare messages with system prompt
                full_messages = [{"role": "system", "content": system_prompt}] + messages

                # Trim to fit context
                trimmed_messages = self.trim_conversation_history(
                    full_messages, settings.MAX_CONTEXT_TOKENS
                )

                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=trimmed_messages,
                    max_tokens=settings.MAX_RESPONSE_TOKENS,
                )
                return response.choices[0].message.content

        except Exception as e:
            print(f"LLM Error: {e}")
            return "I apologize, but I'm having trouble responding right now. Please try again in a moment. If this persists, please contact support."

    async def generate_onboarding_message(self) -> str:
        """Generate initial onboarding message"""
        return """Hi there! 👋 I'm Disha, your AI health coach. I'm so glad you're here!

I'm here to help you with your health and wellness journey. Think of me as your friendly health companion - someone you can talk to anytime about your health concerns, wellness goals, or just general questions.

Before we start, I'd love to get to know you a bit better so I can provide more personalized support. Could you share:

1. What should I call you?
2. How old are you?
3. Do you have any ongoing health conditions I should know about?
4. Are you currently taking any medications?
5. Any allergies?

Don't worry if you'd rather not share everything now - you can tell me more as we go along. What would you like to start with? 😊"""


llm_service = LLMService()
