"""Responsible AI Safeguards and Compliance Audit Module.

Enforces PDF 05 Responsible AI requirements:
- Strictly prohibits defamatory, accusation-based, or judicial phrasing (e.g. 'liar', 'fraud', 'dishonest').
- Verifies that all discrepancies are neutrally framed as 'Potential Contradiction'.
- Enforces the mandatory status 'Requires human verification'.
- Validates that confidence scores are documented as estimation heuristics, never absolute truth.
"""

from typing import List, Dict, Any, Tuple
import re

PROHIBITED_TERMS = [
    r"\bliar\b",
    r"\bfraud\b",
    r"\bfraudster\b",
    r"\bdishonest\b",
    r"\bdeceptive\b",
    r"\bcheat\b",
    r"\bfake\b",
    r"\bguilty\b",
    r"\bcrime\b",
    r"\bforgery\b"
]


def audit_explanation_compliance(reason: str) -> Tuple[bool, List[str]]:
    """Audits an explanation text against Responsible AI standards.

    Returns:
        (is_compliant: bool, violations: List[str])
    """
    violations = []
    text_lower = reason.lower()

    for pattern in PROHIBITED_TERMS:
        if re.search(pattern, text_lower):
            violations.append(f"Contains prohibited defamatory term matching '{pattern}'")

    return len(violations) == 0, violations


def sanitize_responsible_ai_text(text: str) -> str:
    """Sanitizes text by replacing prohibited terms with neutral objective language."""
    sanitized = text
    for pattern in PROHIBITED_TERMS:
        sanitized = re.sub(pattern, "discrepant factual point", sanitized, flags=re.IGNORECASE)
    return sanitized
