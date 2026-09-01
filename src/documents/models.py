from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Document:
    """
    Represents a processed NeMoDoc document.
    """

    document_id: str
    filename: str
    file_hash: str
    storage_path: str

    characters: int = 0
    chunks: int = 0

    created_at: datetime = field(
        default_factory=datetime.now
    )

    updated_at: datetime = field(
        default_factory=datetime.now
    )

    def to_dict(self) -> dict:
        """
        Convert document metadata into a dictionary.
        """

        return {
            "document_id": self.document_id,
            "filename": self.filename,
            "file_hash": self.file_hash,
            "storage_path": self.storage_path,
            "characters": self.characters,
            "chunks": self.chunks,
            "created_at": (
                self.created_at.isoformat()
            ),
            "updated_at": (
                self.updated_at.isoformat()
            ),
        }