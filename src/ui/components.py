import streamlit as st


def render_document_card(
    document_name: str | None,
    document_info: dict | None,
) -> None:
    """
    Render the currently loaded document in the sidebar.
    """

    st.markdown("### 📄 Document")

    if not document_name:
        st.caption("No document uploaded.")
        return

    characters = 0
    chunks = 0

    if document_info:
        characters = document_info.get("characters", 0)
        chunks = document_info.get("chunks", 0)

    st.html(
        f"""
        <div class="nm-sidebar-document">

            <div class="nm-sidebar-document-name">
                📄 {document_name}
            </div>

            <div class="nm-sidebar-document-meta">
                {characters:,} characters&nbsp;&nbsp;•&nbsp;&nbsp;
                {chunks} chunks
            </div>

        </div>
        """
    )


def render_empty_state() -> None:
    """
    Render the initial NeMoDoc welcome screen.
    """

    st.html(
        """
        <div class="nm-empty">

            <div class="nm-empty-icon">
                📄
            </div>

            <div class="nm-empty-title">
                Ask your documents anything
            </div>

            <div class="nm-empty-subtitle">
                Upload a PDF and have a grounded conversation
                with its contents using NeMoDoc and NVIDIA Nemotron.
            </div>

        </div>
        """
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.html(
            """
            <div class="nm-suggestion">

                <div class="nm-suggestion-icon">
                    📚
                </div>

                <strong>
                    Understand
                </strong>

                <span>
                    Ask questions about your document.
                </span>

            </div>
            """
        )

    with col2:
        st.html(
            """
            <div class="nm-suggestion">

                <div class="nm-suggestion-icon">
                    🔎
                </div>

                <strong>
                    Retrieve
                </strong>

                <span>
                    Find relevant information instantly.
                </span>

            </div>
            """
        )

    with col3:
        st.html(
            """
            <div class="nm-suggestion">

                <div class="nm-suggestion-icon">
                    🤖
                </div>

                <strong>
                    Ask Nemotron
                </strong>

                <span>
                    Generate answers grounded in your documents.
                </span>

            </div>
            """
        )


def render_document_header(
    document_name: str | None,
    document_info: dict | None,
) -> None:
    """
    Render the active document header above the conversation.
    """

    if not document_name:
        return

    characters = 0
    chunks = 0

    if document_info:
        characters = document_info.get("characters", 0)
        chunks = document_info.get("chunks", 0)

    st.html(
        f"""
        <div class="nm-document-header">

            <div class="nm-document-main">

                <div class="nm-document-title">
                    📄 {document_name}
                </div>

                <div class="nm-document-meta">
                    {characters:,} characters&nbsp;&nbsp;•&nbsp;&nbsp;
                    {chunks} chunks
                </div>

            </div>

            <div class="nm-status">
                <span class="nm-status-dot"></span>
                Ready
            </div>

        </div>
        """
    )


def render_message_sources(
    sources: list[dict],
) -> None:
    """
    Render retrieved document chunks as compact source cards.
    """

    if not sources:
        return

    st.html(
        f"""
        <div class="nm-sources">

            <div class="nm-sources-title">
                🔎 Sources · {len(sources)}
            </div>

        </div>
        """
    )

    for index, result in enumerate(
        sources,
        start=1,
    ):

        score = float(
            result.get("score", 0.0)
        )

        chunk = str(
            result.get("chunk", "")
        )

        document_id = result.get(
            "document_id"
        )

        if document_id:
            source_label = (
                f"Document · "
                f"{str(document_id)[:10]}..."
            )
        else:
            source_label = f"Source {index}"

        preview = chunk.strip()

        if len(preview) > 280:
            preview = (
                preview[:280].rstrip()
                + "..."
            )

        st.html(
            f"""
            <div class="nm-source-card">

                <div class="nm-source-header">

                    <div class="nm-source-name">
                        📄 {source_label}
                    </div>

                    <div class="nm-source-score">
                        Similarity {score:.4f}
                    </div>

                </div>

                <div class="nm-source-text">
                    {preview}
                </div>

            </div>
            """
        )


def render_message(
    role: str,
    content: str,
    sources: list[dict] | None = None,
) -> None:
    """
    Render a single conversation message.
    """

    if role == "user":

        with st.chat_message(
            "user",
            avatar="👤",
        ):
            st.markdown(content)

    else:

        with st.chat_message(
            "assistant",
            avatar="🤖",
        ):

            st.markdown(content)

            if sources:
                render_message_sources(
                    sources
                )