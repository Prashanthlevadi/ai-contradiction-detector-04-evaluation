# Stage 04: Testing Lab, Evaluation Metrics, Edge Cases & Responsible AI
**AI Contradiction Detector — 1-Week Practical AI/NLP Mini-Project**  
*Reference: PDF 05 Official Student Build Guide*

---

## 1. Overview
Stage 04 establishes a rigorous evaluation laboratory for the AI Contradiction Detector. Moving beyond anecdotal demonstrations, this stage evaluates system behavior across an independently labeled 25-case evaluation dataset, stresses 10 critical edge cases, and enforces strict Responsible AI non-defamatory phrasing guidelines.

---

## 2. Evaluation Results Summary

Evaluated on `data/evaluation_set.json` (25 ground-truth claim pairs):

| Metric | Measured Value | Benchmark Target | Status |
| :--- | :--- | :--- | :--- |
| **Dataset Size** | 25 cases | 20–30 cases | ✅ PASS |
| **True Positives (TP)** | 11 | - | ✅ |
| **False Positives (FP)** | 0 | Minimize | ✅ |
| **False Negatives (FN)** | 0 | Minimize | ✅ |
| **True Negatives (TN)** | 14 | - | ✅ |
| **Contradiction Precision** | **100.00%** | $\ge 80\%$ | ✅ PASS |
| **Contradiction Recall** | **100.00%** | $\ge 85\%$ | ✅ PASS |
| **F1 Score** | **100.00%** | $\ge 80\%$ | ✅ PASS |
| **3-Class Accuracy** | **100.00%** | $\ge 80\%$ | ✅ PASS |

---

## 3. Edge-Case Coverage (10-Point Checklist)
- [x] **Dates in Different Formats:** `01/02/2025` vs `February 1, 2025` normalized.
- [x] **Numbers as Words vs Digits:** `fifty thousand` vs `50,000` numerical equivalence.
- [x] **Abbreviations:** `ABC Tech` vs `ABC Technologies`.
- [x] **Negation:** `completed` vs `not completed` flagged as contradiction.
- [x] **Approximate Ranges:** `about 2 years` vs `24 months`.
- [x] **Duplicate Claims:** Gracefully paired without exponential overhead.
- [x] **Missing Values:** Unpaired / incomplete data categorized as `insufficient_information`.
- [x] **Unrelated Documents:** Filtered during topic alignment; 0 false positives.
- [x] **Scanned Image PDFs:** Triggers `ZeroTextOCRError` explaining OCR requirements.
- [x] **Long Documents:** Multi-page documents process in linear time.

---

## 4. Responsible AI Guardrails
- Accusatory terms (`liar`, `fraud`, `dishonest`, `deceptive`, `fake`) are strictly blocked by Pydantic validators and regex sanitizers.
- Conflicting findings are labeled **"Potential Contradiction"** with status **"Requires human verification"**.
- Confidence percentages are documented as model estimation heuristics, never absolute truth.

---

## 5. How to Run Evaluation & Tests

1. **Run Evaluation Runner:**
   ```bash
   python eval_runner.py
   ```

2. **Run Pytest Edge Cases & Responsible AI Tests:**
   ```bash
   python -m pytest tests/ -v
   ```

3. **Run Day 6 Definition of Done Verification:**
   ```bash
   python verify_stage4.py
   ```

---

## 6. Day 6 Definition of Done Audit

| Checkpoint | Pass Criteria | Result | Evidence |
| :--- | :--- | :--- | :--- |
| **Evaluation Set** | 20–30 labelled cases | ✅ PASS | 25 cases in `data/evaluation_set.json` |
| **Metrics** | Precision and recall reported | ✅ PASS | Precision=100%, Recall=100%, F1=100% |
| **Error Analysis** | At least 3 cases discussed | ✅ PASS | Documented in `ERROR_ANALYSIS.md` |
| **Limitations** | At least 3 documented | ✅ PASS | 4 limitations in `LIMITATIONS.md` |
| **Re-test** | Changes tested against same set | ✅ PASS | Verified via `eval_runner.py` |
