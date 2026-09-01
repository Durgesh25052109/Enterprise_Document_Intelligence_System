from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


class EmbeddingModel:
    """
    Wrapper around the Sentence Transformer embedding model.
    """

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode(self, texts: list[str]):
        """
        Convert a list of text strings into embedding vectors.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        return embeddings


if __name__ == "__main__":
    model = EmbeddingModel()

    test_texts = [
        "Employees are entitled to annual leave.",
        "The company provides vacation days to employees.",
        "The weather is sunny today.",
    ]

    embeddings = model.encode(test_texts)

    print(f"Number of embeddings: {len(embeddings)}")
    print(f"Embedding dimensions: {embeddings.shape[1]}")
    print(f"Embedding shape: {embeddings.shape}")