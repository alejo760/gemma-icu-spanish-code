"""Score original notes and gemma3:1b summaries with five Spanish indices.

The index functions come from the bundled legibilidad package
(Alejandro Muñoz Fernández, GPL-3.0).
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from legibilidad import crawford, fernandez_huerta, gutierrez, mu, szigriszt_pazos

SCORERS = {
    "fernandez_huerta": fernandez_huerta,
    "szigriszt_pazos": szigriszt_pazos,
    "gutierrez": gutierrez,
    "mu": mu,
    "crawford": crawford,
}


def score_column(frame, column, suffix):
    text = frame[column].map(lambda value: str(value) if pd.notna(value) else None)
    for name, function in SCORERS.items():
        frame[f"{name}_{suffix}"] = text.map(lambda value: function(value) if value else None)


def main():
    parser = argparse.ArgumentParser(description="Add readability columns to a spreadsheet.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--note-column", default="nota_completa")
    parser.add_argument("--summary-column", default="summary_gemma3_1b")
    args = parser.parse_args()

    frame = pd.read_excel(args.input)
    if args.note_column in frame.columns:
        score_column(frame, args.note_column, "nota")
    if args.summary_column in frame.columns:
        score_column(frame, args.summary_column, "summary")
    frame.to_excel(args.output, index=False)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
