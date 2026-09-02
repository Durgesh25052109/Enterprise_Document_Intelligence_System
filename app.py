from pathlib import Path

import streamlit as st

from src.chat.manager import ChatManager
from src.documents.manager import DocumentManager

from src.ui.styles import apply_document_intelligence_styles
from src.ui.sidebar import render_sidebar

from src.ui.chat import (
    render_chat_history,
    render_chat_input,
)

from src.ui.components import (
    render_empty_state,
    render_document_header,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Enterprise Document Intelligence System",
    page_icon="📄",
    layout="wide",
)


# ============================================================
# GLOBAL STYLING
# ============================================================

apply_document_intelligence_styles()


# ============================================================
# SESSION STATE
# ============================================================

if "chat_manager" not in st.session_state:

    st.session_state.chat_manager = (
        ChatManager()
    )


if "document_manager" not in st.session_state:

    st.session_state.document_manager = (
        DocumentManager()
    )


# ============================================================
# MANAGERS
# ============================================================

chat_manager = (
    st.session_state.chat_manager
)

document_manager = (
    st.session_state.document_manager
)


# ============================================================
# CHAT INITIALIZATION
# ============================================================

chat_manager.ensure_chat()

active_chat = (
    chat_manager.get_active_chat()
)


# ============================================================
# CURRENT DOCUMENTS
# ============================================================

current_documents = []

current_retrievers = {}


if active_chat is not None:

    for document_id in (
        active_chat.document_ids
    ):

        document = (
            document_manager.get_document(
                document_id
            )
        )

        retriever = (
            document_manager.get_retriever(
                document_id
            )
        )

        if document is not None:

            current_documents.append(
                document
            )

        if retriever is not None:

            current_retrievers[
                document_id
            ] = retriever


# ============================================================
# SIDEBAR DOCUMENT INFORMATION
# ============================================================

current_document_name = None

current_document_info = None


if current_documents:

    first_document = (
        current_documents[0]
    )

    current_document_name = (
        first_document.filename
    )

    current_document_info = {

        "characters": (
            first_document.characters
        ),

        "chunks": (
            first_document.chunks
        ),

    }


# ============================================================
# SIDEBAR
# ============================================================

render_sidebar(
    chat_manager=chat_manager,
    document_name=current_document_name,
    document_info=current_document_info,
)


# ============================================================
# MAIN HEADER
# ============================================================

st.title(
    "💬 Enterprise Document Intelligence System"
)

st.caption(
    "Conversational Document Intelligence powered by "
    "Retrieval-Augmented Generation and NVIDIA Nemotron."
)


# ============================================================
# DOCUMENT SECTION
# ============================================================

st.subheader(
    "📄 Documents"
)


if current_documents:

    for document in current_documents:

        render_document_header(
            document_name=document.filename,
            document_info={
                "characters": (
                    document.characters
                ),
                "chunks": (
                    document.chunks
                ),
            },
        )

else:

    st.caption(
        "No documents are attached to this chat."
    )


# ============================================================
# PDF UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"],
    key=(
        f"pdf_uploader_"
        f"{active_chat.chat_id}"
    ),
    help=(
        "Upload a PDF to add it "
        "to this conversation."
    ),
)


# ============================================================
# PROCESS DOCUMENT
# ============================================================

if uploaded_file is not None:

    file_bytes = (
        uploaded_file.getvalue()
    )

    # --------------------------------------------------------
    # Upload directory
    # --------------------------------------------------------

    upload_directory = Path(
        "data/uploads"
    )

    upload_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    # --------------------------------------------------------
    # Save PDF
    # --------------------------------------------------------

    pdf_path = (
        upload_directory
        / uploaded_file.name
    )

    with open(
        pdf_path,
        "wb",
    ) as file:

        file.write(
            file_bytes
        )

    # --------------------------------------------------------
    # Generate document ID
    # --------------------------------------------------------

    document_id = (
        document_manager.generate_document_id(
            file_bytes
        )
    )

    # --------------------------------------------------------
    # Check whether already attached
    # --------------------------------------------------------

    already_attached = (
        document_id
        in active_chat.document_ids
    )

    # ========================================================
    # PROCESS NEW DOCUMENT
    # ========================================================

    if not already_attached:

        try:

            with st.spinner(
                "Processing document..."
            ):

                document = (
                    document_manager.add_document(
                        file_path=str(
                            pdf_path
                        ),
                        file_bytes=file_bytes,
                    )
                )

            # ------------------------------------------------
            # Attach to current conversation
            # ------------------------------------------------

            active_chat.document_ids.append(
                document.document_id
            )

            # ------------------------------------------------
            # IMPORTANT:
            #
            # Uploading a PDF does NOT automatically
            # summarize, analyze, or generate an
            # executive summary.
            #
            # The user chooses the action manually.
            # ------------------------------------------------

            st.success(
                f"Added **{document.filename}** "
                "to this conversation."
            )

            st.rerun()

        except Exception as error:

            st.error(
                "Failed to process the document: "
                f"{error}"
            )

            st.stop()


# ============================================================
# MAIN DOCUMENT STATE
# ============================================================

if not current_retrievers:

    render_empty_state()


else:

    # ========================================================
    # REFRESH ACTIVE CHAT
    # ========================================================

    active_chat = (
        chat_manager.get_active_chat()
    )

    if active_chat is None:

        active_chat = (
            chat_manager.create_chat()
        )


    # ========================================================
    # CHAT TITLE
    # ========================================================

    if (
        active_chat.title == "New Chat"
        and active_chat.messages
    ):

        first_user_message = next(
            (
                message
                for message
                in active_chat.messages
                if message.role == "user"
            ),
            None,
        )

        if first_user_message:

            title = (
                first_user_message.content
            )

            if len(title) > 40:

                title = (
                    title[:40]
                    + "..."
                )

            active_chat.title = title


    # ========================================================
    # CHAT HEADER
    # ========================================================

    st.divider()

    st.subheader(
        active_chat.title
    )


    # ========================================================
    # CHAT HISTORY
    # ========================================================

    render_chat_history(
        chat_manager
    )


    # ========================================================
    # CHAT INPUT + DOCUMENT ACTIONS
    # ========================================================
    #
    # chat.py renders:
    #
    #   📄 Summarize
    #   🔎 Analyze
    #   📋 Executive Summary
    #
    # followed by the normal chat input.
    #
    # The action-button row stays in normal document flow
    # so generated answers are never covered by it.
    # ========================================================

    render_chat_input(
        chat_manager=chat_manager,
        retrievers=current_retrievers,
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Enterprise Document Intelligence System v1.0 • "
    "Multi-Document Conversational Intelligence"
)
