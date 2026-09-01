# NeMoDoc — Enterprise Document Intelligence

> An NVIDIA Nemotron-powered document intelligence system that uses Retrieval-Augmented Generation (RAG) to let users interact with their documents using natural language.

## 🚀 Live Demo

👉 https://nemadoc-ai.streamlit.app/

## 📌 Overview

NeMoDoc is an AI-powered document intelligence application designed to make large documents easier to understand, search, analyze, and interact with.

Users can upload PDF documents and ask questions about their content using natural language. NeMoDoc processes the uploaded documents, retrieves the most relevant information using semantic search, and uses NVIDIA Nemotron to generate grounded responses.

The system supports:

- 📄 Document summarization
- 🔍 Document analysis
- 📝 Executive summaries
- 💬 Conversational question answering
- 📚 Multi-document interaction
- 🔗 Source-aware responses
- 🧠 Semantic document retrieval

Instead of manually searching through hundreds of pages, users can simply ask questions about their documents.

---

# 🧠 Architecture

NeMoDoc follows a Retrieval-Augmented Generation (RAG) architecture.

The system separates document retrieval from AI response generation.

    USER
      │
      ▼
    Streamlit UI
      │
      ├─────────────── Upload PDF
      │                      │
      │                      ▼
      │               Text Extraction
      │                      │
      │                      ▼
      │               Text Cleaning
      │                      │
      │                      ▼
      │               Document Chunking
      │                      │
      │                      ▼
      │               Embedding Generation
      │                      │
      │                      ▼
      │                FAISS Vector Store
      │
      │
      └─────────────── Ask Question
                             │
                             ▼
                      Query Embedding
                             │
                             ▼
                      Similarity Search
                             │
                             ▼
                     Relevant Context
                             │
                             ▼
                    Prompt Construction
                             │
                             ▼
                    NVIDIA Nemotron
                             │
                             ▼
                       AI Response

---

# 🔄 RAG Pipeline

    PDF Document
          │
          ▼
    Text Extraction
          │
          ▼
    Text Cleaning
          │
          ▼
    Document Chunking
          │
          ▼
    Embedding Generation
          │
          ▼
    FAISS Vector Store
          │
          │
          │        User Question
          │              │
          │              ▼
          │        Query Embedding
          │              │
          └──────────────┤
                         ▼
                  Similarity Search
                         │
                         ▼
                  Relevant Chunks
                         │
                         ▼
                  Context + Prompt
                         │
                         ▼
                  NVIDIA Nemotron
                         │
                         ▼
                      Final Answer

### Why RAG?

Large documents can contain hundreds or thousands of pages. Sending an entire document to an LLM for every question is inefficient and can exceed context limits.

NeMoDoc instead:

1. Extracts text from the uploaded document.
2. Cleans and preprocesses the text.
3. Splits the document into smaller chunks.
4. Generates embeddings for the chunks.
5. Stores the embeddings in FAISS.
6. Converts the user's question into an embedding.
7. Retrieves the most relevant document chunks.
8. Constructs a prompt using the retrieved context.
9. Sends the context and question to NVIDIA Nemotron.
10. Generates the final response.

This allows the LLM to focus on the most relevant information instead of processing the entire document every time.

---

# 🤖 NVIDIA Nemotron

NeMoDoc uses NVIDIA Nemotron as its Large Language Model.

The application communicates with the NVIDIA API through an OpenAI-compatible interface.

### Model

nvidia/nemotron-3-super-120b-a12b

Nemotron is responsible for understanding the retrieved context and generating the final response.

The architecture therefore separates the two major responsibilities:

    FAISS
      ↓
    Find relevant information
      ↓
    Relevant Context
      ↓
    NVIDIA Nemotron
      ↓
    Understand + Generate Response

---

# ✨ Features

## 📄 Document Intelligence

- PDF document upload
- Automatic text extraction
- Text cleaning and preprocessing
- Document chunking
- Semantic embeddings
- Vector storage
- Document identification
- Document-level retrieval

## 🔍 Retrieval-Augmented Generation

- Semantic search
- FAISS vector database
- Relevant context retrieval
- Document-grounded question answering
- Context-aware prompt construction
- Source inspection

## 💬 Conversational AI

- Natural-language document chat
- Conversation history
- Multiple conversations
- Chat switching
- Document-aware conversations
- Conversation management

## 📊 Analysis Tools

NeMoDoc provides dedicated workflows for:

- Summarization
- Document Analysis
- Executive Summary
- Question Answering
- Information Extraction
- Multi-document reasoning

## 📚 Multi-Document Support

The system is designed to work with multiple documents while maintaining document-level organization.

Documents can be associated with stable identifiers so their metadata and retrieval information can be maintained independently.

---

# 🏗️ System Components

### Streamlit Interface

Provides the user-facing application including:

- Document management
- Conversations
- Chat interface
- Document analysis
- Application navigation

### Document Processing

Responsible for:

- PDF processing
- Text extraction
- Text cleaning
- Chunking
- Document preparation

### Embedding Layer

Converts document chunks and user queries into vector representations for semantic retrieval.

### FAISS Vector Store

Stores document embeddings and performs similarity search to retrieve relevant document content.

### Prompt Layer

Combines:

- User query
- Retrieved document context
- Prompt instructions

