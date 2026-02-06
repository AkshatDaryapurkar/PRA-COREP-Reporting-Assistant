"""
Output formatters for COREP reporting.
"""
import json
from typing import List

from tabulate import tabulate

from models.corep import CorepOutput, FieldJustification


class ReportGenerator:
    """Generates formatted outputs for COREP results."""
    
    @staticmethod
    def to_json(output: CorepOutput, indent: int = 2) -> str:
        """
        Generate schema-validated JSON output.
        
        Args:
            output: Validated CorepOutput
            indent: JSON indentation level
            
        Returns:
            JSON string representation
        """
        return output.model_dump_json(indent=indent)
    
    @staticmethod
    def to_table(output: CorepOutput) -> str:
        """
        Generate human-readable COREP table.
        
        Args:
            output: CorepOutput with own_funds data
            
        Returns:
            Formatted ASCII table
        """
        own_funds = output.own_funds
        
        table_data = [
            ["Common Equity Tier 1 (CET1)", f"{own_funds.common_equity_tier_1:,.2f}"],
            ["Additional Tier 1 (AT1)", f"{own_funds.additional_tier_1:,.2f}"],
            ["Total Tier 1 Capital", f"{own_funds.common_equity_tier_1 + own_funds.additional_tier_1:,.2f}"],
            ["Tier 2 (T2)", f"{own_funds.tier_2:,.2f}"],
            ["─" * 35, "─" * 15],
            ["TOTAL OWN FUNDS", f"{own_funds.total_own_funds:,.2f}"],
        ]
        
        headers = ["COREP C 01.00 - Own Funds", "Amount (Millions)"]
        
        return tabulate(table_data, headers=headers, tablefmt="simple")
    
    @staticmethod
    def to_audit_log(output: CorepOutput) -> str:
        """
        Generate formatted audit log.
        
        Args:
            output: CorepOutput with audit_log entries
            
        Returns:
            Formatted audit log string
        """
        lines = ["=" * 60, "AUDIT LOG - COREP Own Funds Population", "=" * 60, ""]
        
        for entry in output.audit_log:
            lines.append(f"📋 Field: {entry.field}")
            lines.append(f"   Value: {entry.value:,.2f}")
            lines.append(f"   Rules: {', '.join(entry.rule_ids)}")
            lines.append(f"   Reason: {entry.explanation}")
            lines.append("")
        
        if output.warnings:
            lines.append("-" * 60)
            lines.append("⚠️  WARNINGS:")
            for warning in output.warnings:
                lines.append(f"   • {warning}")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    @staticmethod
    def generate_full_report(output: CorepOutput) -> str:
        """
        Generate complete report with all formats.
        
        Args:
            output: Complete CorepOutput
            
        Returns:
            Full formatted report string
        """
        sections = [
            "╔══════════════════════════════════════════════════════════════╗",
            "║         PRA COREP OWN FUNDS REPORTING ASSISTANT              ║",
            "╚══════════════════════════════════════════════════════════════╝",
            "",
            "═══ A. STRUCTURED JSON OUTPUT ═══",
            "",
            ReportGenerator.to_json(output),
            "",
            "═══ B. COREP TABLE EXTRACT ═══",
            "",
            ReportGenerator.to_table(output),
            "",
            "═══ C. AUDIT LOG ═══",
            "",
            ReportGenerator.to_audit_log(output),
        ]
        
        return "\n".join(sections)
