
"""
PulsePay Product Analytics
Central Automation Pipeline

Coordinates the existing analytics workflow.
Does not generate or reload synthetic data.
"""
from automation.database_validation import validate_database
from automation.sql_runner import run_sql_analysis
from automation.experiment_runner import run_experiment
from automation.export_runner import run_export
from automation.ai_input_runner import run_ai_input_preparation
from automation.report_runner import run_report_generation
from pathlib import Path


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SQL_DIR = PROJECT_ROOT / "sql"
PYTHON_DIR = PROJECT_ROOT / "python"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "final_results"


# ============================================================
# PIPELINE CONFIGURATION
# ============================================================

PIPELINE_NAME = "PulsePay Product Analytics Automation"

PIPELINE_STAGES = [
    "database_validation",
    "sql_analysis",
    "experiment_analysis",
    "results_export",
    "ai_input_preparation",
    "report_generation",
]

# ============================================================
# PIPELINE STATUS
# ============================================================

pipeline_status = {
    stage: "PENDING"
    for stage in PIPELINE_STAGES
}


# ============================================================
# DISPLAY PIPELINE INFORMATION
# ============================================================

def display_pipeline():

    print("=" * 70)
    print(PIPELINE_NAME)
    print("=" * 70)

    print("\nPlanned pipeline stages:\n")

    for number, stage in enumerate(
        PIPELINE_STAGES,
        start=1
    ):

        print(f"{number}. {stage.replace('_', ' ').title()}")

    print("\nPipeline structure initialized.")

def display_pipeline_status():

    print("\n" + "=" * 70)
    print("PULSEPAY PIPELINE EXECUTION SUMMARY")
    print("=" * 70)

    for stage, status in pipeline_status.items():

        print(
            f"{stage.replace('_', ' ').title():35} "
            f"{status}"
        )

    print("=" * 70)


# ============================================================
# DATABASE VALIDATION STAGE
# ============================================================

def run_database_validation():

    print("\nStarting database validation...")

    pipeline_status["database_validation"] = "RUNNING"

    validation_success = validate_database()

    if validation_success:

        pipeline_status["database_validation"] = "SUCCESS"

        print("\nDatabase validation stage completed.")

    else:

        pipeline_status["database_validation"] = "FAILED"

        print("\nDatabase validation stage failed.")

    return validation_success

# ============================================================
# STAGE 2: DASHBOARD SQL AUTOMATION
# ============================================================

def run_dashboard_sql():

    print("\nStarting dashboard SQL automation...")

    pipeline_status["sql_analysis"] = "RUNNING"

    sql_success = run_sql_analysis()

    if sql_success:

        pipeline_status["sql_analysis"] = "SUCCESS"

        print("\nDashboard SQL stage completed.")

    else:

        pipeline_status["sql_analysis"] = "FAILED"

        print("\nDashboard SQL stage failed.")

    return sql_success


def run_experiment_stage():
    print("\nStarting experiment analysis...")
    pipeline_status["experiment_analysis"] = "RUNNING"

    experiment_success = run_experiment()

    if experiment_success:
        pipeline_status["experiment_analysis"] = "SUCCESS"
        print("\nExperiment analysis stage completed.")
    else:
        pipeline_status["experiment_analysis"] = "FAILED"
        print("\nExperiment analysis stage failed.")

    return experiment_success

def run_results_export():

    print("\nStarting final results export...")

    pipeline_status["results_export"] = "RUNNING"

    export_success = run_export()

    if export_success:
        pipeline_status["results_export"] = "SUCCESS"
        print("\nFinal results export stage completed.")
    else:
        pipeline_status["results_export"] = "FAILED"
        print("\nFinal results export stage failed.")

    return export_success

def run_ai_input_stage():

    print("\nStarting AI evidence preparation...")

    pipeline_status["ai_input_preparation"] = "RUNNING"

    preparation_success = run_ai_input_preparation()

    if preparation_success:
        pipeline_status["ai_input_preparation"] = "SUCCESS"
        print("\nAI evidence preparation stage completed.")
    else:
        pipeline_status["ai_input_preparation"] = "FAILED"
        print("\nAI evidence preparation stage failed.")

    return preparation_success

def run_report_stage():

    print("\nStarting business report generation...")

    pipeline_status["report_generation"] = "RUNNING"

    report_success = run_report_generation()

    if report_success:
        pipeline_status["report_generation"] = "SUCCESS"
        print("\nBusiness report stage completed.")
    else:
        pipeline_status["report_generation"] = "FAILED"
        print("\nBusiness report stage failed.")

    return report_success



# ============================================================
# INITIAL PIPELINE ORCHESTRATION
# ============================================================


def run_initial_stages():

    print("\nStarting initial pipeline stages...")

    if not run_database_validation():
        print("\n[STOP] Database validation failed.")
        return False

    if not run_dashboard_sql():
        print("\n[STOP] Dashboard SQL execution failed.")
        return False

    if not run_experiment_stage():
        print("\n[STOP] Experiment analysis failed.")
        return False

    if not run_results_export():
        print("\n[STOP] Results export failed.")
        return False

    if not run_ai_input_stage():
        print("\n[STOP] AI evidence preparation failed.")
        return False

    print("\n[INFO] Evidence package is ready for business interpretation.")
    print("[INFO] Report generation will be enabled after findings validation.")

    print("\n" + "=" * 70)
    print("[PASS] AUTOMATED DATA PREPARATION COMPLETED")
    print("=" * 70)

    return True