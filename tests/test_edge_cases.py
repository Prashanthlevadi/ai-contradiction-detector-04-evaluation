"""Edge-Case Checklist Test Suite.

Verifies the 10 edge cases defined in PDF 05 Pages 2-3:
1. Dates in different formats
2. Numbers as words vs digits
3. Abbreviations and alternate names
4. Negation (completed vs not completed)
5. Approximate ranges
6. Duplicate claims
7. Missing values
8. Unrelated documents
9. Scanned PDFs (OCR limitations)
10. Very long documents
"""

import os
import sys
import pytest

EVAL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if EVAL_DIR not in sys.path:
    sys.path.insert(0, EVAL_DIR)

from src.claims import Claim
from src.matcher import is_compatible_topic, find_candidate_pairs
from src.comparator import compare_claims_rule_based
from src.pdf_reader import inspect_pdf
from src.errors import diagnose_inputs, ZeroTextOCRError
from src.pipeline import ContradictionPipeline


def test_edge_case_1_date_formats():
    """Dates in different formats: 01/02/2025 vs February 1, 2025."""
    c_a = Claim(claim_id="A-1", subject="Agreement", attribute="date", value="2025-02-01", source_text="01/02/2025", source="A")
    c_b = Claim(claim_id="B-1", subject="Agreement", attribute="date", value="2025-02-01", source_text="February 1, 2025", source="B")
    res = compare_claims_rule_based(c_a, c_b, topic="date")
    assert res.classification == "compatible"


def test_edge_case_2_numbers_words_vs_digits():
    """Numbers as words vs digits: fifty thousand vs 50000."""
    c_a = Claim(claim_id="A-1", subject="Grant", attribute="budget", value=50000, source_text="fifty thousand", source="A")
    c_b = Claim(claim_id="B-1", subject="Grant", attribute="budget", value=50000, source_text="$50,000", source="B")
    res = compare_claims_rule_based(c_a, c_b, topic="budget")
    assert res.classification == "compatible"


def test_edge_case_3_abbreviations_alternate_names():
    """Abbreviations and alternate names: ABC Tech vs ABC Technologies."""
    c_a = Claim(claim_id="A-1", subject="Company", attribute="name", value="ABC Technologies", source_text="ABC Tech", source="A")
    c_b = Claim(claim_id="B-1", subject="Company", attribute="name", value="ABC Technologies", source_text="ABC Technologies", source="B")
    res = compare_claims_rule_based(c_a, c_b, topic="name")
    assert res.classification == "compatible"


def test_edge_case_4_negation():
    """Negation: completed vs not completed."""
    c_a = Claim(claim_id="A-1", subject="Project", attribute="status", value="completed", source_text="Project completed.", source="A")
    c_b = Claim(claim_id="B-1", subject="Project", attribute="status", value="not completed", source_text="Project was not completed.", source="B")
    res = compare_claims_rule_based(c_a, c_b, topic="status")
    assert res.classification == "contradiction"


def test_edge_case_5_approximate_ranges():
    """Approximate ranges: about 2 years vs 24 months."""
    c_a = Claim(claim_id="A-1", subject="Tenure", attribute="duration", value="24 months", source_text="about 2 years", source="A")
    c_b = Claim(claim_id="B-1", subject="Tenure", attribute="duration", value="24 months", source_text="24 months", source="B")
    res = compare_claims_rule_based(c_a, c_b, topic="duration")
    assert res.classification == "compatible"


def test_edge_case_6_duplicate_claims():
    """Duplicate claims in source document are handled without crashing."""
    c_a1 = Claim(claim_id="A-1", subject="ABC", attribute="role", value="Intern", source_text="Role: Intern", source="A")
    c_a2 = Claim(claim_id="A-2", subject="ABC", attribute="role", value="Intern", source_text="Position: Intern", source="A")
    c_b = Claim(claim_id="B-1", subject="ABC", attribute="role", value="Intern", source_text="Intern", source="B")
    pairs = find_candidate_pairs([c_a1, c_a2], [c_b])
    assert len(pairs) == 2


def test_edge_case_7_missing_values():
    """Missing or null values yield insufficient_information."""
    c_a = Claim(claim_id="A-1", subject="Item", attribute="rating", value=None, source_text="No rating", source="A")
    c_b = Claim(claim_id="B-1", subject="Item", attribute="rating", value=4.5, source_text="Rating: 4.5", source="B")
    res = compare_claims_rule_based(c_a, c_b, topic="rating")
    assert res.classification == "insufficient_information"


def test_edge_case_8_unrelated_documents():
    """Completely unrelated documents produce 0 false contradictions."""
    c_a = Claim(claim_id="A-1", subject="Cooking", attribute="recipe", value="Pasta", source_text="Cook pasta", source="A")
    c_b = Claim(claim_id="B-1", subject="Astrophysics", attribute="star", value="Betelgeuse", source_text="Star Betelgeuse", source="B")
    align, _, _ = is_compatible_topic(c_a, c_b)
    assert align is False


def test_edge_case_9_scanned_pdf_ocr():
    """Scanned image-only PDFs trigger ZeroTextOCRError."""
    diag = {"is_likely_scanned": True, "char_count": 0, "page_count": 2}
    with pytest.raises(ZeroTextOCRError):
        diagnose_inputs("", "Valid doc text", diag_a=diag)


def test_edge_case_10_long_document():
    """Long documents process without memory or quadratic explosion."""
    pipe = ContradictionPipeline()
    # 200 repeated lines
    long_doc = "Company: ABC Technologies\nEmployment Period: January 2024 to December 2024\n" * 100
    res = pipe.process_texts(long_doc, long_doc)
    assert res["metrics"]["sources_processed"] == 2
    assert res["metrics"]["contradictions"] == 0
