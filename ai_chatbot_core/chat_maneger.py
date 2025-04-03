from .chat import Chat
from .types import Model

class ManegerChat:
    def __init__(self,api_key: str,model:Model=Model.DEEPSEEK_R1,start_message: str=None):
        self.api_key: str = api_key
        self.chats : dict[Chat] = {}
        self.model:Model = model
        self.start_message:str = "You are a helpful assistant." if start_message is None else start_message
    
    def __create_chat(self,user_id)-> Chat:
        chat= Chat(
            api_key=self.api_key,
            user_id=user_id,
            start_message = self.start_message,
            model=self.model
            )
        self.add_chat(chat) 
        return chat
    
    def connect_chat(self,user_id)->Chat:
        chat = self.get_chat(user_id)
        if chat is None:
            chat = self.__create_chat(user_id)                  
        return chat
    
    def get_chat(self,user_id)->Chat:
        return self.chats.get(user_id)
    
    def add_chat(self,chat: Chat):
        self.chats[chat.user_id] = chat

    def remove_chat(self,user_id):
        del self.chats[user_id]