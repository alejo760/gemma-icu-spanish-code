# gemma3:1b ICU note simplification

Code for the local summarization and Spanish readability comparison described in the manuscript. Clinical notes, identifiers, and result spreadsheets are not in this repository.

## Prompt

Summaries were requested from `gemma3:1b` through the Ollama chat API. The call used a single user message and no system message. The message is stored in `PROMPT.txt`:

```
Resuma las siguientes notas clínicas para garantizar que el resumen pueda ser comprendido por pacientes sin conocimientos médicos. Utilice un lenguaje sencillo y evite la jerga médica.
    Notas Clínicas: {note}
```

`{note}` is the anonymized progress note. The four spaces before `Notas Clínicas:` are part of the string that was sent.

## Scripts

Run these against a spreadsheet you keep outside the repository.

1. `prepare_notes.py` keeps intensivist notes, joins the subjective, objective, analysis, plan, and stay-justification fields, redacts identifier tokens, and draws one note from each of 100 patients (`random_state=42`).
2. `summarize.py` calls `gemma3:1b` with the prompt above. Pull the model first with `ollama pull gemma3:1b`.
3. `add_readability.py` scores the note and the summary with Fernández-Huerta, Szigriszt-Pazos, Gutiérrez de Polini, Mu, and Crawford.
4. `compare_readability.py` tests paired differences with Shapiro-Wilk or D'Agostino-Pearson, then a paired t-test or Wilcoxon signed-rank test.

```bash
python prepare_notes.py --input notes.xlsx --output sample.xlsx
python summarize.py --input sample.xlsx --output summaries.xlsx
python add_readability.py --input summaries.xlsx --output scores.xlsx
python compare_readability.py --input scores.xlsx
```

## Readability package

`legibilidad/` is the Spanish readability library by Alejandro Muñoz Fernández, included under GPL-3.0. Upstream: https://github.com/alejandromunozes/legibilidad
