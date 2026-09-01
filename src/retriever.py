from pathlib import Path

from .document_processor import (
    extract_text_from_pdf,
    chunk_text,
)

from .embeddings import EmbeddingModel

from .vector_store import VectorStore


class Retriever:
    """
    Handles document loading, chunking, embedding,
    vector storage, and similarity-based retrieval.

    Supports both:

    - Creating a new vector store
    - Loading an existing vector store from disk
    """

    def __init__(
        self,
        vector_store: VectorStore | None = None,
    ):
        """
        Initialize the retriever.

        Args:
            vector_store:
                Optional existing VectorStore.

                If supplied, the retriever reuses it
                instead of creating a new empty store.
        """

        print(
            "Initializing Retriever..."
        )

        # ----------------------------------------------------
        # 1. Embedding model
        # ----------------------------------------------------

        self.embedding_model = (
            EmbeddingModel()
        )

        # ----------------------------------------------------
        # 2. Vector store
        # ----------------------------------------------------

        if vector_store is not None:

            self.vector_store = (
                vector_store
            )

        else:

            self.vector_store = (
                VectorStore(
                    dimension=384
                )
            )

        # ----------------------------------------------------
        # Document information
        # ----------------------------------------------------

        self.document_text = ""

        self.chunks = []

    # ========================================================
    # LOAD DOCUMENT
    # ========================================================

    def load_document(
        self,
        file_path: str,
        save_directory: str | None = None,
    ):
        """
        Load and process a PDF document.

        Pipeline:

            PDF
             ↓
            text extraction
             ↓
            chunking
             ↓
            embeddings
             ↓
            FAISS
             ↓
            optional disk persistence

        Args:
            file_path:
                Path to the PDF.

            save_directory:
                Optional directory where the VectorStore
                should be saved.

        Returns:
            Dictionary containing document statistics.
        """

        path = Path(
            file_path
        )

        if not path.exists():

            raise FileNotFoundError(
                f"Document not found: "
                f"{file_path}"
            )

        print(
            f"\nReading PDF: {file_path}"
        )

        # ----------------------------------------------------
        # 1. Extract text
        # ----------------------------------------------------

        self.document_text = (
            extract_text_from_pdf(
                file_path
            )
        )

        print(
            f"Extracted characters: "
            f"{len(self.document_text)}"
        )

        # ----------------------------------------------------
        # 2. Split document into chunks
        # ----------------------------------------------------

        self.chunks = (
            chunk_text(
                self.document_text
            )
        )

        print(
            f"Total chunks: "
            f"{len(self.chunks)}"
        )

        if not self.chunks:

            raise ValueError(
                "No text chunks were created "
                "from the document."
            )

        # ----------------------------------------------------
        # 3. Generate embeddings
        # ----------------------------------------------------

        print(
            "\nGenerating embeddings..."
        )

        embeddings = (
            self.embedding_model.encode(
                self.chunks
            )
        )

        print(
            f"Embedding shape: "
            f"{embeddings.shape}"
        )

        # ----------------------------------------------------
        # 4. Store embeddings in FAISS
        # ----------------------------------------------------

        self.vector_store.add(
            embeddings,
            self.chunks,
        )

        print(
            f"\nVectors stored: "
            f"{len(self.vector_store)}"
        )

        # ----------------------------------------------------
        # 5. Persist vector store if requested
        # ----------------------------------------------------

        if save_directory is not None:

            self.vector_store.save(
                save_directory
            )

            print(
                f"\nVector store saved to: "
                f"{save_directory}"
            )

        return {
            "characters": len(
                self.document_text
            ),
            "chunks": len(
                self.chunks
            ),
            "vectors": len(
                self.vector_store
            ),
        }

    # ========================================================
    # LOAD EXISTING VECTOR STORE
    # ========================================================

    @classmethod
    def from_vector_store(
        cls,
        directory: str,
    ):
        """
        Create a Retriever from an existing
        persisted VectorStore.

        This avoids reprocessing the PDF and
        regenerating embeddings.
        """

        vector_store = (
            VectorStore.load(
                directory
            )
        )

        return cls(
            vector_store=vector_store
        )

    # ========================================================
    # RETRIEVE
    # ========================================================

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
    ):
        """
        Retrieve the most relevant document chunks.
        """

        if not query.strip():

            return []

        if len(
            self.vector_store
        ) == 0:

            return []

        # ----------------------------------------------------
        # 1. Convert query to embedding
        # ----------------------------------------------------

        query_embedding = (
            self.embedding_model.encode(
                [query]
            )
        )

        # ----------------------------------------------------
        # 2. Search FAISS
        # ----------------------------------------------------

        results = (
            self.vector_store.search(
                query_embedding[0],
                top_k=top_k,
            )
        )

        return results


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    PDF_PATH = (
        "data/uploads/test.pdf"
    )

    STORE_PATH = (
        "data/documents/test"
    )

    # --------------------------------------------------------
    # First pass:
    # Process PDF and save the vector store.
    # --------------------------------------------------------

    print(
        "\n=== FIRST LOAD ==="
    )

    retriever = Retriever()

    document_info = (
        retriever.load_document(
            PDF_PATH,
            save_directory=STORE_PATH,
        )
    )

    print(
        "\nDocument loaded successfully."
    )

    print(
        f"Characters: "
        f"{document_info['characters']}"
    )

    print(
        f"Chunks: "
        f"{document_info['chunks']}"
    )

    # --------------------------------------------------------
    # Second pass:
    # Load the saved vector store.
    # --------------------------------------------------------

    print(
        "\n=== SECOND LOAD ==="
    )

    loaded_retriever = (
        Retriever.from_vector_store(
            STORE_PATH
        )
    )

    print(
        f"Loaded vectors: "
        f"{len(loaded_retriever.vector_store)}"
    )

    # --------------------------------------------------------
    # Test retrieval.
    # --------------------------------------------------------

    query = (
        "What is this course about?"
    )

    print(
        f"\nQuery: {query}"
    )

    results = (
        loaded_retriever.retrieve(
            query,
            top_k=3,
        )
    )

    print(
        "\nRetrieved chunks:"
    )

    for index, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"\n--- Result {index} ---"
        )

        print(
            f"Similarity: "
            f"{result['score']:.4f}"
        )

        print(
            f"Text: "
            f"{result['chunk']}"
        )