"""
COREP Own Funds schema models.
"""
from typing import List
from pydantic import BaseModel, Field


class OwnFunds(BaseModel):
    """COREP Own Funds (C 01.00) capital breakdown."""
    
    common_equity_tier_1: float = Field(
        ..., 
        description="Common Equity Tier 1 (CET1) capital in currency units",
        ge=0
    )
    additional_tier_1: float = Field(
        ..., 
        description="Additional Tier 1 (AT1) capital in currency units",
        ge=0
    )
    tier_2: float = Field(
        ..., 
        description="Tier 2 (T2) capital in currency units",
        ge=0
    )
    total_own_funds: float = Field(
        ..., 
        description="Total Own Funds = CET1 + AT1 + Tier2",
        ge=0
    )


class FieldJustification(BaseModel):
    """Audit log entry explaining a COREP field population."""
    
    field: str = Field(
        ..., 
        description="Name of the COREP field"
    )
    value: float = Field(
        ..., 
        description="Value assigned to the field"
    )
    rule_ids: List[str] = Field(
        default_factory=list,
        description="IDs of regulatory chunks used to determine this value"
    )
    explanation: str = Field(
        ..., 
        description="Reasoning for why this value was assigned"
    )


class CorepOutput(BaseModel):
    """Complete COREP output with own funds, audit log, and warnings."""
    
    own_funds: OwnFunds = Field(
        ..., 
        description="Populated COREP Own Funds table"
    )
    audit_log: List[FieldJustification] = Field(
        default_factory=list,
        description="Audit trail explaining each field"
    )
    warnings: List[str] = Field(
        default_factory=list,
        description="Validation warnings, if any"
    )
