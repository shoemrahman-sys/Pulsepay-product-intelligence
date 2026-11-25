
"""
PulsePay Product Analytics
Final Results Export Automation Runner

Connects the existing CSV exporter to the central pipeline.
"""

from python.analysis.export_final_results import main as run_export_script


def run_export():

    print("\n" + "=" * 70)
    print("PULSEPAY RESULTS EXPORT AUTOMATION")
    print("=" * 70)

    try:
        export_success = run_export_script()

        if export_success:
            print("\n[PASS] Results export completed.")
            return True

        print("\n[FAIL] Results export did not complete.")
        return False

    except Exception as error:
        print(f"\n[ERROR] Results export failed: {error}")
        return False
