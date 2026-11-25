
"""
PulsePay Product Analytics
Report Generation Runner

Connects the DOCX and PDF report generator
to the central automation pipeline.
"""

from automation.report_generator import generate_report


def run_report_generation():

    print("\n" + "=" * 70)
    print("PULSEPAY BUSINESS REPORT GENERATION")
    print("=" * 70)

    try:
        report_success = generate_report()

        if report_success:
            print("\n[PASS] Report generation completed.")
            return True

        print("\n[FAIL] Report generation failed.")
        return False

    except Exception as error:
        print(f"\n[ERROR] Report generation failed: {error}")
        return False
