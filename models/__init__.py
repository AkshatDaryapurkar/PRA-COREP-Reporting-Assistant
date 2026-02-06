"""Models package for COREP reporting assistant."""
from .regulatory import RegulatoryChunk
from .corep import OwnFunds, FieldJustification, CorepOutput

__all__ = ["RegulatoryChunk", "OwnFunds", "FieldJustification", "CorepOutput"]
