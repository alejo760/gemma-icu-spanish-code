"""Compare paired readability scores for original notes and summaries.

Expects an Excel file that already has columns named
{index}_nota and {index}_summary for each index. The file itself is not
included in this repository.
"""

import argparse

import numpy as np
import pandas as pd
from scipy import stats

INDICES = ["fernandez_huerta", "szigriszt_pazos", "gutierrez", "mu", "crawford"]


def compare(frame, alpha=0.05):
    rows = []
    for index_name in INDICES:
        note_column = f"{index_name}_nota"
        summary_column = f"{index_name}_summary"
        if note_column not in frame.columns or summary_column not in frame.columns:
            continue
        paired = frame[[note_column, summary_column]].dropna()
        note = paired[note_column]
        summary = paired[summary_column]
        differences = note - summary
        n_pairs = len(paired)
        if n_pairs < 8:
            rows.append({"index": index_name, "n_pairs": n_pairs, "test": "not run"})
            continue
        if n_pairs < 50:
            normality_name = "Shapiro-Wilk"
            _, normality_p = stats.shapiro(differences)
        else:
            normality_name = "D'Agostino-Pearson"
            _, normality_p = stats.normaltest(differences)
        if normality_p > alpha:
            test_name = "paired t-test"
            statistic, p_value = stats.ttest_rel(note, summary)
        elif (differences == 0).all():
            test_name = "Wilcoxon signed-rank"
            statistic, p_value = np.nan, np.nan
        else:
            test_name = "Wilcoxon signed-rank"
            statistic, p_value = stats.wilcoxon(note, summary)
        rows.append({
            "index": index_name,
            "n_pairs": n_pairs,
            "normality_test": normality_name,
            "normality_p": normality_p,
            "test": test_name,
            "statistic": statistic,
            "p_value": p_value,
            "significant": bool(p_value < alpha) if pd.notna(p_value) else None,
            "mean_original": note.mean(),
            "mean_summary": summary.mean(),
            "median_original": note.median(),
            "median_summary": summary.median(),
        })
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser(description="Paired readability comparison.")
    parser.add_argument("--input", required=True, help="Excel file with score columns. Not stored in this repository.")
    parser.add_argument("--output", help="Optional Excel path for the comparison table.")
    args = parser.parse_args()
    result = compare(pd.read_excel(args.input))
    print(result.to_string(index=False))
    if args.output:
        result.to_excel(args.output, index=False)


if __name__ == "__main__":
    main()
