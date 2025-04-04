from .chat import Chat
from .types import Model

class ChatManager:
    """
    Manages multiple chat instances for different users.

    This class handles the creation, retrieval, addition, and removal of chat instances.
    It also manages the API key, default model, and start message for all chats.
    """
    
    
    def __init__(self, api_key: str, model: Model = Model.DEEPSEEK_R1, start_message: str = None):
        """
        Initializes the ManegerChat with an API key, default model, and start message.

        Args:
            api_key (str): The API key for accessing the chat service.
            model (Model, optional): The default model to use for new chats. Defaults to Model.DEEPSEEK_R1.
            start_message (str, optional): The default start message for new chats. Defaults to "You are a helpful assistant.".
        """
        self.__api_key: str = api_key
        self.chats: dict[int, Chat] = {}
        self.model: Model = model
        self.__start_message: str = "You are a helpful assistant." if start_message is None else start_message
    
    async def __create_chat(self, user_id: int) -> Chat:
        """
        Creates a new chat instance for a given user ID.

        Args:
            user_id (int): The ID of the user for whom to create a chat.

        Returns:
            Chat: The newly created chat instance.
        """
        chat = Chat(
            api_key=self.__api_key,
            user_id=user_id,
            start_message=self.__start_message,
            model=self.model
        )
        await self.add_chat(chat) 
        return chat
    
    async def connect_chat(self, user_id: int) -> Chat:
        """
        Connects to an existing chat or creates a new one if it doesn't exist.

        Args:
            user_id (int): The ID of the user for whom to connect or create a chat.

        Returns:
            Chat: The connected or newly created chat instance.
        """
        chat = await self.get_chat(user_id)
        if chat is None:
            chat = await self.__create_chat(user_id)                  
        return chat
    
    async def get_chat(self, user_id: int) -> Chat:
        """
        Retrieves a chat instance for a given user ID.

        Args:
            user_id (int): The ID of the user whose chat to retrieve.

        Returns:
            Chat: The chat instance if found, otherwise None.
        """
        return self.chats.get(user_id)
    
    async def add_chat(self, chat: Chat):
        self.chats[chat.user_id] = chat

    async def remove_chat(self, user_id: int):
        del self.chats[user_id]
