# ai_chatbot_core

**Version:** 0.2.1

## Project Overview

`ai_chatbot_core` is a Python library designed to provide the foundational components for building AI-powered chatbot applications. It offers a flexible and extensible framework for managing chat sessions, handling user interactions, and integrating with various language models. This library abstracts away the complexities of managing chat states and interactions, allowing developers to focus on creating unique and engaging chatbot experiences.

**Key Features:**

*   **Chat Management:** Efficiently manage multiple chat sessions with different users.
*   **Model Agnostic:** Designed to be compatible with various language models, allowing for easy integration and switching.
*   **Customizable:** Highly configurable to adapt to different chatbot use cases and requirements.
*   **Asynchronous:** Built with asynchronous programming in mind, ensuring high performance and responsiveness.
*   **Extensible:** Easy to extend with custom message types, models, and other features.

**Key Technologies:**

*   **Python:** The core programming language.
*   **Asyncio:** For asynchronous programming and handling concurrent chat sessions.
*   **Pydantic:** For data validation and settings management.

## Installation Instructions

### Prerequisites

*   **Python 3.9+:** `ai_chatbot_core` requires Python 3.9 or higher.
*   **pip:** The Python package installer.

### Installation Steps

1.  **Create a Virtual Environment (Recommended):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate  # On Windows
    ```

2.  **Install `ai_chatbot_core`:**

    ```bash
    pip install ai_chatbot_core
    ```

### Platform-Specific Instructions

*   **Windows:** Follow the standard installation steps above. Ensure that Python is added to your system's PATH environment variable.
*   **macOS:** Follow the standard installation steps. Python 3 is typically pre-installed on macOS.
*   **Linux:** Follow the standard installation steps. You may need to use `python3` and `pip3` if you have both Python 2 and 3 installed.

## Usage Guide

After installing `ai_chatbot_core`, you can start building your chatbot application by importing the necessary classes and functions.

### API key
https://io.net

### Basic Usage

Here's a simple example of how to use `ai_chatbot_core` to manage a chat session:

```python
import asyncio
from ai_chatbot_core.chat_maneger import ManegerChat
from ai_chatbot_core.types import Model

async def main():
    # Initialize the chat manager with your API key
    manager = ManegerChat(api_key="YOUR_API_KEY", model=Model.DEEPSEEK_R1, start_message="Hello, I'm your assistant.")

    # Connect to a chat session for a user (creates a new one if it doesn't exist)
    user_id = 123
    chat = await manager.connect_chat(user_id)

    # Get the chat instance
    chat = await manager.get_chat(user_id)
    print(f"Chat for user {user_id}: {chat}")
    # Get response 
    response = await chat.response('Hi chat')
    print(response)


    # Remove the chat session
    await manager.remove_chat(user_id)

if __name__ == "__main__":
    asyncio.run(main())
