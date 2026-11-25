
"""
PulsePay Product Analytics
Experiment Analysis Automation Runner

Runs the existing KYC A/B test analysis
and reports whether execution completed successfully.
"""

from python.analysis.experiment_analysis import main as run_experiment_analysis


def run_experiment():

    print("\n" + "=" * 70)
    print("PULSEPAY EXPERIMENT ANALYSIS AUTOMATION")
    print("=" * 70)

    try:
        execution_success = run_experiment_analysis()

        if execution_success:
            print("\n[PASS] Experiment analysis execution completed.")
            return True

        print("\n[FAIL] Experiment analysis execution failed.")
        return False

    except Exception as error:
        print(f"\n[ERROR] Experiment runner failed: {error}")
        return False
