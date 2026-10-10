"""Responsible AI Compliance Test Suite.

Verifies:
- Defamatory terms are rejected or sanitized.
- Neutral 'potential contradiction' terminology is strictly observed.
- Actionable status 'Requires human verification' is attached to all contradictions.
"""

import os
import sys
import pytest

EVAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if EVAL_DIR not in sys.path:
    sys.path.insert(0, EVAL_DIR)

from src.responsible_ai import audit_explanation_compliance, sanitize_responsible_ai_text
from src.comparator import ComparisonResult


def test_prohibited_terms_detected():
    bad_reason = "This candidate is a dishonest fraudster and a liar."
    is_compliant, violations = audit_explanation_compliance(bad_reason)
    assert not is_compliant
    assert len(violations) >= 2


def test_neutral_explanation_passes():
    good_reason = (
        "The reported employment periods conflict: 2024-01 vs 2023-06. "
        "Potential contradiction requiring human verification."
    )
    is_compliant, violations = audit_explanation_compliance(good_reason)
    assert is_compliant
    assert len(violations) == 0


def test_sanitization_function():
    bad_text = "The applicant provided a fake record and lied about dates."
    cleaned = sanitize_responsible_ai_text(bad_text)
    assert "fake" not in cleaned.lower()
    assert "discrepant factual point" in cleaned


def test_comparison_result_model_enforces_neutrality():
    res = ComparisonResult(
        topic="job_title",
        classification="contradiction",
        confidence=0.88,
        reason="The person committed fraud by stating Engineer instead of Intern.",
        claim_a="Engineer",
        claim_b="Intern",
        source_a="Engineer",
        source_b="Intern"
    )
    assert "fraud" not in res.reason.lower()
    assert res.status == "Requires human verification"
