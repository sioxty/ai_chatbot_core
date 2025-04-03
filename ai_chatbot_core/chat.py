import aiohttp
from .types import Message, StartMessage, Model
import re
import logging

logger = logging.getLogger("agent")

def remove_think_content(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

class Chat:
    def __init__(self, api_key, user_id=1, start_message: str = None, model=Model.DEEPSEEK_R1):
        self.api_key = api_key
        self.user_id = user_id
        self.model: Model = model
        self.messages: list[Message] = [StartMessage(start_message)]

    async def add_message(self, role: str, content: str):
        """
        Adds a new message to the chat history.

        Args:
            role (str): The role of the message sender (e.g., "user" or "assistant").
            content (str): The content of the message.

        Returns:
            None
        """
        self.messages.append(Message(content, role))

    async def get_messages(self) -> list[dict]:
        """
        Retrieves the chat history as a list of dictionaries.

        Each dictionary represents a message and contains the following keys:
        - "role": The role of the message sender.
        - "content": The content of the message.

        Returns:
            list[dict]: A list of dictionaries representing the chat history.
        """
        return [message.get_content() for message in self.messages]

    async def get_response(self, content):
        url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
        await self.add_message("user", content)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        messages = await self.get_messages()
        data = {"model": self.model.value, "messages": messages}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        content = await response.json()
                        ai_message = content["choices"][0]["message"]
                        ai_content = remove_think_content(ai_message["content"])
                        await self.add_message(ai_message["role"], ai_content)
                        return ai_content

                    logger.error(f"Error: {response.status}")
                    logger.error(await response.text())
                    return "An error occurred while processing your request."
            except aiohttp.ClientError as e:
                logger.error(f"Aiohttp client error: {e}")
                return "An error occurred while processing your request."

    async def clear_chat(self):
        self.messages.clear()
        self.messages.append(StartMessage())

    def __eq__(self, other):
        if isinstance(other, Chat):
            return self.user_id == other.user_id
        elif isinstance(other, int):
            return self.user_id == other
        return NotImplemented
