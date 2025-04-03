import unittest
from ai_chatbot_core.types import Message, StartMessage

class TestTypes(unittest.TestCase):
    def test_message_creation(self):
        message = Message("Hello, world!")
        self.assertEqual(message.content, "Hello, world!")
        self.assertEqual(message.role, "user")

    def test_message_creation_with_role(self):
        message = Message("How are you?", role="assistant")
        self.assertEqual(message.content, "How are you?")
        self.assertEqual(message.role, "assistant")

    def test_message_repr(self):
        message = Message("Test message", role="system")
        expected_repr = {"role": "system", "content": "Test message"}
        self.assertEqual(message.get_content(), expected_repr)

    def test_start_message_creation(self):
        start_message = StartMessage(content=None)
        self.assertEqual(start_message.content, "You are a helpful assistant.")
        self.assertEqual(start_message.role, "system")

    def test_start_message_creation_with_content(self):
        start_message = StartMessage("You are a coding assistant.")
        self.assertEqual(start_message.content, "You are a coding assistant.")
        self.assertEqual(start_message.role, "system")
        
if __name__ == '__main__':
    unittest.main()
