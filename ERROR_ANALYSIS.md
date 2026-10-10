# ERROR_ANALYSIS.md — Failure Mode & Edge Case Deep Dive
**AI Contradiction Detector — Stage 04 Testing & Evaluation Lab**  
*Reference: PDF 05 Official Student Build Guide*

---

## 1. Methodology
To prevent over-fitting and understand where large language models and rule heuristics fail, we analyze edge cases and failure modes observed during evaluation dataset construction and pipeline stress testing.

---

## 2. In-Depth Failure Mode Investigations

### Case Study 1: Approximate Durations vs Exact Months (Potential False Positive)
- **Claim A:** *"Candidate has about 2 years of backend experience."*
- **Claim B:** *"Employment record documents 20 months of backend work."*
- **Expected Label:** Compatible (Under conversational rounding heuristics).
- **Initial Model Failure:** The baseline comparison engine flagged this as a **Contradiction** ($24 \neq 20$ months), failing to recognize that *"about 2 years"* is an approximate qualifying statement rather than an exact bounding timestamp.
- **Root Cause:** Literal string/numeric equality checks do not handle hedging expressions ("about", "approximately", "nearly").
- **Mitigation & Resolution:** Implemented qualitative boundary slack: when a claim contains an approximation qualifier ("about", "approx"), a $\pm 20\%$ margin of variance is permitted before escalating to "Potential Contradiction".

---

### Case Study 2: Scanned PDFs with Image-Only Content (Potential False Negative)
- **Document Input:** Scanned employment certificate saved inside a PDF container without an embedded OCR text stream.
- **Initial Pipeline Behavior:** PyMuPDF returned an empty string (`""`). The initial pipeline treated this as "No Contradictions Found" (zero claims extracted), resulting in a dangerous False Negative.
- **Root Cause:** Silent zero-claim propagation through the alignment and comparison steps.
- **Mitigation & Resolution:** Created `inspect_pdf()` diagnostic check in `src/pdf_reader.py` and `ZeroTextOCRError` in `src/errors.py`. If a PDF contains pages with images but 0 characters, the system halts and notifies the user:
  > *"Document contains images with 0 extractable text characters. Scanned/image-only PDFs require an OCR engine."*

---

### Case Study 3: Differing Degrees with Shared Domain (Potential False Positive)
- **Claim A:** *"Degree: Bachelor of Science in Information Technology (BS IT)"*
- **Claim B:** *"Degree: Bachelor of Science in Computer Science (BS CS)"*
- **Observed Behavior:** High fuzzy similarity in the matcher ($>80\%$) initially aligned both under `degree`. The comparison engine flagged them as a contradiction because the subject areas differed.
- **Analysis:** Is this a genuine contradiction or two distinct degrees?
- **Root Cause:** If a candidate completed *both* degrees, treating them as conflicting claims creates an incorrect false alarm.
- **Mitigation & Resolution:** Added context inspection: if both claims originate from different institutions or different graduation years, they are treated as distinct educational milestones rather than mutually exclusive claims.

---

## 3. Summary of Investigation Actions (PDF 05 Page 2)

| Symptom | Identified Cause | Implemented Action |
| :--- | :--- | :--- |
| **Over-sensitive Contradictions** | Literal value matching | Permitted numerical/format synonyms and rounding buffers |
| **Missed Contradictions** | Weak attribute normalization | Expanded synonym clusters in `matcher.py` (tenure, budget, residence) |
| **Hallucinated Evidence** | Unrestricted LLM prompt | Required exact `source_text` sentence in `Claim` Pydantic model |
| **Defamatory Language** | Unconstrained generative text | Pydantic regex validators sanitize all accusatory words |
