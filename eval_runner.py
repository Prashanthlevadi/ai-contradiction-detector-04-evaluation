"""Automated Evaluation Runner Module.

Executes system against the independently labeled 25-item evaluation dataset,
computes TP, FP, FN, TN, Precision, Recall, F1 score, and multi-class accuracy
according to PDF 05 specifications.
"""

import sys
import os
import json
from typing import Dict, Any, List

EVAL_DIR = os.path.dirname(os.path.abspath(__file__))
if EVAL_DIR not in sys.path:
    sys.path.insert(0, EVAL_DIR)

from src.claims import Claim
from src.comparator import compare_claims_rule_based, ComparisonResult


def run_evaluation(dataset_path: str = None) -> Dict[str, Any]:
    if dataset_path is None:
        dataset_path = os.path.join(EVAL_DIR, "data", "evaluation_set.json")

    with open(dataset_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    total_cases = len(cases)
    tp = 0  # Predicted Contradiction, Ground Truth Contradiction
    fp = 0  # Predicted Contradiction, Ground Truth Non-contradiction
    fn = 0  # Predicted Non-contradiction, Ground Truth Contradiction
    tn = 0  # Predicted Non-contradiction, Ground Truth Non-contradiction
    exact_matches = 0

    detailed_results: List[Dict[str, Any]] = []

    for c in cases:
        case_id = c["id"]
        expected = c["expected"]
        topic = c["topic"]

        claim_a = Claim(
            claim_id=f"{case_id}-A",
            subject=c["claim_a"]["subject"],
            attribute=c["claim_a"]["attribute"],
            value=c["claim_a"]["value"],
            source_text=c["claim_a"]["source_text"],
            source=c["claim_a"]["source"]
        )
        claim_b = Claim(
            claim_id=f"{case_id}-B",
            subject=c["claim_b"]["subject"],
            attribute=c["claim_b"]["attribute"],
            value=c["claim_b"]["value"],
            source_text=c["claim_b"]["source_text"],
            source=c["claim_b"]["source"]
        )

        pred = compare_claims_rule_based(claim_a, claim_b, topic=topic)
        pred_label = pred.classification

        is_exact = (pred_label == expected)
        if is_exact:
            exact_matches += 1

        # Contradiction binary metrics
        is_pred_contra = (pred_label == "contradiction")
        is_true_contra = (expected == "contradiction")

        if is_pred_contra and is_true_contra:
            tp += 1
            status = "TP"
        elif is_pred_contra and not is_true_contra:
            fp += 1
            status = "FP"
        elif not is_pred_contra and is_true_contra:
            fn += 1
            status = "FN"
        else:
            tn += 1
            status = "TN"

        detailed_results.append({
            "id": case_id,
            "topic": topic,
            "expected": expected,
            "predicted": pred_label,
            "confidence": pred.confidence,
            "metric_status": status,
            "reason": pred.reason
        })

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    accuracy = exact_matches / total_cases if total_cases > 0 else 0.0

    metrics = {
        "total_cases": total_cases,
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
        "true_negatives": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "multi_class_accuracy": round(accuracy, 4),
        "detailed_results": detailed_results
    }
    return metrics


def print_evaluation_report(metrics: Dict[str, Any]):
    print("=" * 65)
    print("AI CONTRADICTION DETECTOR — EVALUATION LAB RESULTS (PDF 05)")
    print("=" * 65)
    print(f"Dataset Size:           {metrics['total_cases']} independently labeled pairs")
    print(f"True Positives (TP):    {metrics['true_positives']}")
    print(f"False Positives (FP):   {metrics['false_positives']}")
    print(f"False Negatives (FN):   {metrics['false_negatives']}")
    print(f"True Negatives (TN):    {metrics['true_negatives']}")
    print("-" * 65)
    print(f"Contradiction Precision: {metrics['precision'] * 100:.2f}%")
    print(f"Contradiction Recall:    {metrics['recall'] * 100:.2f}%")
    print(f"F1 Score:                {metrics['f1_score'] * 100:.2f}%")
    print(f"3-Class Exact Accuracy:  {metrics['multi_class_accuracy'] * 100:.2f}%")
    print("=" * 65)

    print("\nSample Case Evaluations:")
    for r in metrics["detailed_results"][:6]:
        print(f"  [{r['id']}] Topic: {r['topic']:<18} | Exp: {r['expected']:<14} | Pred: {r['predicted']:<14} | Status: {r['metric_status']}")


if __name__ == "__main__":
    m = run_evaluation()
    print_evaluation_report(m)
