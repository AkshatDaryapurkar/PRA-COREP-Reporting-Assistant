"""
FAISS vector store for semantic retrieval.
"""
from typing import List, Tuple
import numpy as np
import faiss

from models.regulatory import RegulatoryChunk
from .embeddings import EmbeddingGenerator
import config


class VectorStore:
    """FAISS-based vector store for regulatory chunk retrieval."""
    
    def __init__(self, embedding_generator: EmbeddingGenerator = None):
        """Initialize vector store with optional embedding generator."""
        self.embedding_generator = embedding_generator or EmbeddingGenerator()
        self.index: faiss.IndexFlatL2 = None
        self.chunks: List[RegulatoryChunk] = []
    
    def build_index(self, chunks: List[RegulatoryChunk]) -> None:
        """Build FAISS index from regulatory chunks."""
        self.chunks = chunks
        
        # Generate embeddings for all chunks
        embeddings = self.embedding_generator.embed_chunks(chunks)
        
        # Create FAISS index
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype(np.float32))
    
    def retrieve(
        self, 
        query: str, 
        top_k: int = None
    ) -> List[Tuple[RegulatoryChunk, float]]:
        """
        Retrieve top-k most relevant chunks for a query.
        
        Args:
            query: User question/query text
            top_k: Number of chunks to retrieve (default from config)
            
        Returns:
            List of (chunk, distance) tuples sorted by relevance
        """
        if self.index is None:
            raise ValueError("Index not built. Call build_index() first.")
        
        top_k = top_k or config.TOP_K_CHUNKS
        
        # Embed the query
        query_embedding = self.embedding_generator.embed_text(query)
        query_embedding = query_embedding.reshape(1, -1).astype(np.float32)
        
        # Search the index
        distances, indices = self.index.search(query_embedding, top_k)
        
        # Return chunks with their distances
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.chunks):
                results.append((self.chunks[idx], float(dist)))
        
        return results
    
    def retrieve_chunks(self, query: str, top_k: int = None) -> List[RegulatoryChunk]:
        """Retrieve just the chunks without distances."""
        results = self.retrieve(query, top_k)
        return [chunk for chunk, _ in results]
