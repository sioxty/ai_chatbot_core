import unittest
from unittest.mock import patch, AsyncMock
from ai_chatbot_core.chat import Chat, remove_think_content
from ai_chatbot_core.types import  Model, Message


class TestChatSync(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_api_key"
        self.chat = Chat(self.api_key)

    def test_remove_think_content(self):
        text_with_think = "This is some text <think>This is a thought</think> and more text."
        text_without_think = remove_think_content(text_with_think)
        self.assertEqual(text_without_think, "This is some text  and more text.")

        text_with_think_multiline = "This is some text <think>\nThis is a thought\n</think> and more text."
        text_without_think_multiline = remove_think_content(text_with_think_multiline)
        self.assertEqual(text_without_think_multiline, "This is some text  and more text.")

        text_without_think_tag = "This is some text and more text."
        text_without_think_tag_result = remove_think_content(text_without_think_tag)
        self.assertEqual(text_without_think_tag_result, "This is some text and more text.")

    def test_chat_initialization(self):
        chat = Chat(self.api_key, user_id=123, start_message="Custom start message", model=Model.QWEN_QWQ_32B)
        self.assertEqual(chat.api_key, self.api_key)
        self.assertEqual(chat.user_id, 123)
        self.assertEqual(chat.model, Model.QWEN_QWQ_32B)
        self.assertEqual(len(chat.messages), 1)
        self.assertEqual(chat.messages[0].content, "Custom start message")
        self.assertEqual(chat.messages[0].role, "system")

    def test_eq_chat(self):
        chat1 = Chat(self.api_key, user_id=123)
        chat2 = Chat(self.api_key, user_id=123)
        chat3 = Chat(self.api_key, user_id=456)
        self.assertEqual(chat1, chat2)
        self.assertNotEqual(chat1, chat3)

    def test_eq_int(self):
        chat1 = Chat(self.api_key, user_id=123)
        self.assertEqual(chat1, 123)
        self.assertNotEqual(chat1, 456)

    def test_eq_not_implemented(self):
        chat1 = Chat(self.api_key, user_id=123)
        self.assertEqual(chat1.__eq__("string"), NotImplemented)
    
class TestChatAsync(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.api_key = "test_api_key"
        self.chat = Chat(self.api_key)

    async def test_add_message(self):
        chat = Chat("test_api_key")
        await chat.add_message("user", "Test message")
        self.assertEqual(len(chat.messages), 2)
        self.assertIsInstance(chat.messages[1], Message)
        self.assertEqual(chat.messages[1].content, "Test message")
        self.assertEqual(chat.messages[1].role, "user")

    async def test_get_messages(self):
        chat = Chat("test_api_key")
        await chat.add_message("user", "Test message")
        messages = await chat.get_messages()
        self.assertEqual(len(messages), 2)
        self.assertEqual(messages[0]["role"], "system")
        self.assertEqual(messages[1]["role"], "user")
        self.assertEqual(messages[1]["content"], "Test message")
    
    @patch('aiohttp.ClientSession.post')
    async def test_get_response_success(self, mock_post):
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json.return_value = {"choices": [{"message": {"role": "assistant", "content": "This is a test response."}}]}
        mock_post.return_value.__aenter__.return_value = mock_response
        
        response = await self.chat.get_response("Test question")
        self.assertEqual(response, "This is a test response.")
        self.assertEqual(len(self.chat.messages), 3)
        
    @patch('aiohttp.ClientSession.post')
    async def test_get_response_error(self, mock_post):
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text.return_value = "Internal Server Error"
        mock_post.return_value.__aenter__.return_value = mock_response

        response = await self.chat.get_response("Test question")
        self.assertEqual(response, "An error occurred while processing your request.")
