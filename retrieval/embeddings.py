"""
Embedding generation using sentence-transformers.
"""
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

from models.regulatory import RegulatoryChunk
import config


class EmbeddingGenerator:
    """Generates embeddings for text using sentence-transformers."""
    
    def __init__(self, model_name: str = None):
        """Initialize with specified model or default from config."""
        self.model_name = model_name or config.EMBEDDING_MODEL
        self._model = None
    
    @property
    def model(self) -> SentenceTransformer:
        """Lazy load the embedding model."""
        if self._model is None:
            self._model = SentenceTransformer(self.model_name)
        return self._model
    
    def embed_text(self, text: str) -> np.ndarray:
        """Generate embedding for a single text string."""
        return self.model.encode(text, convert_to_numpy=True)
    
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for multiple texts."""
        return self.model.encode(texts, convert_to_numpy=True)
    
    def embed_chunks(self, chunks: List[RegulatoryChunk]) -> np.ndarray:
        """Generate embeddings for regulatory chunks using their text content."""
        texts = [chunk.text for chunk in chunks]
        return self.embed_texts(texts)
