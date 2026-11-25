
"""
PulsePay Product Analytics
Main Automation Entry Point

Starts the central analytics automation pipeline.
"""

from automation.pipeline import (
    display_pipeline,
    run_initial_stages,
    display_pipeline_status,
)


def main():

    print("\n" + "=" * 70)
    print("PULSEPAY PRODUCT ANALYTICS")
    print("END-TO-END AUTOMATION")
    print("=" * 70)

    display_pipeline()

    try:

        pipeline_success = run_initial_stages()

        if pipeline_success:
            print("\n[SUCCESS] Automated data preparation completed.")
        else:
            print("\n[FAILED] Automation stopped before completion.")

    except Exception as error:

        print(f"\n[ERROR] Unexpected pipeline error: {error}")

    finally:

        display_pipeline_status()

        print("\nPulsePay automation process finished.")


if __name__ == "__main__":
    main()
