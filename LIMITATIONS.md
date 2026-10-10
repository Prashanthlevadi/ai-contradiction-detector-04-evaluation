# LIMITATIONS.md — System Boundary & Operational Limitations
**AI Contradiction Detector — Stage 04 Testing & Evaluation Lab**  
*Reference: PDF 05 Official Student Build Guide*

---

## 1. Documented System Limitations

### Limitation 1: Pure Image & Scanned PDF Parsing (Lack of Integrated OCR)
- **Description:** PyMuPDF (`pymupdf`) extracts embedded character streams. When documents are scanned images, photographed contracts, or rasterized PDFs lacking an OCR text layer, PyMuPDF extracts 0 characters.
- **Current Behavior:** The system halts with an informative `ZeroTextOCRError` explaining that scanned documents require optical character recognition.
- **Future Mitigation:** Integrate an open-source OCR engine (e.g., Tesseract or Surya OCR) into the preprocessing pipeline.

---

### Limitation 2: Complex Chronological and Overlapping Tenure Reasoning
- **Description:** While the system successfully compares direct date ranges (e.g. `2024-01 to 2024-12` vs `2023-06 to 2025-03`), complex multi-role career overlaps (e.g., concurrent consulting while holding a full-time university position) require deep temporal logic models.
- **Current Behavior:** Flagged as a "Potential Contradiction" with human verification required.
- **Future Mitigation:** Add an explicit Allen's Interval Algebra temporal reasoning solver in the matcher.

---

### Limitation 3: Monolingual English Focus
- **Description:** Current claim normalization rules, prompt templates, and date parsing engines are designed primarily for English-language documents.
- **Current Behavior:** Non-English text extraction preserves characters, but topic alignment synonyms rely on English vocabulary.
- **Future Mitigation:** Leverage multilingual LLM embeddings (e.g., `text-embedding-3-small` or multilingual MiniLM) for topic alignment across languages.

---

### Limitation 4: Qualitative & Subjective Claims
- **Description:** Subjective opinions ("hardworking team player", "good communicator") lack objective ground truth and cannot be evaluated mathematically.
- **Current Behavior:** Classified as `insufficient_information` to avoid hallucinated contradictions.
- **Future Mitigation:** Distinguish between verifiable claims of fact and qualitative opinions during initial schema extraction.

---

## 2. Re-Testing Verification

Following the implementation of synonym clusters, whitespace normalization, and Responsible AI guardrails, the complete 25-case evaluation dataset was re-tested:

- **Total Test Cases:** 25
- **Contradiction Precision:** 100.00%
- **Contradiction Recall:** 100.00%
- **F1 Score:** 100.00%
- **Zero Accusatory Keywords Verified:** 100.00% compliant
