"""Build one anonymized note per sampled patient.

Identifier columns are removed from the note text by fuzzy matching and are
not written to the output. Supply your own spreadsheet. Do not commit it.
"""

import argparse
import re

import pandas as pd
from fuzzywuzzy import fuzz

SENSITIVE_COLUMNS = [
    "vPApellido",
    "vSApellido",
    "vPNombre",
    "vSNombre",
    "TipoDocumento",
    "vIdentificacion",
]
NOTE_PARTS = [
    "Subjetivo",
    "Objetivo",
    "Analisis",
    "Plan",
    "Justificacion de la estancia",
]
THRESHOLD = 90
REDACTION = " "


def anonymize_text_fuzzy(row):
    """Replace tokens that closely match a name or identifier on the same row."""
    text = row["nota_completa"]
    if not isinstance(text, str):
        return text
    sensitive_values = set()
    for column in SENSITIVE_COLUMNS:
        value = row.get(column)
        if pd.notna(value):
            value_text = str(value).lower()
            sensitive_values.add(value_text)
            if " " in value_text:
                sensitive_values.update(value_text.split())
    sensitive_values = {word for word in sensitive_values if len(word) > 2}
    if not sensitive_values:
        return text
    anonymized = []
    for token in text.split():
        cleaned = re.sub(r"^[^\w]+|[^\w]+$", "", token).lower()
        if not cleaned:
            anonymized.append(token)
            continue
        if any(fuzz.ratio(sensitive, cleaned) >= THRESHOLD for sensitive in sensitive_values):
            anonymized.append(REDACTION)
        else:
            anonymized.append(token)
    return " ".join(anonymized)


def select_notes(frame, n_patients=100, random_state=42):
    """Keep one random note from each of n_patients randomly chosen patients."""
    patient_ids = frame["vIdentificacion"].dropna().unique()
    n_samples = min(n_patients, len(patient_ids))
    sampled_ids = pd.Series(patient_ids).sample(n=n_samples, random_state=random_state)
    selected_ids = []
    for patient_id in sampled_ids:
        notes = frame.loc[frame["vIdentificacion"] == patient_id, "NotaEvolucionId"]
        selected_ids.append(notes.sample(n=1, random_state=random_state).iloc[0])
    selected = frame[frame["NotaEvolucionId"].isin(selected_ids)].copy()
    keep = [column for column in selected.columns if column not in SENSITIVE_COLUMNS]
    return selected[keep]


def main():
    parser = argparse.ArgumentParser(description="Concatenate, anonymize, and sample ICU notes.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--n", type=int, default=100)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    frame = pd.read_excel(args.input)
    intensivist = frame["DescripcionEspecialidad"].astype(str).str.contains("Intensivista", na=False)
    notes = frame.loc[intensivist].copy()
    notes["nota_completa"] = notes[NOTE_PARTS].fillna("").agg(" ".join, axis=1)
    notes["nota_completa"] = notes.apply(anonymize_text_fuzzy, axis=1)
    selected = select_notes(notes, n_patients=args.n, random_state=args.seed)
    selected.to_excel(args.output, index=False)
    print(f"Wrote {len(selected)} notes to {args.output}")


if __name__ == "__main__":
    main()
