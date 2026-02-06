"""
Validation rules for COREP Own Funds output.
"""
from typing import List

from models.corep import CorepOutput, OwnFunds
import config


class Validator:
    """Validates COREP output against business rules."""
    
    def __init__(self, tolerance: float = None):
        """Initialize with tolerance for float comparisons."""
        self.tolerance = tolerance or config.VALIDATION_TOLERANCE
    
    def validate_totals(self, own_funds: OwnFunds) -> List[str]:
        """
        Validate that total_own_funds equals sum of components.
        
        Rule: total_own_funds == CET1 + AT1 + Tier2
        """
        warnings = []
        
        expected_total = (
            own_funds.common_equity_tier_1 +
            own_funds.additional_tier_1 +
            own_funds.tier_2
        )
        
        actual_total = own_funds.total_own_funds
        difference = abs(expected_total - actual_total)
        
        if difference > self.tolerance:
            warnings.append(
                f"VALIDATION ERROR: total_own_funds ({actual_total}) does not equal "
                f"CET1 + AT1 + Tier2 ({expected_total}). "
                f"Difference: {difference:.2f}"
            )
        
        return warnings
    
    def validate_non_negative(self, own_funds: OwnFunds) -> List[str]:
        """
        Validate that all values are non-negative.
        
        Rule: All capital values must be >= 0
        """
        warnings = []
        
        fields = [
            ("common_equity_tier_1", own_funds.common_equity_tier_1),
            ("additional_tier_1", own_funds.additional_tier_1),
            ("tier_2", own_funds.tier_2),
            ("total_own_funds", own_funds.total_own_funds),
        ]
        
        for field_name, value in fields:
            if value < 0:
                warnings.append(
                    f"VALIDATION ERROR: {field_name} ({value}) must be >= 0"
                )
        
        return warnings
    
    def validate_cet1_minimum(self, own_funds: OwnFunds) -> List[str]:
        """
        Validate CET1 is typically largest component.
        
        This is a soft warning, not an error.
        """
        warnings = []
        
        if own_funds.common_equity_tier_1 < own_funds.additional_tier_1:
            warnings.append(
                "WARNING: CET1 is typically larger than AT1. "
                "Please verify this is intentional."
            )
        
        if own_funds.common_equity_tier_1 < own_funds.tier_2:
            warnings.append(
                "WARNING: CET1 is typically larger than Tier 2. "
                "Please verify this is intentional."
            )
        
        return warnings
    
    def run_all_validations(self, output: CorepOutput) -> List[str]:
        """
        Run all validation rules and return aggregated warnings.
        
        Args:
            output: CorepOutput to validate
            
        Returns:
            List of all warning messages
        """
        all_warnings = []
        
        # Core validations
        all_warnings.extend(self.validate_totals(output.own_funds))
        all_warnings.extend(self.validate_non_negative(output.own_funds))
        
        # Soft validations
        all_warnings.extend(self.validate_cet1_minimum(output.own_funds))
        
        return all_warnings
