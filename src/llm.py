import os

import requests
from dotenv import load_dotenv

from .prompts import (
    build_analysis_prompt,
    build_executive_summary_prompt,
    build_rag_system_prompt,
    build_summary_prompt,
)


load_dotenv()


API_KEY = os.getenv("NVIDIA_API_KEY")
BASE_URL = os.getenv("NVIDIA_BASE_URL")
MODEL = os.getenv("NVIDIA_MODEL")


def _call_nemotron(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 800,
    temperature: float = 0.2,
) -> str:
    """
    Send a generic request to NVIDIA Nemotron.

    This helper is shared by all NeMoDoc capabilities.
    """

    if not API_KEY:
        raise ValueError(
            "NVIDIA_API_KEY is not configured."
        )

    if not BASE_URL:
        raise ValueError(
            "NVIDIA_BASE_URL is not configured."
        )

    if not MODEL:
        raise ValueError(
            "NVIDIA_MODEL is not configured."
        )

    url = f"{BASE_URL}/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=180,
    )

    response.raise_for_status()

    result = response.json()

    choice = result["choices"][0]
    finish_reason = choice.get("finish_reason")

    if finish_reason == "length":
        print(
            "\nWARNING: Nemotron stopped because the output token limit "
            "was reached (max_tokens=3000)."
        )

    return choice["message"]["content"]


# ============================================================
# RAG QUESTION ANSWERING
# ============================================================


def ask_nemotron(
    question: str,
    context: str,
    chat_history: list[dict] | None = None,
) -> str:
    """
    Answer a user's question using retrieved document
    context and previous conversation history.

    This is the primary RAG question-answering function.
    """

    system_message = build_rag_system_prompt(
        context
    )

    messages = [
        {
            "role": "system",
            "content": system_message,
        }
    ]

    # --------------------------------------------------------
    # Previous conversation
    # --------------------------------------------------------

    if chat_history:

        for message in chat_history:

            role = message.get("role")
            content = message.get("content")

            if (
                role in ["user", "assistant"]
                and content
            ):

                messages.append(
                    {
                        "role": role,
                        "content": content,
                    }
                )

    # --------------------------------------------------------
    # Current question
    # --------------------------------------------------------

    messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    # --------------------------------------------------------
    # API validation
    # --------------------------------------------------------

    if not API_KEY:
        raise ValueError(
            "NVIDIA_API_KEY is not configured."
        )

    if not BASE_URL:
        raise ValueError(
            "NVIDIA_BASE_URL is not configured."
        )

    if not MODEL:
        raise ValueError(
            "NVIDIA_MODEL is not configured."
        )

    url = f"{BASE_URL}/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 3000,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=180,
    )

    response.raise_for_status()

    result = response.json()

    choice = result["choices"][0]
    finish_reason = choice.get("finish_reason")

    if finish_reason == "length":
        print(
            "\nWARNING: Nemotron stopped because the output token limit "
            "was reached (max_tokens=3000)."
        )

    return choice["message"]["content"]


# ============================================================
# DOCUMENT SUMMARIZATION
# ============================================================


def summarize_document(
    context: str,
) -> str:
    """
    Generate a structured summary of a document.

    Uses an explicitly engineered summarization prompt.
    """

    if not context.strip():
        return (
            "No document content is available "
            "for summarization."
        )

    prompt = build_summary_prompt(
        context
    )

    return _call_nemotron(
        system_prompt=(
            "You are NeMoDoc's document "
            "summarization assistant."
        ),
        user_prompt=prompt,
        max_tokens=5000,
        temperature=0.7,
    )


# ============================================================
# DOCUMENT ANALYST
# ============================================================


def analyze_document(
    context: str,
) -> str:
    """
    Perform structured document analysis.

    This represents NeMoDoc's Document Analyst workflow.
    """

    if not context.strip():
        return (
            "No document content is available "
            "for analysis."
        )

    prompt = build_analysis_prompt(
        context
    )

    return _call_nemotron(
        system_prompt=(
            "You are NeMoDoc's Document Analyst. "
            "Analyze documents carefully and provide "
            "structured, evidence-grounded findings."
        ),
        user_prompt=prompt,
        max_tokens=5000,
        temperature=0.7,
    )


# ============================================================
# EXECUTIVE SUMMARY
# ============================================================


def generate_executive_summary(
    context: str,
) -> str:
    """
    Generate a concise executive-level summary.

    This implements the Project 5 bonus capability.
    """

    if not context.strip():
        return (
            "No document content is available "
            "for executive summary generation."
        )

    prompt = build_executive_summary_prompt(
        context
    )

    return _call_nemotron(
        system_prompt=(
            "You are NeMoDoc's executive summary "
            "generation assistant."
        ),
        user_prompt=prompt,
        max_tokens=3000,
        temperature=0.7,
    )


# ============================================================
# STANDALONE TEST
# ============================================================


if __name__ == "__main__":

    test_context = """
    NeMoDoc is an Enterprise Document Intelligence
    System designed to help users interact with PDF
    documents using Retrieval-Augmented Generation.

    The system extracts text from documents, divides
    the text into chunks, creates embeddings, stores
    vectors using FAISS, retrieves relevant information,
    and uses NVIDIA Nemotron to generate responses.

    NeMoDoc supports conversational document
    question answering and independent document
    conversations.
    """

    print("\n--- TEST: QUESTION ANSWERING ---")

    answer = ask_nemotron(
        question="What is NeMoDoc?",
        context=test_context,
    )

    print(answer)

    print("\n--- TEST: DOCUMENT SUMMARY ---")

    summary = summarize_document(
        test_context
    )

    print(summary)

    print("\n--- TEST: DOCUMENT ANALYSIS ---")

    analysis = analyze_document(
        test_context
    )

    print(analysis)

    print("\n--- TEST: EXECUTIVE SUMMARY ---")

    executive_summary = (
        generate_executive_summary(
            test_context
        )
    )

    print(executive_summary)