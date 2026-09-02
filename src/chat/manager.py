from uuid import uuid4

from .models import Chat
from .history import ChatHistory


class ChatManager:
    """
    Manages multiple Enterprise Document Intelligence System conversations.

    The manager is intentionally independent of Streamlit
    so it can later be connected to persistent storage.
    """

    def __init__(self):
        self.chats: dict[str, Chat] = {}
        self.active_chat_id: str | None = None

    # ========================================================
    # CHAT CREATION
    # ========================================================

    def create_chat(
        self,
        title: str = "New Chat"
    ) -> Chat:
        """
        Create a new chat and make it active.
        """

        chat_id = str(uuid4())

        chat = Chat(
            chat_id=chat_id,
            title=title,
        )

        self.chats[chat_id] = chat

        self.active_chat_id = chat_id

        return chat

    # ========================================================
    # CHAT RETRIEVAL
    # ========================================================

    def get_chat(
        self,
        chat_id: str
    ) -> Chat | None:
        """
        Return a chat by its ID.
        """

        return self.chats.get(chat_id)

    def get_active_chat(self) -> Chat | None:
        """
        Return the currently active chat.
        """

        if self.active_chat_id is None:
            return None

        return self.chats.get(
            self.active_chat_id
        )

    def get_active_history(
        self
    ) -> ChatHistory | None:
        """
        Return a ChatHistory object for the
        currently active conversation.
        """

        chat = self.get_active_chat()

        if chat is None:
            return None

        return ChatHistory(chat)

    # ========================================================
    # CHAT SWITCHING
    # ========================================================

    def switch_chat(
        self,
        chat_id: str
    ) -> bool:
        """
        Make an existing chat active.

        Returns:
            True if the chat exists and was switched to.
            False otherwise.
        """

        if chat_id not in self.chats:
            return False

        self.active_chat_id = chat_id

        return True

    # ========================================================
    # CHAT DELETION
    # ========================================================

    def delete_chat(
        self,
        chat_id: str
    ) -> bool:
        """
        Delete a chat.

        If the deleted chat was active, another available
        chat becomes active automatically.
        """

        if chat_id not in self.chats:
            return False

        del self.chats[chat_id]

        # ----------------------------------------------------
        # If the active chat was deleted, select another chat.
        # ----------------------------------------------------

        if self.active_chat_id == chat_id:

            if self.chats:

                self.active_chat_id = next(
                    iter(self.chats)
                )

            else:

                self.active_chat_id = None

        return True

    # ========================================================
    # CHAT CLEARING
    # ========================================================

    def clear_active_chat(self) -> bool:
        """
        Remove all messages from the active chat.
        """

        history = self.get_active_history()

        if history is None:
            return False

        history.clear()

        return True

    # ========================================================
    # CHAT LIST
    # ========================================================

    def list_chats(self) -> list[Chat]:
        """
        Return all chats.

        Chats are returned from newest activity to oldest.
        """

        return sorted(
            self.chats.values(),
            key=lambda chat: chat.updated_at,
            reverse=True,
        )

    # ========================================================
    # UTILITY
    # ========================================================

    def ensure_chat(self) -> Chat:
        """
        Return the active chat.

        If no chat exists, automatically create one.
        """

        chat = self.get_active_chat()

        if chat is not None:
            return chat

        return self.create_chat()

    def __len__(self) -> int:
        """
        Return the number of chats.
        """

        return len(self.chats)
