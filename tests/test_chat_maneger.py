import asyncio
import unittest
from unittest.mock import AsyncMock, patch

from ai_chatbot_core.chat import Chat
from ai_chatbot_core.chat_maneger import ChatManager
from ai_chatbot_core.types import Model


class TestChatManager(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.model = Model.DEEPSEEK_R1
        self.start_message = "Test start message"
        self.manager = ChatManager(self.api_key, self.model, self.start_message)

    async def test_create_chat(self):
        user_id = 1
        chat = await self.manager._ChatManager__create_chat(user_id)
        self.assertIsInstance(chat, Chat)
        self.assertEqual(chat.user_id, user_id)
        self.assertEqual(chat.api_key, self.api_key)
        self.assertEqual(chat.model, self.model)
        self.assertEqual(chat.messages[0].content, self.start_message)

    async def test_connect_chat_new(self):
        user_id = 2
        chat = await self.manager.connect_chat(user_id)
        self.assertIsInstance(chat, Chat)
        self.assertEqual(chat.user_id, user_id)
        self.assertIn(user_id, self.manager.chats)

    async def test_connect_chat_existing(self):
        user_id = 3
        await self.manager._ChatManager__create_chat(user_id)
        chat1 = await self.manager.get_chat(user_id)
        chat2 = await self.manager.connect_chat(user_id)
        self.assertEqual(chat1, chat2)

    async def test_get_chat(self):
        user_id = 4
        await self.manager._ChatManager__create_chat(user_id)
        chat = await self.manager.get_chat(user_id)
        self.assertIsInstance(chat, Chat)
        self.assertEqual(chat.user_id, user_id)

    async def test_get_chat_not_found(self):
        user_id = 5
        chat = await self.manager.get_chat(user_id)
        self.assertIsNone(chat)

    async def test_add_chat(self):
        user_id = 6
        chat = Chat(self.api_key, user_id, self.start_message, self.model)
        await self.manager.add_chat(chat)
        self.assertIn(user_id, self.manager.chats)
        self.assertEqual(self.manager.chats[user_id], chat)

    async def test_remove_chat(self):
        user_id = 7
        await self.manager._ChatManager__create_chat(user_id)
        await self.manager.remove_chat(user_id)
        self.assertNotIn(user_id, self.manager.chats)

    async def test_default_start_message(self):
        manager = ChatManager(self.api_key)
        user_id = 8
        chat = await manager._ChatManager__create_chat(user_id)
        self.assertEqual(chat.messages[0].content, "You are a helpful assistant.")

    async def test_default_model(self):
        manager = ChatManager(self.api_key)
        user_id = 9
        chat = await manager._ChatManager__create_chat(user_id)
        self.assertEqual(chat.model, Model.DEEPSEEK_R1)


if __name__ == "__main__":
    unittest.main()
