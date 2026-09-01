from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class Message:
    """
    Represents a single message in a NeMoDoc conversation.
    """

    role: str
    content: str
    sources: list[dict[str, Any]] = field(
        default_factory=list
    )
    timestamp: datetime = field(
        default_factory=datetime.now
    )

    def to_dict(self) -> dict:
        """
        Convert the message into a dictionary.

        This makes the message compatible with
        Streamlit session state and future persistence.
        """

        return {
            "role": self.role,
            "content": self.content,
            "sources": self.sources,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class Chat:
    """
    Represents a NeMoDoc conversation.

    A chat can later contain multiple documents,
    persistent history, and cross-chat memory.
    """

    chat_id: str
    title: str = "New Chat"

    created_at: datetime = field(
        default_factory=datetime.now
    )

    updated_at: datetime = field(
        default_factory=datetime.now
    )

    messages: list[Message] = field(
        default_factory=list
    )

    document_ids: list[str] = field(
        default_factory=list
    )

    def add_message(
        self,
        message: Message
    ) -> None:
        """
        Add a message to the conversation.
        """

        self.messages.append(message)

        self.updated_at = datetime.now()

    def clear_messages(self) -> None:
        """
        Remove all messages from the conversation.
        """

        self.messages.clear()

        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """
        Convert the chat into a dictionary.

        This prepares the structure for future
        persistent storage.
        """

        return {
            "chat_id": self.chat_id,
            "title": self.title,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "messages": [
                message.to_dict()
                for message in self.messages
            ],
            "document_ids": self.document_ids,
        }