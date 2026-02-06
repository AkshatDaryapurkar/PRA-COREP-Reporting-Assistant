"""
Prompt templates for LLM reasoning.
"""
from typing import List

from models.regulatory import RegulatoryChunk
from models.corep import CorepOutput


# JSON Schema for LLM output
COREP_SCHEMA = '''
{
    "own_funds": {
        "common_equity_tier_1": <float>,
        "additional_tier_1": <float>,
        "tier_2": <float>,
        "total_own_funds": <float>
    },
    "audit_log": [
        {
            "field": "<field_name>",
            "value": <float>,
            "rule_ids": ["<rule_id_1>", "<rule_id_2>"],
            "explanation": "<reasoning for this value>"
        }
    ],
    "warnings": ["<optional warning messages>"]
}
'''


SYSTEM_PROMPT_TEMPLATE = '''You are a regulatory reporting expert specializing in PRA COREP reporting for UK banks.

Your task is to populate the COREP Own Funds (C 01.00) template based on the regulatory text provided and the user's question.

## Instructions:
1. Analyze the retrieved regulatory text carefully
2. Use SAMPLE/MOCK financial data to populate the COREP fields (this is a prototype)
3. For each field, cite which regulatory chunk IDs you used
4. Explain your reasoning for each value
5. Ensure total_own_funds = common_equity_tier_1 + additional_tier_1 + tier_2

## Output Format:
Return ONLY valid JSON matching this exact schema:
{schema}

## Important:
- Use realistic sample values (e.g., CET1: 50000, AT1: 10000, Tier2: 15000)
- Values should be in millions (currency units)
- All values must be >= 0
- Cite specific rule IDs (e.g., PRA_OWNFUNDS_001) in the audit_log
- Provide clear explanations linking rules to values
'''


USER_PROMPT_TEMPLATE = '''## User Question
{question}

## Retrieved Regulatory Text
The following regulatory excerpts are most relevant to the question:

{chunks_text}

## Task
Based on the regulatory text above and the user's question:
1. Populate the COREP Own Funds table with appropriate sample values
2. For each field, cite the rule_ids used and explain your reasoning
3. Ensure arithmetic consistency: total_own_funds = CET1 + AT1 + Tier2
4. Return ONLY the JSON output, no other text
'''


def build_system_prompt() -> str:
    """Build the system prompt with schema."""
    return SYSTEM_PROMPT_TEMPLATE.format(schema=COREP_SCHEMA)


def build_user_prompt(question: str, chunks: List[RegulatoryChunk]) -> str:
    """
    Build the user prompt with question and retrieved chunks.
    
    Args:
        question: User's natural language question
        chunks: Retrieved regulatory chunks
        
    Returns:
        Formatted user prompt
    """
    chunks_text = "\n\n".join([
        f"---\n{chunk.to_context_string()}\n---"
        for chunk in chunks
    ])
    
    return USER_PROMPT_TEMPLATE.format(
        question=question,
        chunks_text=chunks_text
    )
