from .models import Chat, Message


class ChatHistory:
    """
    Manages the messages belonging to a single chat.

    This class keeps conversation logic separate from
    the Streamlit UI so it can later be reused by
    persistent storage and multi-chat functionality.
    """

    def __init__(self, chat: Chat):
        self.chat = chat

    def add_user_message(
        self,
        content: str
    ) -> Message:
        """
        Add a user message to the conversation.
        """

        message = Message(
            role="user",
            content=content,
        )

        self.chat.add_message(message)

        return message

    def add_assistant_message(
        self,
        content: str,
        sources: list[dict] | None = None,
    ) -> Message:
        """
        Add an assistant message to the conversation.

        Retrieved document chunks can be stored alongside
        the assistant response for source inspection.
        """

        message = Message(
            role="assistant",
            content=content,
            sources=sources or [],
        )

        self.chat.add_message(message)

        return message

    def get_messages(self) -> list[Message]:
        """
        Return all messages in the conversation.
        """

        return self.chat.messages

    def get_llm_history(self) -> list[dict]:
        """
        Return conversation history in the format
        expected by the LLM API.
        """

        history = []

        for message in self.chat.messages:

            history.append(
                {
                    "role": message.role,
                    "content": message.content,
                }
            )

        return history

    def clear(self) -> None:
        """
        Clear all messages from the conversation.
        """

        self.chat.clear_messages()

    def __len__(self) -> int:
        """
        Return the number of messages in the conversation.
        """

        return len(self.chat.messages)