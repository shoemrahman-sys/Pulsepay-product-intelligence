
"""
PulsePay Product Analytics
AI Evidence Preparation

Collects existing analytical CSV outputs and project
documentation into a structured package for ChatGPT.

Does not modify the source data or analytical results.
Does not require an AI API.
"""

import json
from pathlib import Path
from datetime import datetime

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RESULTS_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "final_results"
)

DOCS_DIR = PROJECT_ROOT / "docs"

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "ai_input"
)

DOCUMENT_FILES = [
    "project_charter.md",
    "data-dictionary.md",
    "metric_dictionary.md",
    "methodology.md",
    "case-study.md",
]


def collect_csv_evidence():

    evidence = {}

    if not RESULTS_DIR.exists():
        raise FileNotFoundError(
            f"Results directory not found: {RESULTS_DIR}"
        )

    csv_files = sorted(RESULTS_DIR.glob("*.csv"))

    if not csv_files:
        raise FileNotFoundError(
            "No analytical CSV files were found."
        )

    for csv_file in csv_files:

        if csv_file.name == "export_manifest.csv":
            continue

        df = pd.read_csv(csv_file)

        evidence[csv_file.stem] = {
            "filename": csv_file.name,
            "row_count": len(df),
            "columns": df.columns.tolist(),
            "missing_values": (
                df.isnull().sum().to_dict()
            ),
            "numeric_summary": (
                df.describe(include="all")
                .fillna("")
                .to_dict()
            ),
            "sample_records": (
                df.head(20)
                .fillna("")
                .to_dict(orient="records")
            ),
        }

    return evidence


def collect_project_documentation():

    documentation = {}

    for filename in DOCUMENT_FILES:

        file_path = DOCS_DIR / filename

        if file_path.exists():

            documentation[filename] = (
                file_path.read_text(encoding="utf-8")
            )

    return documentation


def build_evidence_package():

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    package = {
        "project": "PulsePay Product Analytics",
        "generated_at": datetime.now().isoformat(),
        "purpose": (
            "Prepare existing analytical evidence "
            "for business interpretation."
        ),
        "data": collect_csv_evidence(),
        "documentation": (
            collect_project_documentation()
        ),
    }

    output_file = (
        OUTPUT_DIR / "pulsepay_ai_evidence.json"
    )

    with output_file.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            package,
            file,
            indent=4,
            default=str
        )

    print("\n[PASS] AI evidence package created.")
    print(f"[INFO] Output: {output_file}")

    return True
