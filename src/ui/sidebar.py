import streamlit as st

from src.chat.manager import ChatManager
from src.ui.components import render_document_card


def render_sidebar(
    chat_manager: ChatManager,
    document_name: str | None,
    document_info: dict | None,
) -> None:
    """
    Render the Enterprise Document Intelligence System sidebar.
    """

    with st.sidebar:

        # ====================================================
        # BRAND
        # ====================================================

        st.html(
            """
            <div class="nm-brand">

                <div class="nm-brand-title">
                    📄 Enterprise Document Intelligence System
                </div>

                <div class="nm-brand-subtitle">
                    Document Intelligence
                </div>

            </div>
            """
        )

        # ====================================================
        # NEW CHAT
        # ====================================================

        if st.button(
            "＋  New Chat",
            use_container_width=True,
        ):

            chat_manager.create_chat()

            st.rerun()

        st.divider()

        # ====================================================
        # CONVERSATIONS
        # ====================================================

        st.html(
            """
            <div class="nm-sidebar-section-title">
                Conversations
            </div>
            """
        )

        chats = chat_manager.list_chats()

        if not chats:

            st.caption(
                "No conversations yet."
            )

        else:

            for chat in chats:

                is_active = (
                    chat.chat_id
                    == chat_manager.active_chat_id
                )

                title = chat.title

                if (
                    title == "New Chat"
                    and chat.messages
                ):

                    first_user_message = next(
                        (
                            message
                            for message
                            in chat.messages
                            if message.role == "user"
                        ),
                        None,
                    )

                    if first_user_message:

                        title = (
                            first_user_message.content[:32]
                        )

                        if len(title) > 32:
                            title += "..."

                if is_active:
                    button_label = f"●  {title}"
                else:
                    button_label = f"   {title}"

                if st.button(
                    button_label,
                    key=f"chat_{chat.chat_id}",
                    use_container_width=True,
                ):

                    chat_manager.switch_chat(
                        chat.chat_id
                    )

                    st.rerun()

        st.divider()

        # ====================================================
        # CURRENT DOCUMENT
        # ====================================================

        render_document_card(
            document_name=document_name,
            document_info=document_info,
        )

        st.divider()

        # ====================================================
        # CHAT ACTIONS
        # ====================================================

        active_chat = (
            chat_manager.get_active_chat()
        )

        if active_chat is not None:

            if active_chat.messages:

                st.html(
                    """
                    <div class="nm-sidebar-section-title">
                        Chat Actions
                    </div>
                    """
                )

                if st.button(
                    "🗑️  Clear Chat",
                    use_container_width=True,
                ):

                    active_chat.clear_messages()

                    st.rerun()

            if len(chats) > 1:

                if st.button(
                    "🗑️  Delete Chat",
                    use_container_width=True,
                ):

                    chat_manager.delete_chat(
                        active_chat.chat_id
                    )

                    st.rerun()

        # ====================================================
        # FOOTER
        # ====================================================

        st.html(
            """
            <div class="nm-sidebar-footer">

                <div class="nm-sidebar-version">
                    Enterprise Document Intelligence System v1.0
                </div>

                <div class="nm-sidebar-tech">
                    RAG · NVIDIA Nemotron
                </div>

            </div>
            """
        )
