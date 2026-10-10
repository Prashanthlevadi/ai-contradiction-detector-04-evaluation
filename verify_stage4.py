"""Stage 4 Standalone Verification Script.

Audits Day 6 Definition of Done from PDF 05 Page 3:
1. Evaluation set: 20-30 labeled cases verified.
2. Metrics: Precision and recall computed and reported.
3. Error analysis: At least 3 error examples documented.
4. Limitations: At least 3 system limitations documented.
5. Re-test: Executed against the evaluation set.
"""

import os
import sys

def run_verification():
    print("=" * 60)
    print("STAGE 04 — DEFINITION OF DONE VERIFICATION")
    print("=" * 60)

    from eval_runner import run_evaluation

    # 1. Evaluation set check
    print("[1/5] Checking mini evaluation dataset...")
    data_path = os.path.join(os.path.dirname(__file__), "data", "evaluation_set.json")
    assert os.path.exists(data_path), "evaluation_set.json must exist"
    metrics = run_evaluation(data_path)
    count = metrics["total_cases"]
    assert 20 <= count <= 30, f"Evaluation set must have 20-30 cases, found {count}"
    print(f"  - Dataset size: {count} cases (Target: 20-30) (OK)")

    # 2. Precision & Recall reporting
    print("\n[2/5] Verifying precision & recall calculation...")
    p = metrics["precision"]
    r = metrics["recall"]
    f1 = metrics["f1_score"]
    assert p > 0.0 and r > 0.0, "Precision and recall must be greater than 0"
    print(f"  - Precision: {p * 100:.2f}%")
    print(f"  - Recall:    {r * 100:.2f}%")
    print(f"  - F1 Score:  {f1 * 100:.2f}% (OK)")

    # 3. Error analysis documentation check
    print("\n[3/5] Checking error analysis documentation...")
    err_path = os.path.join(os.path.dirname(__file__), "ERROR_ANALYSIS.md")
    assert os.path.exists(err_path), "ERROR_ANALYSIS.md must exist"
    with open(err_path, "r", encoding="utf-8") as f:
        err_txt = f.read()
    assert "Case Study 1" in err_txt
    assert "Case Study 2" in err_txt
    assert "Case Study 3" in err_txt
    print("  - At least 3 detailed error case studies documented (OK)")

    # 4. Limitations documentation check
    print("\n[4/5] Checking documented system limitations...")
    lim_path = os.path.join(os.path.dirname(__file__), "LIMITATIONS.md")
    assert os.path.exists(lim_path), "LIMITATIONS.md must exist"
    with open(lim_path, "r", encoding="utf-8") as f:
        lim_txt = f.read()
    assert "Limitation 1" in lim_txt
    assert "Limitation 2" in lim_txt
    assert "Limitation 3" in lim_txt
    print("  - At least 3 limitations documented (OK)")

    # 5. Re-test execution
    print("\n[5/5] Re-testing against evaluation dataset...")
    retest_metrics = run_evaluation(data_path)
    assert retest_metrics["precision"] >= 0.80, "Re-test precision must exceed 80%"
    assert retest_metrics["recall"] >= 0.80, "Re-test recall must exceed 80%"
    print(f"  - Re-test successful: Precision={retest_metrics['precision']*100:.1f}%, Recall={retest_metrics['recall']*100:.1f}% (OK)")

    print("\n" + "=" * 60)
    print("ALL 5 DAY 6 DEFINITION OF DONE CHECKPOINTS PASSED!")
    print("=" * 60)

if __name__ == "__main__":
    run_verification()
