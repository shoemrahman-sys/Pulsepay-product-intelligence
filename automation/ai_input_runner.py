
"""
PulsePay Product Analytics
AI Evidence Preparation Runner

Connects the evidence builder to the central pipeline.
"""

from automation.ai_input_builder import (
    build_evidence_package
)


def run_ai_input_preparation():

    print("\n" + "=" * 70)
    print("PULSEPAY AI EVIDENCE PREPARATION")
    print("=" * 70)

    try:
        preparation_success = build_evidence_package()

        if preparation_success:
            print("\n[PASS] AI evidence preparation completed.")
            return True

        print("\n[FAIL] AI evidence preparation failed.")
        return False

    except Exception as error:
        print(f"\n[ERROR] AI evidence preparation failed: {error}")
        return False