to construct the final LLM request.

### NVIDIA Nemotron

Processes the retrieved context and generates the final natural-language response.

---

# 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| UI Framework | Streamlit |
| LLM | NVIDIA Nemotron |
| LLM API | NVIDIA Integrate API |
| Architecture | Retrieval-Augmented Generation |
| Embeddings | Sentence Transformers |
| Vector Database | FAISS |
| PDF Processing | PyMuPDF / pypdf |
| OCR | pytesseract |
| Version Control | Git + GitHub |
| Deployment | Streamlit Cloud |

---

# 📁 Project Structure

    NeMoDoc/
    │
    ├── README.md
    ├── requirements.txt
    ├── .gitignore
    ├── app.py
    │
    ├── src/
    │   ├── document_processor.py
    │   ├── embeddings.py
    │   ├── llm.py
    │   ├── prompts.py
    │   ├── retriever.py
    │   ├── vector_store.py
    │   │
    │   ├── chat/
    │   │   ├── history.py
    │   │   ├── manager.py
    │   │   └── models.py
    │   │
    │   ├── documents/
    │   │   ├── manager.py
    │   │   └── models.py
    │   │
    │   └── ui/
    │       ├── chat.py
    │       ├── components.py
    │       ├── sidebar.py
    │       └── styles.py
    │
    ├── data/
    │   ├── uploads/
    │   └── documents/
    │
    └── tests/

---

# ⚙️ Running Locally

## 1. Clone the Repository

    git clone https://github.com/KunalLuthra05/nemodoc-enterprise-document-intelligence.git
    cd nemodoc-enterprise-document-intelligence

## 2. Create a Virtual Environment

### Windows

    python -m venv .venv
    .venv\Scripts\activate

### Linux / macOS

    python3 -m venv .venv
    source .venv/bin/activate

## 3. Install Dependencies

    pip install -r requirements.txt

## 4. Configure NVIDIA API

Create a .env file containing:

    NVIDIA_API_KEY=your_api_key_here
    NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
    NVIDIA_MODEL=nvidia/nemotron-3-super-120b-a12b

## 5. Run the Application

    streamlit run app.py

The application will be available locally at:

    http://localhost:8501

---

# ☁️ Deployment

NeMoDoc is deployed using Streamlit Cloud and connected directly to the GitHub repository.

    GitHub Repository
           │
           ▼
       main branch
           │
           ▼
      Streamlit Cloud
           │
           ▼
      Application Build
           │
           ▼
          NeMoDoc

The production NVIDIA API credentials are stored securely using Streamlit Secrets instead of being committed to the repository.

Example Streamlit Secrets configuration:

    NVIDIA_API_KEY = "your_actual_api_key"
    NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MODEL = "nvidia/nemotron-3-super-120b-a12b"

Never commit your real NVIDIA API key to GitHub.

---

# 🔐 Security

API credentials are intentionally kept outside the source code.

### Local Development

    .env
      ↓
    NeMoDoc
      ↓
    NVIDIA API

### Cloud Deployment

    Streamlit Secrets
          ↓
       NeMoDoc
          ↓
     NVIDIA API

This prevents sensitive credentials from being exposed through the public repository.

---

# 🎓 Academic Context

NeMoDoc was developed as part of the IIT Delhi certification program:

## Introduction to LLM and Prompt Engineering

The project applies concepts covered during the program, including:

- Large Language Models
- Prompt Engineering
- Retrieval-Augmented Generation
- Embeddings
- Vector Databases
- Document Intelligence
- LLM Application Development
- Generative AI workflows
- Responsible AI concepts

The project serves as a practical implementation of these concepts by combining them into a complete working LLM application.

---

# 🎯 Project Objective

The goal of NeMoDoc is to demonstrate how modern LLM technologies can be combined to build a practical document intelligence system.

    Documents
        +
    Document Processing
        +
    Embeddings
        +
    Vector Search
        +
    Retrieval-Augmented Generation
        +
    Prompt Engineering
        +
    NVIDIA Nemotron
        +
    Conversational UI
        ↓
    Enterprise Document Intelligence

Rather than treating an LLM as a simple chatbot, NeMoDoc uses the LLM as part of a larger information retrieval and document understanding pipeline.

---

# ⚠️ Limitations

NeMoDoc is primarily an academic and demonstration project.

A production enterprise deployment could additionally require:

- User authentication
- Role-based access control
- Multi-user data isolation
- Cloud object storage
- Managed vector databases
- Rate limiting
- Usage monitoring
- Advanced evaluation
- Production observability
- Stronger security controls
- Scalable background processing
- Additional document formats

---

# 🔗 Links

### 🌐 Live Application

https://nemadoc-ai.streamlit.app/

### 💻 GitHub Repository

https://github.com/KunalLuthra05/nemodoc-enterprise-document-intelligence

---

# 👨‍💻 Built With

Python • Streamlit • NVIDIA Nemotron • FAISS • Sentence Transformers • RAG

---

> Built as a practical implementation of Large Language Models, Retrieval-Augmented Generation, Prompt Engineering, and Document Intelligence as part of the IIT Delhi certification program.

# 🚀 NeMoDoc

### Enterprise Document Intelligence powered by NVIDIA Nemotron
