import re

import streamlit as st

from src.chat.manager import ChatManager

from src.llm import (
    ask_nemotron,
    summarize_document,
    analyze_document,
    generate_executive_summary,
)

from src.ui.components import (
    render_message,
    render_message_sources,
)


# ============================================================
# CLEAN MODEL OUTPUT
# ============================================================

def clean_model_output(
    answer: str,
) -> str:
    """
    Remove UI/navigation artifacts occasionally produced
    by the model or Markdown rendering.

    Keeps the actual generated content unchanged.
    """

    if not answer:
        return answer

    # --------------------------------------------------------
    # Remove localhost SVG/navigation artifacts.
    # --------------------------------------------------------

    answer = re.sub(
        r"\[svg\]\(https?://localhost:[0-9]+/#[^)]+\)",
        "",
        answer,
        flags=re.IGNORECASE,
    )

    # --------------------------------------------------------
    # Remove localhost links that may appear as
    # generated navigation artifacts.
    # --------------------------------------------------------

    answer = re.sub(
        r"\[[^\]]*\]\(https?://localhost:[0-9]+/#[^)]+\)",
        "",
        answer,
        flags=re.IGNORECASE,
    )

    # --------------------------------------------------------
    # Remove excessive blank lines.
    # --------------------------------------------------------

    answer = re.sub(
        r"\n{3,}",
        "\n\n",
        answer,
    )

    return answer.strip()


# ============================================================
# CHAT HISTORY
# ============================================================

def render_chat_history(
    chat_manager: ChatManager,
) -> None:
    """
    Render all messages from the active chat.
    """

    chat = chat_manager.get_active_chat()

    if chat is None:
        return

    for message in chat.messages:

        render_message(
            role=message.role,
            content=message.content,
            sources=message.sources,
        )


# ============================================================
# LLM CHAT HISTORY
# ============================================================

def build_chat_history(
    chat_manager: ChatManager,
) -> list[dict]:
    """
    Convert the active chat into the message format
    expected by the LLM.
    """

    history = (
        chat_manager.get_active_history()
    )

    if history is None:
        return []

    return history.get_llm_history()


# ============================================================
# NORMAL RAG RETRIEVAL
# ============================================================

def retrieve_context(
    question: str,
    retrievers: dict[str, object],
    top_k: int = 3,
) -> tuple[str, list[dict]]:
    """
    Retrieve the most relevant chunks for normal
    question answering.
    """

    all_results = []

    if not retrievers:
        return "", []

    # --------------------------------------------------------
    # Search every attached document.
    # --------------------------------------------------------

    for document_id, retriever in (
        retrievers.items()
    ):

        results = retriever.retrieve(
            question,
            top_k=top_k,
        )

        for result in results:

            all_results.append(
                {
                    **result,
                    "document_id": document_id,
                }
            )

    # --------------------------------------------------------
    # Strongest matches first.
    # --------------------------------------------------------

    all_results.sort(
        key=lambda result: result["score"],
        reverse=True,
    )

    # --------------------------------------------------------
    # Keep strongest results across all documents.
    # --------------------------------------------------------

    all_results = all_results[:8]

    # --------------------------------------------------------
    # Build context.
    # --------------------------------------------------------

    context_parts = []

    for result in all_results:

        context_parts.append(
            result["chunk"]
        )

    context = "\n\n".join(
        context_parts
    )

    return context, all_results


# ============================================================
# DOCUMENT-WIDE CONTEXT
# ============================================================

