import unittest
from unittest.mock import patch
from ai_chatbot_core.chat_maneger import ManegerChat
from ai_chatbot_core.chat import Chat
from ai_chatbot_core.types import Model


class TestManegerChat(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.manager = ManegerChat(self.api_key)

    def test_manager_initialization(self):
        self.assertEqual(self.manager.api_key, self.api_key)
        self.assertEqual(self.manager.chats, {})
        self.assertEqual(self.manager.model, Model.DEEPSEEK_R1)
        self.assertEqual(self.manager.start_message, "You are a helpful assistant.")

    def test_manager_initialization_with_custom_values(self):
        custom_start_message = "Custom start message"
        custom_model = Model.QWEN_QWQ_32B
        manager = ManegerChat(self.api_key, model=custom_model, start_message=custom_start_message)
        self.assertEqual(manager.api_key, self.api_key)
        self.assertEqual(manager.chats, {})
        self.assertEqual(manager.model, custom_model)
        self.assertEqual(manager.start_message, custom_start_message)

    def test_create_chat(self):
        chat = self.manager._ManegerChat__create_chat(1)
        self.assertIsInstance(chat, Chat)
        self.assertEqual(chat.api_key, self.api_key)
        self.assertEqual(chat.user_id, 1)
        self.assertEqual(chat.messages[0].content, "You are a helpful assistant.")
        self.assertEqual(chat.model, Model.DEEPSEEK_R1)

    def test_connect_chat_new_user(self):
        chat = self.manager.connect_chat(1)
        self.assertIsInstance(chat, Chat)
        self.assertEqual(chat.user_id, 1)
        self.assertIn(1, self.manager.chats)
        self.assertEqual(self.manager.chats[1], chat)

    def test_connect_chat_existing_user(self):
        chat1 = self.manager.connect_chat(1)
        chat2 = self.manager.connect_chat(1)
        self.assertEqual(chat1, chat2)
        self.assertEqual(len(self.manager.chats), 1)

    def test_get_chat_existing_user(self):
        chat = self.manager.connect_chat(1)
        retrieved_chat = self.manager.get_chat(1)
        self.assertEqual(retrieved_chat, chat)

    def test_get_chat_nonexistent_user(self):
        retrieved_chat = self.manager.get_chat(1)
        self.assertIsNone(retrieved_chat)

    def test_add_chat(self):
        chat = Chat(self.api_key, user_id=123)
        self.manager.add_chat(chat)
        self.assertIn(123, self.manager.chats)
        self.assertEqual(self.manager.chats[123], chat)

    def test_remove_chat(self):
        chat = self.manager.connect_chat(1)
        self.manager.remove_chat(1)
        self.assertNotIn(1, self.manager.chats)
        self.assertIsNone(self.manager.get_chat(1))

if __name__ == '__main__':
    unittest.main()