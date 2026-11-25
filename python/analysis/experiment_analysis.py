"""
PulsePay Product Analytics
Experiment Analysis: KYC Flow A/B Test

Purpose:
- Pull experiment outcomes from MySQL
- Compare control vs treatment KYC completion
- Calculate absolute and relative lift
- Run a two-proportion z-test
- Calculate a 95% confidence interval
- Check sample ratio mismatch
- Produce an evidence-based experiment recommendation
"""
from math import sqrt
from scipy.stats import norm, chi2
from config.database import get_db_connection

import pandas as pd



# ============================================================
# STATISTICAL SETTINGS
# ============================================================

ALPHA = 0.05
Z_CRITICAL_95 = 1.959963984540054
EXPECTED_CONTROL_RATIO = 0.50
EXPECTED_TREATMENT_RATIO = 0.50

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def two_sided_p_value(z_score):
    """
    Two-sided p-value from a standard normal z-score.
    Uses SciPy for numerical stability.
    """
    return 2 * norm.sf(abs(z_score))


def connect_to_mysql():
    print("=" * 70)
    print("PULSEPAY PRODUCT ANALYTICS")
    print("KYC FLOW A/B TEST — STATISTICAL ANALYSIS")
    print("=" * 70)

    connection = get_db_connection()

    print("\nConnected successfully to MySQL.")

    return connection

# ============================================================
# LOAD EXPERIMENT DATA
# ============================================================


def load_experiment_data(connection):

    query = """
    SELECT
    ea.user_id,
    ea.variant,

    -- KYC completed within 14 days
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM kyc_applications k
            WHERE k.user_id = ea.user_id
              AND k.status = 'completed'
              AND k.completed_at >= ea.assigned_at
              AND k.completed_at < DATE_ADD(
                  ea.assigned_at, INTERVAL 14 DAY
              )
        )
        THEN 1 ELSE 0
    END AS completed_kyc,

    -- Support contact within 14 days
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM support_tickets s
            WHERE s.user_id = ea.user_id
              AND s.created_at >= ea.assigned_at
              AND s.created_at < DATE_ADD(
                  ea.assigned_at, INTERVAL 14 DAY
              )
        )
        THEN 1 ELSE 0
    END AS contacted_support,

    -- Successful activation within 30 days
    CASE
        WHEN EXISTS (
            SELECT 1
            FROM events e
            WHERE e.user_id = ea.user_id
              AND e.event_name = 'first_successful_transaction'
              AND e.event_timestamp >= ea.assigned_at
              AND e.event_timestamp < DATE_ADD(
                  ea.assigned_at, INTERVAL 30 DAY
              )
        )
        THEN 1 ELSE 0
    END AS activated

FROM experiment_assignments ea

INNER JOIN experiments ex
    ON ea.experiment_id = ex.experiment_id

WHERE ea.experiment_id = 1

    -- Restrict assignments to the experiment period
    AND ea.assigned_at >= ex.start_date
    AND ea.assigned_at < DATE_ADD(
        ex.end_date, INTERVAL 1 DAY
    )

    -- Require a complete 30-day observation window
    AND ea.assigned_at <= DATE_SUB(
        CURRENT_TIMESTAMP,
        INTERVAL 30 DAY
    )

    """

    df = pd.read_sql(query, connection)

    return df



# ============================================================
# DATA QUALITY CHECKS
# ============================================================



