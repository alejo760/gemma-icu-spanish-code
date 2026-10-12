"""Generate plain-language summaries with a local gemma3:1b model.

The instruction sent to the model is the text in PROMPT.txt. The clinical
note is inserted after the label "Notas Clínicas:". No note text is stored
in this repository.
"""

import argparse
import time

import pandas as pd
from tqdm import tqdm

PROMPT_TEMPLATE = """Resuma las siguientes notas clínicas para garantizar que el resumen pueda ser comprendido por pacientes sin conocimientos médicos. Utilice un lenguaje sencillo y evite la jerga médica.
    Notas Clínicas: {note}
"""


def format_input(note):
    """Build the user message that was sent to gemma3:1b."""
    return PROMPT_TEMPLATE.format(note=note)


def generate_summary(note, model_name, client):
    """Return a summary, or an empty string when the note is missing."""
    if pd.isna(note) or not isinstance(note, str) or not note.strip():
        return ""
    response = client.chat(
        model=model_name,
        messages=[{"role": "user", "content": format_input(note)}],
    )
    time.sleep(0.1)
    return response["message"]["content"]


def main():
    parser = argparse.ArgumentParser(description="Summarize a column of clinical notes with Ollama.")
    parser.add_argument("--input", required=True, help="Excel file with a text column. This file is not part of the repository.")
    parser.add_argument("--column", default="nota_completa", help="Column that holds the note text.")
    parser.add_argument("--model", default="gemma3:1b")
    parser.add_argument("--output", required=True, help="Excel file to write. Do not commit this file.")
    args = parser.parse_args()

    import ollama

    frame = pd.read_excel(args.input)
    column_name = f"summary_{args.model.replace(':', '_').replace('-', '_')}"
    summaries = []
    for note in tqdm(frame[args.column], desc=args.model):
        try:
            summaries.append(generate_summary(note, args.model, ollama))
        except Exception as error:
            summaries.append(f"Error: {error}")
    frame[column_name] = summaries
    frame.to_excel(args.output, index=False)
    print(f"Wrote {len(frame)} rows to {args.output}")


if __name__ == "__main__":
    main()