def build_document_wide_context(
    retrievers: dict[str, object],
    chunks_per_document: int = 10,
    max_chars_per_document: int = 7500,
) -> tuple[str, list[dict]]:
    """
    Build broad document context for summarization,
    document analysis, and executive summaries.

    Samples chunks across each document so the LLM gets
    information from the beginning, middle, and end.

    The context is deliberately limited so the model has
    enough generation capacity to complete its response.
    """

    context_parts = []
    sources = []

    if not retrievers:
        return "", []

    # --------------------------------------------------------
    # Process each attached document independently.
    # --------------------------------------------------------

    for document_id, retriever in (
        retrievers.items()
    ):

        try:

            chunks = (
                retriever.vector_store.chunks
            )

        except AttributeError:

            chunks = []

        if not chunks:
            continue

        total_chunks = len(
            chunks
        )

        # ----------------------------------------------------
        # Determine how many chunks to sample.
        # ----------------------------------------------------

        sample_count = min(
            chunks_per_document,
            total_chunks,
        )

        # ----------------------------------------------------
        # Select evenly distributed chunks.
        #
        # This gives coverage from the beginning,
        # middle, and end of the document.
        # ----------------------------------------------------

        if sample_count == 1:

            indexes = [0]

        else:

            indexes = [

                round(
                    i
                    * (total_chunks - 1)
                    / (sample_count - 1)
                )

                for i in range(
                    sample_count
                )

            ]

        # ----------------------------------------------------
        # Remove duplicate indexes.
        # ----------------------------------------------------

        indexes = list(
            dict.fromkeys(
                indexes
            )
        )

        document_context_parts = []

        document_characters = 0

        # ----------------------------------------------------
        # Collect sampled chunks.
        # ----------------------------------------------------

        for index in indexes:

            chunk = str(
                chunks[index]
            ).strip()

            if not chunk:
                continue

            remaining = (
                max_chars_per_document
                - document_characters
            )

            if remaining <= 0:
                break

            if len(chunk) > remaining:

                chunk = chunk[
                    :remaining
                ]

            document_context_parts.append(

                f"[Document {document_id[:10]}... | "
                f"Chunk {index + 1}/{total_chunks}]\n"
                f"{chunk}"

            )

            document_characters += len(
                chunk
            )

            sources.append(
                {
                    "document_id": document_id,
                    "chunk": chunk,
                    "score": 0.0,
                    "coverage": True,
                }
            )

        # ----------------------------------------------------
        # Add this document's sampled context.
        # ----------------------------------------------------

        if document_context_parts:

            context_parts.append(
                "\n\n".join(
                    document_context_parts
                )
            )

    # --------------------------------------------------------
    # Combine documents.
    # --------------------------------------------------------

    context = "\n\n".join(
        context_parts
    )

    return context, sources


# ============================================================
# SAVE GENERATED RESPONSE
# ============================================================

def save_response(
    chat_manager: ChatManager,
    user_prompt: str,
    answer: str,
    sources: list[dict],
) -> None:
    """
    Save an interaction to the active conversation.
    """

    history = (
        chat_manager.get_active_history()
    )

    if history is None:
        return

    # --------------------------------------------------------
    # Clean before saving so navigation artifacts never
    # become part of the conversation memory.
    # --------------------------------------------------------

    answer = clean_model_output(
        answer
    )

    history.add_user_message(
        user_prompt
    )

    history.add_assistant_message(
        content=answer,
        sources=sources,
    )


# ============================================================
# DISPLAY RESPONSE
# ============================================================

def display_response(
    answer: str,
    sources: list[dict],
) -> None:
    """
    Display an assistant response and its sources.
    """

    # --------------------------------------------------------
    # Clean before rendering.
    # --------------------------------------------------------

    answer = clean_model_output(
        answer
    )

    with st.chat_message(
        "assistant",
        avatar="🤖",
    ):

        st.markdown(
            answer
        )

        if sources:

            render_message_sources(
                sources
            )


# ============================================================
# DOCUMENT ACTION
# ============================================================

def run_document_action(
    action: str,
    chat_manager: ChatManager,
    retrievers: dict[str, object],
) -> None:
    """
    Execute a document-intelligence action.

    Supported actions:

        summarize
        analyze
        executive

    Each action uses its dedicated LLM function and
    centralized prompt from src.llm.llm / prompts.py.
    """

    if not retrievers:

        st.warning(
            "No documents are attached to this chat."
        )

        return

    # ========================================================
    # DOCUMENT-WIDE CONTEXT
    # ========================================================

    with st.spinner(
        "Reviewing the document..."
    ):

        context, sources = (
            build_document_wide_context(
                retrievers=retrievers,
                chunks_per_document=10,
                max_chars_per_document=7500,
            )
        )

    if not context:

        st.warning(
            "No document content was available "
            "for this operation."
        )

        return

    # ========================================================
    # SUMMARIZE
    # ========================================================

    if action == "summarize":

        user_prompt = (
            "Summarize the uploaded document "
            "comprehensively."
        )

        with st.spinner(
            "Creating document summary..."
        ):

            answer = summarize_document(
                context
            )

    # ========================================================
    # ANALYZE
    # ========================================================

    elif action == "analyze":

        user_prompt = (
            "Analyze the uploaded document."
        )

        with st.spinner(
            "Analyzing the document..."
        ):

            answer = analyze_document(
                context
            )

    # ========================================================
    # EXECUTIVE SUMMARY
    # ========================================================

    elif action == "executive":

        user_prompt = (
            "Generate an executive summary "
            "of the uploaded document."
        )

        with st.spinner(
            "Creating executive summary..."
        ):

            answer = (
                generate_executive_summary(
                    context
                )
            )

    else:

        return

    # ========================================================
    # CLEAN OUTPUT
    # ========================================================

    answer = clean_model_output(
        answer
    )

    # ========================================================
    # SAVE
    # ========================================================

    save_response(
        chat_manager=chat_manager,
        user_prompt=user_prompt,
        answer=answer,
        sources=sources,
    )

    # ========================================================
    # DISPLAY
    # ========================================================

    display_response(
        answer=answer,
        sources=sources,
    )