def validate_experiment_data(df):

    print("\nValidating experiment data...")

    required_columns = [
        "user_id",
        "variant",
        "completed_kyc",
        "contacted_support",
        "activated",
    ]

    # 1. Check that data exists
    if df.empty:
        raise ValueError("Experiment dataset is empty.")

    # 2. Check required columns
    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # 3. Check missing user IDs and variants
    if df["user_id"].isnull().any():
        raise ValueError("Missing user IDs detected.")

    if df["variant"].isnull().any():
        raise ValueError("Missing experiment variants detected.")

    # 4. Standardize variant names
    df["variant"] = (
        df["variant"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    expected_variants = {"control", "treatment"}

    actual_variants = set(df["variant"].unique())

    if actual_variants != expected_variants:
        raise ValueError(
            f"Unexpected experiment variants: {actual_variants}"
        )

    # 5. Check duplicate users
    duplicate_users = df["user_id"].duplicated().sum()

    if duplicate_users > 0:
        raise ValueError(
            f"Duplicate experiment users detected: {duplicate_users}"
        )

    # 6. Validate binary outcome columns
    outcome_columns = [
        "completed_kyc",
        "contacted_support",
        "activated",
    ]

    for column in outcome_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        if df[column].isnull().any():
            raise ValueError(
                f"Invalid or missing values in {column}."
            )

        if not df[column].isin([0, 1]).all():
            raise ValueError(
                f"{column} must contain only 0 and 1."
            )

        df[column] = df[column].astype(int)

    print("[PASS] Experiment data validation completed.")
    print(f"[INFO] Total assigned users: {len(df):,}")
    print("[INFO] Both control and treatment groups are present.")



# ============================================================
# EXPERIMENT SCORECARD
# ============================================================

def create_scorecard(df):
    """
    Build descriptive metrics for each experiment variant.
    """

    scorecard = (
        df.groupby("variant")
        .agg(
    assigned_users=("user_id", "nunique"),
    completed_kyc_users=("completed_kyc", "sum"),
    support_contact_users=("contacted_support", "sum"),
    activated_users=("activated", "sum"),
    kyc_completion_rate=("completed_kyc", "mean"),
    support_contact_rate=("contacted_support", "mean"),
    activation_rate=("activated", "mean"),
)
        .reset_index()
    )

    return scorecard


def print_scorecard(scorecard):
    """
    Print a readable experiment scorecard.
    """

    display_df = scorecard.copy()

    display_df["kyc_completion_rate"] = (
        display_df["kyc_completion_rate"] * 100
    ).round(2)

    display_df["support_contact_rate"] = (
        display_df["support_contact_rate"] * 100
    ).round(2)

    display_df["activation_rate"] = (
        display_df["activation_rate"] * 100
    ).round(2)

    display_df = display_df.rename(
        columns={
            "kyc_completion_rate": "kyc_completion_rate_pct",
            "support_contact_rate": "support_contact_rate_pct",
            "activation_rate": "activation_rate_pct",
        }
    )

    print("\n" + "=" * 70)
    print("2. EXPERIMENT SCORECARD")
    print("=" * 70)

    print(
        "\n"
        + display_df.to_string(
            index=False
        )
    )


# ============================================================
# SAMPLE RATIO MISMATCH CHECK
# ============================================================


def sample_ratio_mismatch_test(scorecard):
    """
    Chi-square goodness-of-fit test for the expected
    experiment allocation ratio.
    """

    counts = dict(
        zip(
            scorecard["variant"],
            scorecard["assigned_users"],
        )
    )

    control_n = counts["control"]
    treatment_n = counts["treatment"]

    total_n = control_n + treatment_n

    expected_control = (
        total_n * EXPECTED_CONTROL_RATIO
    )

    expected_treatment = (
        total_n * EXPECTED_TREATMENT_RATIO
    )

    chi_square = (
        (control_n - expected_control) ** 2
        / expected_control
    ) + (
        (treatment_n - expected_treatment) ** 2
        / expected_treatment
    )

    p_value = chi2.sf(chi_square, df=1)

    print("\n" + "=" * 70)
    print("3. SAMPLE RATIO MISMATCH CHECK")
    print("=" * 70)

    print(f"\nControl users:   {control_n:,}")
    print(f"Treatment users: {treatment_n:,}")

    print(
        f"Expected split:  "
        f"{EXPECTED_CONTROL_RATIO:.0%} / "
        f"{EXPECTED_TREATMENT_RATIO:.0%}"
    )

    print(f"Chi-square:      {chi_square:.4f}")
    print(f"P-value:         {p_value:.6f}")

    if p_value < ALPHA:
        print(
            "\nResult: WARNING — statistically significant "
            "sample ratio mismatch detected."
        )
        print(
            "Investigate assignment, filtering, and data "
            "collection before interpreting experiment results."
        )
    else:
        print(
            "\nResult: PASSED — no statistically significant "
            "sample ratio mismatch detected."
        )

    return p_value



# ============================================================
# TWO-PROPORTION Z-TEST
# ============================================================

def analyze_primary_metric(scorecard):
    """
    Compare treatment and control KYC completion rates.
    """

    metrics = scorecard.set_index("variant")

    control_n = int(
        metrics.loc[
            "control",
            "assigned_users",
        ]
    )

    treatment_n = int(
        metrics.loc[
            "treatment",
            "assigned_users",
        ]
    )

    control_successes = int(
        metrics.loc[
            "control",
            "completed_kyc_users",
        ]
    )

    treatment_successes = int(
        metrics.loc[
            "treatment",
            "completed_kyc_users",
        ]
    )

    control_rate = (
        control_successes / control_n
    )

    treatment_rate = (
        treatment_successes / treatment_n
    )

    absolute_lift = (
        treatment_rate - control_rate
    )

    if control_rate != 0:
        relative_lift = (
            absolute_lift / control_rate
        )
    else:
        relative_lift = float("nan")

    pooled_rate = (
        control_successes
        + treatment_successes
    ) / (
        control_n
        + treatment_n
    )

    pooled_standard_error = sqrt(
        pooled_rate
        *
        (1 - pooled_rate)
        *
        (
            (1 / control_n)
            +
            (1 / treatment_n)
        )
    )

    if pooled_standard_error == 0:
        z_score = 0
        p_value = 1
    else:
        z_score = (
            absolute_lift
            /
            pooled_standard_error
        )

        p_value = two_sided_p_value(
            z_score
        )

    # Unpooled standard error for confidence interval
    ci_standard_error = sqrt(

        (
            control_rate
            *
            (1 - control_rate)
            /
            control_n
        )

        +

        (
            treatment_rate
            *
            (1 - treatment_rate)
            /
            treatment_n
        )
    )

    ci_lower = (
        absolute_lift
        -
        Z_CRITICAL_95
        *
        ci_standard_error
    )

    ci_upper = (
        absolute_lift
        +
        Z_CRITICAL_95
        *
        ci_standard_error
    )

    print("\n" + "=" * 70)
    print("4. PRIMARY METRIC ANALYSIS")
    print("=" * 70)

    print(
        f"\nControl completion rate:   "
        f"{control_rate * 100:.2f}%"
    )

    print(
        f"Treatment completion rate: "
        f"{treatment_rate * 100:.2f}%"
    )

    print(
        f"\nAbsolute lift: "
        f"{absolute_lift * 100:.2f} percentage points"
    )

    print(
        f"Relative lift: "
        f"{relative_lift * 100:.2f}%"
    )

    print(
        f"\nZ-score: {z_score:.4f}"
    )

    print(
        f"P-value: {p_value:.6f}"
    )

    print(
        "\n95% confidence interval for "
        "treatment - control:"
    )

    print(
        f"[{ci_lower * 100:.2f}, "
        f"{ci_upper * 100:.2f}] percentage points"
    )

    significant = (
        p_value < ALPHA
    )

    return {
        "control_rate": control_rate,
        "treatment_rate": treatment_rate,
        "absolute_lift": absolute_lift,
        "relative_lift": relative_lift,
        "z_score": z_score,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "significant": significant,
    }


# ============================================================
# EXPERIMENT DECISION
# ============================================================


def print_recommendation(scorecard, results, srm_p_value):

    control = scorecard.loc[
        scorecard["variant"] == "control"
    ].iloc[0]

    treatment = scorecard.loc[
        scorecard["variant"] == "treatment"
    ].iloc[0]

    control_support = control["support_contact_rate"]
    treatment_support = treatment["support_contact_rate"]

    control_activation = control["activation_rate"]
    treatment_activation = treatment["activation_rate"]

    p_value = results["p_value"]
    lift = results["absolute_lift"]

    print("\n" + "=" * 60)
    print("BUSINESS RECOMMENDATION")
    print("=" * 60)

    # Check experiment assignment integrity
    if srm_p_value < ALPHA:
        print("WARNING: Sample ratio mismatch detected.")
        print("Investigate assignment imbalance before")
        print("making a rollout decision.")
        return

    # Check primary metric
    if p_value >= ALPHA:
        print("KYC improvement is not statistically significant.")
        print("Do not claim that treatment improved KYC completion.")
        print("Do not roll out based on this experiment alone.")
        return

    if lift <= 0:
        print("Treatment did not improve KYC completion.")
        print("Do not roll out the treatment.")
        return

    print("Treatment significantly improved KYC completion.")

    # Check support guardrail
    if treatment_support > control_support:
        print("\nWARNING: Support contact rate increased.")
        print("Investigate the increase before rollout.")
        return

    # Check activation guardrail
    if treatment_activation < control_activation:
        print("\nWARNING: Successful activation rate decreased.")
        print("Investigate downstream activation before rollout.")
        return

    print("\nNo deterioration observed in the measured guardrails.")
    print("Treatment is a candidate for controlled rollout.")
    print("Continue monitoring KYC, support and activation.")


# ============================================================
# MAIN
# ============================================================

def main():

    connection = None

    try:

        connection = get_db_connection()

        df = load_experiment_data(
            connection
        )

        validate_experiment_data(
            df
        )

        scorecard = create_scorecard(
            df
        )

        print_scorecard(
            scorecard
        )

        srm_p_value = sample_ratio_mismatch_test(scorecard)

        results = analyze_primary_metric(
            scorecard
        )

        print_recommendation(
    scorecard,
    results,
    srm_p_value
)

        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)

        return True

    except Exception as error:

        print(
            f"\nERROR: {error}"
        )

        return False

    finally:

        if (
            connection is not None
            and connection.is_connected()
        ):

            connection.close()

            print(
                "\nMySQL connection closed."
            )


if __name__ == "__main__":
    main()