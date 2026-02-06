"""
Mock regulatory knowledge base for PRA COREP Own Funds.
Contains 10 regulatory chunks covering CET1, AT1, Tier 2, and total own funds.
"""
from typing import List
from models.regulatory import RegulatoryChunk


REGULATORY_CORPUS: List[dict] = [
    {
        "id": "PRA_OWNFUNDS_001",
        "source": "PRA Rulebook",
        "paragraph": "Article 26",
        "text": "Common Equity Tier 1 capital shall include the following items: (a) capital instruments, provided the conditions laid down in Article 28 are met; (b) share premium accounts related to the instruments referred to in point (a); (c) retained earnings; (d) accumulated other comprehensive income; (e) other reserves."
    },
    {
        "id": "PRA_OWNFUNDS_002",
        "source": "PRA Rulebook",
        "paragraph": "Article 28",
        "text": "Capital instruments qualify as Common Equity Tier 1 instruments only if the following conditions are met: (a) the instruments are issued directly by the institution with the prior approval of the owners; (b) the instruments are paid up and their purchase is not funded by the institution; (c) the instruments are perpetual; (d) the principal amount of the instruments may not be reduced except in liquidation."
    },
    {
        "id": "PRA_OWNFUNDS_003",
        "source": "PRA Rulebook",
        "paragraph": "Article 36",
        "text": "Institutions shall deduct the following from Common Equity Tier 1 items: (a) losses for the current financial year; (b) intangible assets; (c) deferred tax assets that rely on future profitability; (d) defined benefit pension fund assets; (e) direct and indirect holdings of own CET1 instruments."
    },
    {
        "id": "PRA_OWNFUNDS_004",
        "source": "PRA Rulebook",
        "paragraph": "Article 51",
        "text": "Additional Tier 1 capital shall consist of capital instruments meeting conditions in Article 52, plus related share premium. AT1 instruments are subordinated to Tier 2 instruments, depositors and general creditors. AT1 instruments must be perpetual with no maturity date and may be called only after minimum 5 years."
    },
    {
        "id": "PRA_OWNFUNDS_005",
        "source": "PRA Rulebook",
        "paragraph": "Article 52",
        "text": "Additional Tier 1 instruments qualify if: (a) issued and paid up; (b) not purchased by the institution or its subsidiaries; (c) perpetual and provisions do not provide incentive to redeem; (d) callable only at option of issuer after minimum 5 years; (e) distributions are paid out of distributable items and are fully discretionary."
    },
    {
        "id": "PRA_OWNFUNDS_006",
        "source": "PRA Rulebook",
        "paragraph": "Article 62",
        "text": "Tier 2 capital shall consist of: (a) capital instruments meeting Article 63 conditions; (b) share premium accounts related to those instruments; (c) for institutions calculating risk-weighted exposure amounts under Standardised Approach, general credit risk adjustments up to 1.25% of risk-weighted exposure amounts."
    },
    {
        "id": "PRA_OWNFUNDS_007",
        "source": "PRA Rulebook",
        "paragraph": "Article 63",
        "text": "Tier 2 instruments qualify if: (a) issued and paid up; (b) not purchased by the institution; (c) original maturity of at least 5 years; (d) provisions do not provide incentive for early redemption; (e) callable only at option of issuer after 5 years; (f) claim on principal is subordinated to all non-subordinated creditors."
    },
    {
        "id": "PRA_OWNFUNDS_008",
        "source": "PRA Rulebook",
        "paragraph": "Article 72",
        "text": "Total Own Funds of an institution shall consist of the sum of its Tier 1 capital and Tier 2 capital. Tier 1 capital is the sum of Common Equity Tier 1 capital and Additional Tier 1 capital. Total Own Funds = CET1 + AT1 + Tier2."
    },
    {
        "id": "PRA_OWNFUNDS_009",
        "source": "PRA SS3/21",
        "paragraph": "Section 2.1",
        "text": "UK banks must report their own funds in accordance with COREP reporting template C 01.00. The template requires disclosure of CET1 capital items, CET1 deductions, AT1 capital, AT1 deductions, Tier 2 capital, Tier 2 deductions, and total own funds after all deductions."
    },
    {
        "id": "PRA_OWNFUNDS_010",
        "source": "PRA SS3/21", 
        "paragraph": "Section 2.3",
        "text": "For COREP C 01.00 reporting, UK institutions should report: Row 010 (CET1 capital before deductions), Row 020 (CET1 deductions), Row 029 (CET1 capital after deductions), Row 045 (AT1 capital), Row 060 (Total Tier 1), Row 070 (Tier 2 capital), and Row 100 (Total Own Funds). All values shall be reported in thousands."
    }
]


def get_all_chunks() -> List[RegulatoryChunk]:
    """Return all regulatory chunks as RegulatoryChunk objects."""
    return [RegulatoryChunk(**chunk) for chunk in REGULATORY_CORPUS]