# ============================================================
# DOCUMENT ACTION BAR
# ============================================================

def render_document_actions(
    chat_manager: ChatManager,
    retrievers: dict[str, object],
) -> None:
    """
    Render the document-intelligence action bar in normal
    document flow so it never overlaps generated answers.

    Nothing runs automatically. The user must explicitly
    choose an action.
    """

    st.markdown(
        "### What would you like to do?"
    )

    st.caption(
        "Choose an action or ask a question below."
    )

    col1, col2, col3 = st.columns(
        3,
        gap="small",
    )

    with col1:
        summarize_clicked = st.button(
            "📄  Summarize",
            use_container_width=True,
            key="action_summarize",
        )

    with col2:
        analyze_clicked = st.button(
            "🔎  Analyze",
            use_container_width=True,
            key="action_analyze",
        )

    with col3:
        executive_clicked = st.button(
            "📋  Executive Summary",
            use_container_width=True,
            key="action_executive",
        )

    if summarize_clicked:
        try:
            run_document_action(
                action="summarize",
                chat_manager=chat_manager,
                retrievers=retrievers,
            )
        except Exception as error:
            st.error(
                f"Summarization failed: {error}"
            )

    elif analyze_clicked:
        try:
            run_document_action(
                action="analyze",
                chat_manager=chat_manager,
                retrievers=retrievers,
            )
        except Exception as error:
            st.error(
                f"Document analysis failed: {error}"
            )

    elif executive_clicked:
        try:
            run_document_action(
                action="executive",
                chat_manager=chat_manager,
                retrievers=retrievers,
            )
        except Exception as error:
            st.error(
                f"Executive summary failed: {error}"
            )


# ============================================================
# CHAT INPUT
# ============================================================

def render_chat_input(
    chat_manager: ChatManager,
    retrievers: dict[str, object],
) -> None:
    """
    Render the document action bar and normal
    chat input.

    Actions are completely manual.

    Nothing happens just because a PDF was uploaded.
    """

    render_document_actions(
        chat_manager=chat_manager,
        retrievers=retrievers,
    )

    # ========================================================
    # NORMAL QUESTION INPUT
    # ========================================================

    question = st.chat_input(
        "Ask anything about your documents..."
    )

    if not question:
        return

    question = question.strip()

    if not question:
        return

    history = (
        chat_manager.get_active_history()
    )

    if history is None:

        st.error(
            "No active conversation is available."
        )

        return

    # ========================================================
    # DISPLAY USER QUESTION
    # ========================================================

    with st.chat_message(
        "user",
        avatar="👤",
    ):

        st.markdown(
            question
        )

    try:

        # ====================================================
        # NORMAL RAG RETRIEVAL
        # ====================================================

        if not retrievers:

            st.warning(
                "No documents are attached to this chat."
            )

            return

        with st.spinner(
            "Searching your documents..."
        ):

            context, all_results = (
                retrieve_context(
                    question=question,
                    retrievers=retrievers,
                    top_k=3,
                )
            )

        if not context:

            st.warning(
                "No relevant information was found "
                "in the attached documents."
            )

            return

        # ====================================================
        # CONVERSATION HISTORY
        # ====================================================

        chat_history = (
            history.get_llm_history()
        )

        # ====================================================
        # GENERATE ANSWER
        #
        # Normal Q&A still goes through ask_nemotron()
        # because this path requires conversation memory.
        # ====================================================

        with st.spinner(
            "Thinking..."
        ):

            answer = ask_nemotron(
                question=question,
                context=context,
                chat_history=chat_history,
            )

        # ====================================================
        # CLEAN GENERATED OUTPUT
        # ====================================================

        answer = clean_model_output(
            answer
        )

        # ====================================================
        # SAVE USER MESSAGE
        # ====================================================

        history.add_user_message(
            question
        )

        # ====================================================
        # SAVE ASSISTANT MESSAGE
        # ====================================================

        history.add_assistant_message(
            content=answer,
            sources=all_results,
        )

        # ====================================================
        # DISPLAY RESPONSE
        # ====================================================

        display_response(
            answer=answer,
            sources=all_results,
        )

    except Exception as error:

        st.error(
            f"An error occurred: {error}"
        )