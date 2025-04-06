import aiohttp
import re
import logging

from .config import api_url
from .types import Message, StartMessage, Model


logger = logging.getLogger("agent")


def remove_think_content(text: str) -> str:
    """
    Removes content enclosed within <think> tags from a given string.

    Args:
        text (str): The input string potentially containing <think> tags.

    Returns:
        str: The string with <think> content removed.
    """
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


class Chat:
    """
    Represents a chat session with an AI model.

    Manages the chat history, interacts with the AI API, and handles
    message processing.
    """

    def __init__(
        self,
        api_key: str,
        user_id: int = 1,
        start_message: str = None,
        model: Model = Model.DEEPSEEK_R1,
        history: bool = True,
    ):
        """
        Initializes a new chat session.

        Args:
            api_key (str): The API key for accessing the chat service.
            user_id (int, optional): The ID of the user. Defaults to 1.
            start_message (str, optional): The initial message.
                Defaults to None.
            model (Model, optional): The AI model to use.
                Defaults to Model.DEEPSEEK_R1.
            history (bool, optional): Whether to store the chat history.
                Defaults to True.
        """
        self.api_key: str = str(api_key)
        self.user_id: int = int(user_id)
        self.model: Model = model
        self.__history: bool = bool(history)
        self.messages: list[Message] = [StartMessage(start_message)]

    async def add_message(self, role: str, content: str):
        """
        Adds a new message to the chat history.

        The message is stored as a Message object in the chat's message list.
        This method is used to record both user inputs and AI responses.
        
        The role parameter specifies whether the message is from the user
        or the assistant, and the content parameter contains the text of the
        message.

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

        This method is used to format the chat history into a structure
        that can be sent to the AI API.
        Retrieves the chat history as a list of dictionaries.

        Each dictionary represents a message and contains the following keys:
        - "role": The role of the message sender.
        - "content": The content of the message.

        Returns:
            list[dict]: A list of dictionaries representing the chat history.
        """
        return [message.get_content() for message in self.messages]

    async def get_response(self, content: str) -> str:
        """
        Gets a response from the AI model for a given message.

        This method sends the current chat history to the AI API,
        receives the AI's response, and adds it to the chat history.
        It also handles API errors and returns a user-friendly error message
        if something goes wrong.

        Args:
            content (str): The content of the user's message.

        Returns:
            str: The AI's response or an error message.
        """
        await self.add_message("user", str(content))

        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        messages: list[dict] = await self.get_messages()
        data: dict[str, list | str] = {"model": self.model.value, "messages": messages}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    api_url, headers=headers, json=data
                ) as response:
                    if response.status == 200:
                        return await self._process_response(response)
                    else:
                        logger.error(f"Error: {response.status}")
                        logger.error(await response.text())
                        return "An error occurred while processing your request."
            except aiohttp.ClientError as error:
                logger.error(f"Aiohttp client error: {error}")
                return "An error occurred while processing your request."

    async def _process_response(self, response: aiohttp.ClientResponse) -> str:
        """
        Processes the response from the AI API.

        Extracts the AI's message from the response, removes any <think>
        content, adds the message to the chat history, and returns the
        processed content.

        Args:
            response (aiohttp.ClientResponse): The response from the AI API.

        Returns:
            str: The processed content of the AI's message.
        """
        content: dict = await response.json()
        ai_message: dict = content["choices"][0]["message"]
        ai_content: str = remove_think_content(ai_message["content"])
        if self.__history:
            await self.add_message(ai_message["role"], ai_content)
        return ai_content

    async def clear_chat(self) -> None:
        """Clears the chat history and resets it with a start message."""
        self.messages.clear()
        self.messages.append(StartMessage())

    def __eq__(self, other: object) -> bool:
        """
        Checks if this chat is equal to another object.
        """
        if isinstance(other, Chat):
            return self.user_id == other.user_id
        elif isinstance(other, int):
            return self.user_id == other
        return NotImplemented
