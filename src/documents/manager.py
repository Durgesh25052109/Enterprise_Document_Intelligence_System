from pathlib import Path
import hashlib

from src.retriever import Retriever

from .models import Document


class DocumentManager:
    """
    Manages NeMoDoc documents independently from chats.

    Responsibilities:

    - Generate stable document IDs
    - Process PDFs
    - Persist vector stores
    - Reuse previously processed documents
    - Provide retrievers for documents
    """

    def __init__(
        self,
        storage_directory: str = "data/documents",
    ):
        """
        Initialize the document manager.
        """

        self.storage_directory = Path(
            storage_directory
        )

        self.storage_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        # Documents currently known to this manager.
        self.documents: dict[str, Document] = {}

        # Active retrievers in memory.
        self.retrievers: dict[str, Retriever] = {}

    # ========================================================
    # DOCUMENT ID
    # ========================================================

    @staticmethod
    def generate_document_id(
        file_bytes: bytes,
    ) -> str:
        """
        Generate a stable ID from document contents.
        """

        return hashlib.sha256(
            file_bytes
        ).hexdigest()

    # ========================================================
    # STORAGE PATH
    # ========================================================

    def get_storage_path(
        self,
        document_id: str,
    ) -> Path:
        """
        Return the persistent storage directory
        for a document.
        """

        return (
            self.storage_directory
            / document_id
        )

    # ========================================================
    # CHECK PERSISTENCE
    # ========================================================

    def is_persisted(
        self,
        document_id: str,
    ) -> bool:
        """
        Check whether a persisted vector store exists.
        """

        storage_path = (
            self.get_storage_path(
                document_id
            )
        )

        return (
            (storage_path / "index.faiss").exists()
            and
            (storage_path / "chunks.json").exists()
        )

    # ========================================================
    # ADD / LOAD DOCUMENT
    # ========================================================

    def add_document(
        self,
        file_path: str,
        file_bytes: bytes | None = None,
    ) -> Document:
        """
        Add a document to NeMoDoc.

        If the document was already processed and its
        vector store exists on disk, reuse it.

        Otherwise process the PDF and persist the
        resulting vector store.
        """

        path = Path(
            file_path
        )

        if not path.exists():

            raise FileNotFoundError(
                f"Document not found: {file_path}"
            )

        # ----------------------------------------------------
        # Read file bytes if not supplied.
        # ----------------------------------------------------

        if file_bytes is None:

            file_bytes = path.read_bytes()

        # ----------------------------------------------------
        # Generate stable document ID.
        # ----------------------------------------------------

        document_id = (
            self.generate_document_id(
                file_bytes
            )
        )

        storage_path = (
            self.get_storage_path(
                document_id
            )
        )

        # ====================================================
        # CASE 1 — ALREADY LOADED IN MEMORY
        # ====================================================

        if document_id in self.documents:

            return self.documents[
                document_id
            ]

        # ====================================================
        # CASE 2 — PERSISTED ON DISK
        # ====================================================

        if self.is_persisted(
            document_id
        ):

            print(
                f"\nLoading existing document: "
                f"{path.name}"
            )

            retriever = (
                Retriever.from_vector_store(
                    str(storage_path)
                )
            )

            # ------------------------------------------------
            # Create metadata from persisted data.
            # ------------------------------------------------

            chunks = (
                retriever.vector_store.chunks
            )

            characters = 0

            if chunks:

                characters = sum(
                    len(chunk)
                    for chunk in chunks
                )

            document = Document(
                document_id=document_id,
                filename=path.name,
                file_hash=document_id,
                storage_path=str(
                    storage_path
                ),
                characters=characters,
                chunks=len(chunks),
            )

            self.documents[
                document_id
            ] = document

            self.retrievers[
                document_id
            ] = retriever

            return document

        # ====================================================
        # CASE 3 — NEW DOCUMENT
        # ====================================================

        print(
            f"\nProcessing new document: "
            f"{path.name}"
        )

        retriever = Retriever()

        document_info = (
            retriever.load_document(
                str(path)
            )
        )

        # ----------------------------------------------------
        # Store in memory.
        # ----------------------------------------------------

        self.retrievers[
            document_id
        ] = retriever

        # ----------------------------------------------------
        # Create metadata.
        # ----------------------------------------------------

        document = Document(
            document_id=document_id,
            filename=path.name,
            file_hash=document_id,
            storage_path=str(
                storage_path
            ),
            characters=document_info[
                "characters"
            ],
            chunks=document_info[
                "chunks"
            ],
        )

        self.documents[
            document_id
        ] = document

        return document

    # ========================================================
    # GET DOCUMENT
    # ========================================================

    def get_document(
        self,
        document_id: str,
    ) -> Document | None:
        """
        Return document metadata.
        """

        return self.documents.get(
            document_id
        )

    # ========================================================
    # GET RETRIEVER
    # ========================================================

    def get_retriever(
        self,
        document_id: str,
    ) -> Retriever | None:
        """
        Return the retriever for a document.

        If it is already in memory, return it directly.

        If it exists on disk, load it automatically.
        """

        # ----------------------------------------------------
        # In-memory retriever.
        # ----------------------------------------------------

        if document_id in self.retrievers:

            return self.retrievers[
                document_id
            ]

        # ----------------------------------------------------
        # Persistent retriever.
        # ----------------------------------------------------

        storage_path = (
            self.get_storage_path(
                document_id
            )
        )

        if not self.is_persisted(
            document_id
        ):

            return None

        retriever = (
            Retriever.from_vector_store(
                str(storage_path)
            )
        )

        self.retrievers[
            document_id
        ] = retriever

        return retriever

    # ========================================================
    # LIST DOCUMENTS
    # ========================================================

    def list_documents(
        self,
    ) -> list[Document]:
        """
        Return documents currently registered
        in memory.
        """

        return sorted(
            self.documents.values(),
            key=lambda document: (
                document.updated_at
            ),
            reverse=True,
        )

    # ========================================================
    # DOCUMENT EXISTS
    # ========================================================

    def has_document(
        self,
        document_id: str,
    ) -> bool:
        """
        Check whether a document exists either
        in memory or on disk.
        """

        return (
            document_id in self.documents
            or
            self.is_persisted(
                document_id
            )
        )

    # ========================================================
    # DOCUMENT COUNT
    # ========================================================

    def __len__(self) -> int:
        """
        Return the number of currently registered
        documents.
        """

        return len(
            self.documents
        )