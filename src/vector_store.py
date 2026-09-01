import json
from pathlib import Path

import faiss
import numpy as np


class VectorStore:
    """
    FAISS-based vector store for document chunk embeddings.

    Supports:

    - Adding vectors
    - Similarity search
    - Saving the FAISS index to disk
    - Saving associated text chunks to disk
    - Loading a previously saved index
    """

    def __init__(self, dimension: int):
        """
        Initialize the FAISS index.

        Args:
            dimension:
                Size of each embedding vector.
        """

        self.dimension = dimension

        # Inner product works well with normalized embeddings.
        self.index = faiss.IndexFlatIP(
            dimension
        )

        # Original document chunks.
        self.chunks: list[str] = []

    # ========================================================
    # ADD
    # ========================================================

    def add(
        self,
        embeddings,
        chunks: list[str],
    ):
        """
        Add embeddings and their corresponding chunks.
        """

        if len(embeddings) != len(chunks):

            raise ValueError(
                "The number of embeddings must match "
                "the number of chunks."
            )

        if len(embeddings) == 0:
            return

        vectors = np.asarray(
            embeddings,
            dtype="float32",
        )

        self.index.add(
            vectors
        )

        self.chunks.extend(
            chunks
        )

    # ========================================================
    # SEARCH
    # ========================================================

    def search(
        self,
        query_embedding,
        top_k: int = 3,
    ):
        """
        Search for the most relevant chunks.
        """

        if self.index.ntotal == 0:
            return []

        query_vector = np.asarray(
            query_embedding,
            dtype="float32",
        )

        if query_vector.ndim == 1:

            query_vector = (
                query_vector.reshape(1, -1)
            )

        scores, indices = self.index.search(
            query_vector,
            min(
                top_k,
                self.index.ntotal,
            ),
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0],
        ):

            if index == -1:
                continue

            results.append(
                {
                    "chunk": self.chunks[index],
                    "score": float(score),
                }
            )

        return results

    # ========================================================
    # SAVE
    # ========================================================

    def save(
        self,
        directory: str,
    ) -> None:
        """
        Save the FAISS index and document chunks to disk.

        Creates:

            directory/
                index.faiss
                chunks.json
                metadata.json
        """

        path = Path(
            directory
        )

        path.mkdir(
            parents=True,
            exist_ok=True,
        )

        # ----------------------------------------------------
        # Save FAISS index.
        # ----------------------------------------------------

        index_path = (
            path / "index.faiss"
        )

        faiss.write_index(
            self.index,
            str(index_path),
        )

        # ----------------------------------------------------
        # Save chunks.
        # ----------------------------------------------------

        chunks_path = (
            path / "chunks.json"
        )

        with open(
            chunks_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.chunks,
                file,
                ensure_ascii=False,
                indent=2,
            )

        # ----------------------------------------------------
        # Save metadata.
        # ----------------------------------------------------

        metadata_path = (
            path / "metadata.json"
        )

        metadata = {
            "dimension": self.dimension,
            "vectors": self.index.ntotal,
            "chunks": len(self.chunks),
        }

        with open(
            metadata_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                metadata,
                file,
                indent=2,
            )

    # ========================================================
    # LOAD
    # ========================================================

    @classmethod
    def load(
        cls,
        directory: str,
    ):
        """
        Load a previously saved VectorStore.

        Returns:
            VectorStore instance.

        Raises:
            FileNotFoundError:
                If the stored index or chunks are missing.
        """

        path = Path(
            directory
        )

        index_path = (
            path / "index.faiss"
        )

        chunks_path = (
            path / "chunks.json"
        )

        metadata_path = (
            path / "metadata.json"
        )

        if not index_path.exists():

            raise FileNotFoundError(
                f"FAISS index not found: "
                f"{index_path}"
            )

        if not chunks_path.exists():

            raise FileNotFoundError(
                f"Chunk data not found: "
                f"{chunks_path}"
            )

        # ----------------------------------------------------
        # Load metadata.
        # ----------------------------------------------------

        dimension = None

        if metadata_path.exists():

            with open(
                metadata_path,
                "r",
                encoding="utf-8",
            ) as file:

                metadata = json.load(
                    file
                )

            dimension = metadata.get(
                "dimension"
            )

        # ----------------------------------------------------
        # Load FAISS index.
        # ----------------------------------------------------

        index = faiss.read_index(
            str(index_path)
        )

        # ----------------------------------------------------
        # If metadata was unavailable, get dimension
        # directly from FAISS.
        # ----------------------------------------------------

        if dimension is None:

            dimension = index.d

        # ----------------------------------------------------
        # Create VectorStore instance.
        # ----------------------------------------------------

        store = cls(
            dimension=dimension
        )

        store.index = index

        # ----------------------------------------------------
        # Load chunks.
        # ----------------------------------------------------

        with open(
            chunks_path,
            "r",
            encoding="utf-8",
        ) as file:

            store.chunks = json.load(
                file
            )

        # ----------------------------------------------------
        # Validate stored data.
        # ----------------------------------------------------

        if len(store.chunks) != store.index.ntotal:

            raise ValueError(
                "Stored chunk count does not match "
                "the number of vectors in the FAISS index."
            )

        return store

    # ========================================================
    # LENGTH
    # ========================================================

    def __len__(self):
        """
        Return the number of stored vectors.
        """

        return self.index.ntotal


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    import tempfile

    # --------------------------------------------------------
    # Create a test store.
    # --------------------------------------------------------

    dimension = 384

    store = VectorStore(
        dimension
    )

    # --------------------------------------------------------
    # Create fake normalized vectors.
    # --------------------------------------------------------

    test_embeddings = np.random.rand(
        3,
        dimension,
    ).astype(
        "float32"
    )

    test_embeddings /= np.linalg.norm(
        test_embeddings,
        axis=1,
        keepdims=True,
    )

    test_chunks = [
        "This document explains Large Language Models.",
        "This section discusses Retrieval-Augmented Generation.",
        "This section explains prompt engineering.",
    ]

    store.add(
        test_embeddings,
        test_chunks,
    )

    print(
        f"Vectors stored: {len(store)}"
    )

    # --------------------------------------------------------
    # Test search.
    # --------------------------------------------------------

    results = store.search(
        test_embeddings[0],
        top_k=2,
    )

    print(
        "\nSearch results:"
    )

    for result in results:

        print(
            f"\nScore: "
            f"{result['score']:.4f}"
        )

        print(
            f"Chunk: "
            f"{result['chunk']}"
        )

    # --------------------------------------------------------
    # Test persistence.
    # --------------------------------------------------------

    with tempfile.TemporaryDirectory() as directory:

        print(
            f"\nSaving test store to: "
            f"{directory}"
        )

        store.save(
            directory
        )

        loaded_store = (
            VectorStore.load(
                directory
            )
        )

        print(
            f"Loaded vectors: "
            f"{len(loaded_store)}"
        )

        print(
            f"Loaded chunks: "
            f"{len(loaded_store.chunks)}"
        )

        loaded_results = (
            loaded_store.search(
                test_embeddings[0],
                top_k=2,
            )
        )

        print(
            "Persistence test passed."
        )