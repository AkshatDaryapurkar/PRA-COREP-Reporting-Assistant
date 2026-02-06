"""
Regulatory chunk data model.
"""
from pydantic import BaseModel


class RegulatoryChunk(BaseModel):
    """Represents a chunk of regulatory text from the knowledge base."""
    
    id: str
    """Unique identifier, e.g., 'PRA_OWNFUNDS_001'"""
    
    source: str
    """Source document, e.g., 'PRA Rulebook'"""
    
    paragraph: str
    """Reference paragraph/article, e.g., 'Article 26'"""
    
    text: str
    """Full regulatory text content"""
    
    def to_context_string(self) -> str:
        """Format chunk for LLM context."""
        return f"[{self.id}] {self.source}, {self.paragraph}:\n{self.text}"
