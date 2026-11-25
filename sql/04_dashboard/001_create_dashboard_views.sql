USE pulsepay_analytics;

-- ============================================================
-- PULSEPAY PRODUCT ANALYTICS
-- DASHBOARD DATA LAYER
-- ============================================================
--
-- Purpose:
-- Create reusable MySQL views for the PulsePay executive
-- product analytics dashboard.
--
-- Dashboard Pages:
-- 1. Executive Overview
-- 2. Funnel & Activation
-- 3. Retention & Cohorts
-- 4. Root-Cause Investigation
-- 5. Acquisition Quality
-- 6. Experiment Results
--
-- ============================================================


-- ============================================================
-- VIEW 1: EXECUTIVE KPI SUMMARY
-- ============================================================

CREATE OR REPLACE VIEW vw_executive_kpis AS

SELECT

    (SELECT COUNT(*)
     FROM users) AS total_users,

    (SELECT COUNT(*)
     FROM transactions) AS total_transactions,

    (SELECT COUNT(*)
     FROM transactions
     WHERE status = 'success') AS successful_transactions,

    ROUND(
        100.0 *
        (
            SELECT COUNT(*)
            FROM transactions
            WHERE status = 'success'
        )
        /
        NULLIF(
            (
                SELECT COUNT(*)
                FROM transactions
            ),
            0
        ),
        2
    ) AS transaction_success_rate_pct,

    (
        SELECT COUNT(DISTINCT user_id)
        FROM transactions
        WHERE status = 'success'
    ) AS successful_transacting_users,

    ROUND(
        100.0 *
        (
            SELECT COUNT(DISTINCT user_id)
            FROM transactions
            WHERE status = 'success'
        )
        /
        NULLIF(
            (
                SELECT COUNT(*)
                FROM users
            ),
            0
        ),
        2
    ) AS successful_transactor_rate_pct,

    ROUND(
        (
            SELECT SUM(amount)
            FROM transactions
            WHERE status = 'success'
        ),
        2
    ) AS total_successful_transaction_value;


-- ============================================================
-- VIEW 2: WEEKLY NORTH STAR METRIC
-- Weekly Successful Transacting Users
-- ============================================================

CREATE OR REPLACE VIEW vw_weekly_north_star AS

SELECT

    DATE(
        transaction_timestamp
        - INTERVAL WEEKDAY(transaction_timestamp) DAY
    ) AS week_start,

    COUNT(
        DISTINCT user_id
    ) AS weekly_successful_transacting_users,

    COUNT(*) AS successful_transactions,

    ROUND(
        SUM(amount),
        2
    ) AS successful_transaction_value

FROM transactions

WHERE
    status = 'success'

GROUP BY
    DATE(
        transaction_timestamp
        - INTERVAL WEEKDAY(transaction_timestamp) DAY
    );


-- ============================================================
-- VIEW 3: ONBOARDING FUNNEL
-- ============================================================

CREATE OR REPLACE VIEW vw_onboarding_funnel AS

WITH funnel_counts AS (

    SELECT
        (SELECT COUNT(*)
         FROM users) AS account_created,

        COUNT(DISTINCT CASE
            WHEN event_name = 'otp_verified'
            THEN user_id
        END) AS otp_verified,

        COUNT(DISTINCT CASE
            WHEN event_name = 'kyc_started'
            THEN user_id
        END) AS kyc_started,

        COUNT(DISTINCT CASE
            WHEN event_name = 'kyc_completed'
            THEN user_id
        END) AS kyc_completed,

        COUNT(DISTINCT CASE
            WHEN event_name = 'bank_linked'
            THEN user_id
        END) AS bank_linked,

        COUNT(DISTINCT CASE
            WHEN event_name = 'first_successful_transaction'
            THEN user_id
        END) AS first_successful_transaction

    FROM events
)

SELECT 1 AS step_order,
       'Account Created' AS funnel_step,
       account_created AS users
FROM funnel_counts

UNION ALL

SELECT 2, 'OTP Verified', otp_verified
FROM funnel_counts

UNION ALL

SELECT 3, 'KYC Started', kyc_started
FROM funnel_counts

UNION ALL

SELECT 4, 'KYC Completed', kyc_completed
FROM funnel_counts

UNION ALL

SELECT 5, 'Bank Linked', bank_linked
FROM funnel_counts

UNION ALL

SELECT 6, 'First Successful Transaction',
       first_successful_transaction
FROM funnel_counts;


-- ============================================================
-- VIEW 4: KYC PERFORMANCE BY DEVICE AND VERSION
-- ============================================================

CREATE OR REPLACE VIEW vw_kyc_device_version AS

SELECT

    u.device_type,

    u.signup_app_version AS app_version,

    COUNT(*) AS kyc_attempts,

    SUM(
        k.status = 'completed'
    ) AS completed,

    SUM(
        k.status = 'failed'
    ) AS failed,

    SUM(
        k.status = 'abandoned'
    ) AS abandoned,

    SUM(
        k.failure_reason =
        'document_upload_error'
    ) AS document_upload_errors,

    ROUND(
        100.0 *
        SUM(
            k.status = 'completed'
        )
        /
        COUNT(*),
        2
    ) AS completion_rate_pct,

    ROUND(
        100.0 *
        SUM(
            k.failure_reason =
            'document_upload_error'
        )
        /
        COUNT(*),
        2
    ) AS document_upload_error_rate_pct

FROM kyc_applications k

JOIN users u
    ON k.user_id = u.user_id

GROUP BY
    u.device_type,
    u.signup_app_version;


-- ============================================================
-- VIEW 5: WEEKLY KYC TREND
-- ============================================================

CREATE OR REPLACE VIEW vw_weekly_kyc_trend AS

SELECT

    DATE(
        k.started_at
        - INTERVAL WEEKDAY(k.started_at) DAY
    ) AS week_start,

    u.device_type,

    u.signup_app_version AS app_version,

    COUNT(*) AS kyc_started,

    SUM(
        k.status = 'completed'
    ) AS kyc_completed,

    SUM(
        k.status = 'failed'
    ) AS kyc_failed,

    ROUND(
        100.0 *
        SUM(
            k.status = 'completed'
        )
        /
        COUNT(*),
        2
    ) AS kyc_completion_rate_pct

FROM kyc_applications k

JOIN users u
    ON k.user_id = u.user_id

GROUP BY

    DATE(
        k.started_at
        - INTERVAL WEEKDAY(k.started_at) DAY
    ),

    u.device_type,

    u.signup_app_version;



-- ============================================================
-- VIEW 6: ACQUISITION QUALITY SCORECARD
-- Corrected D30 eligibility
-- ============================================================

CREATE OR REPLACE VIEW vw_acquisition_quality AS

WITH data_cutoff AS (
    SELECT DATE(MAX(transaction_timestamp)) AS cutoff_date
    FROM transactions
),

kyc_metrics AS (
    SELECT
        user_id,
        MAX(status = 'completed') AS completed_kyc
    FROM kyc_applications
    GROUP BY user_id
),

activation_metrics AS (
    SELECT
        user_id,
        MAX(event_name = 'first_successful_transaction') AS activated
    FROM events
    GROUP BY user_id
),

retention_metrics AS (
    SELECT
        u.user_id,
        MAX(
            CASE
                WHEN t.status = 'success'
                 AND DATEDIFF(
                     DATE(t.transaction_timestamp),
                     DATE(u.signup_timestamp)
                 ) BETWEEN 30 AND 37
                THEN 1
                ELSE 0
            END
        ) AS retained_d30
    FROM users u
    LEFT JOIN transactions t
        ON u.user_id = t.user_id
    GROUP BY u.user_id
),

user_metrics AS (
    SELECT
        u.user_id,
        u.acquisition_channel,

        COALESCE(k.completed_kyc, 0) AS completed_kyc,
        COALESCE(a.activated, 0) AS activated,

        CASE
            WHEN DATE_ADD(
                DATE(u.signup_timestamp),
                INTERVAL 37 DAY
            ) <= d.cutoff_date
            THEN COALESCE(r.retained_d30, 0)
            ELSE NULL
        END AS retained_d30,

        CASE
            WHEN DATE_ADD(
                DATE(u.signup_timestamp),
                INTERVAL 37 DAY
            ) <= d.cutoff_date
            THEN 1
            ELSE 0
        END AS retention_eligible

    FROM users u
    CROSS JOIN data_cutoff d

    LEFT JOIN kyc_metrics k
        ON u.user_id = k.user_id

    LEFT JOIN activation_metrics a
        ON u.user_id = a.user_id

    LEFT JOIN retention_metrics r
        ON u.user_id = r.user_id
)

SELECT
    acquisition_channel,

    COUNT(*) AS acquired_users,

    ROUND(
        100.0 * SUM(completed_kyc) / COUNT(*),
        2
    ) AS kyc_completion_pct,

    ROUND(
        100.0 * SUM(activated) / COUNT(*),
        2
    ) AS activation_rate_pct,

    ROUND(
        100.0 * SUM(
            CASE WHEN retention_eligible = 1
                 THEN retained_d30 ELSE 0 END
        ) / NULLIF(SUM(retention_eligible), 0),
        2
    ) AS d30_retention_pct,

    ROUND(
        (
            100.0 * SUM(activated) / COUNT(*) * 0.40
        )
        +
        (
            100.0 * SUM(
                CASE WHEN retention_eligible = 1
                     THEN retained_d30 ELSE 0 END
            ) / NULLIF(SUM(retention_eligible), 0) * 0.40
        )
        +
        (
            100.0 * SUM(completed_kyc) / COUNT(*) * 0.20
        ),
        2
    ) AS acquisition_quality_score

FROM user_metrics
GROUP BY acquisition_channel;


-- ============================================================
-- VIEW 7: EARLY BEHAVIOR AND D30 RETENTION
-- Corrected D30 eligibility
-- ============================================================

CREATE OR REPLACE VIEW vw_activation_retention AS

WITH data_cutoff AS (
    SELECT DATE(MAX(transaction_timestamp)) AS cutoff_date
    FROM transactions
),

user_behavior AS (
    SELECT
        u.user_id,

        COUNT(
            CASE
                WHEN t.status = 'success'
                 AND t.transaction_timestamp >= u.signup_timestamp
                 AND t.transaction_timestamp <
                     u.signup_timestamp + INTERVAL 7 DAY
                THEN t.transaction_id
            END
        ) AS transactions_first_7d,

        MAX(
            CASE
                WHEN t.status = 'success'
                 AND DATEDIFF(
                     DATE(t.transaction_timestamp),
                     DATE(u.signup_timestamp)
                 ) BETWEEN 30 AND 37
                THEN 1
                ELSE 0
            END
        ) AS retained_d30,

        CASE
            WHEN DATE_ADD(
                DATE(u.signup_timestamp),
                INTERVAL 37 DAY
            ) <= d.cutoff_date
            THEN 1
            ELSE 0
        END AS retention_eligible

    FROM users u
    CROSS JOIN data_cutoff d

    LEFT JOIN transactions t
        ON u.user_id = t.user_id

    GROUP BY
        u.user_id,
        u.signup_timestamp,
        d.cutoff_date
)

SELECT
    CASE
        WHEN transactions_first_7d = 0 THEN '0 transactions'
        WHEN transactions_first_7d = 1 THEN '1 transaction'
        WHEN transactions_first_7d = 2 THEN '2 transactions'
        WHEN transactions_first_7d BETWEEN 3 AND 4
            THEN '3-4 transactions'
        ELSE '5+ transactions'
    END AS early_behavior_group,

    CASE
        WHEN transactions_first_7d = 0 THEN 1
        WHEN transactions_first_7d = 1 THEN 2
        WHEN transactions_first_7d = 2 THEN 3
        WHEN transactions_first_7d BETWEEN 3 AND 4 THEN 4
        ELSE 5
    END AS group_order,

    COUNT(*) AS users,

    SUM(
        CASE
            WHEN retention_eligible = 1
             AND retained_d30 = 1
            THEN 1
            ELSE 0
        END
    ) AS retained_d30_users,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN retention_eligible = 1
                THEN retained_d30
                ELSE 0
            END
        ) / NULLIF(SUM(retention_eligible), 0),
        2
    ) AS d30_retention_pct

FROM user_behavior

GROUP BY
    early_behavior_group,
    group_order;


-- ============================================================
-- VIEW 8: MONTHLY COHORT RETENTION MATRIX
-- Correctly distinguishes zero retention from unobserved months
-- ============================================================

CREATE OR REPLACE VIEW vw_cohort_retention AS

WITH data_cutoff AS (
    SELECT DATE(MAX(transaction_timestamp)) AS cutoff_date
    FROM transactions
),

user_cohorts AS (
    SELECT
        user_id,
        DATE_FORMAT(signup_timestamp, '%Y-%m-01') AS cohort_month,
        CAST(
            DATE_FORMAT(signup_timestamp, '%Y-%m-01')
            AS DATE
        ) AS cohort_start
    FROM users
),

cohort_sizes AS (
    SELECT
        cohort_month,
        cohort_start,
        COUNT(*) AS cohort_size
    FROM user_cohorts
    GROUP BY cohort_month, cohort_start
),

activity AS (
    SELECT DISTINCT
        uc.user_id,
        uc.cohort_month,

        TIMESTAMPDIFF(
            MONTH,
            uc.cohort_start,
            CAST(
                DATE_FORMAT(t.transaction_timestamp, '%Y-%m-01')
                AS DATE
            )
        ) AS month_number

    FROM user_cohorts uc

    JOIN transactions t
        ON uc.user_id = t.user_id

    WHERE t.status = 'success'
),

retention AS (
    SELECT
        cohort_month,
        month_number,
        COUNT(DISTINCT user_id) AS retained_users
    FROM activity
    WHERE month_number BETWEEN 0 AND 5
    GROUP BY cohort_month, month_number
)

SELECT
    c.cohort_month,
    c.cohort_size,

    CASE
        WHEN LAST_DAY(c.cohort_start) <= d.cutoff_date
        THEN ROUND(
            100.0 * COALESCE(
                MAX(CASE WHEN r.month_number = 0
                    THEN r.retained_users END), 0
            ) / c.cohort_size,
            2
        )
        ELSE NULL
    END AS M0,

    CASE
        WHEN LAST_DAY(c.cohort_start + INTERVAL 1 MONTH)
             <= d.cutoff_date
        THEN ROUND(
            100.0 * COALESCE(
                MAX(CASE WHEN r.month_number = 1
                    THEN r.retained_users END), 0
            ) / c.cohort_size,
            2
        )
        ELSE NULL
    END AS M1,

    CASE
        WHEN LAST_DAY(c.cohort_start + INTERVAL 2 MONTH)
             <= d.cutoff_date
        THEN ROUND(
            100.0 * COALESCE(
                MAX(CASE WHEN r.month_number = 2
                    THEN r.retained_users END), 0
            ) / c.cohort_size,
            2
        )
        ELSE NULL
    END AS M2,

    CASE
        WHEN LAST_DAY(c.cohort_start + INTERVAL 3 MONTH)
             <= d.cutoff_date
        THEN ROUND(
            100.0 * COALESCE(
                MAX(CASE WHEN r.month_number = 3
                    THEN r.retained_users END), 0
            ) / c.cohort_size,
            2
        )
        ELSE NULL
    END AS M3,

    CASE
        WHEN LAST_DAY(c.cohort_start + INTERVAL 4 MONTH)
             <= d.cutoff_date
        THEN ROUND(
            100.0 * COALESCE(
                MAX(CASE WHEN r.month_number = 4
                    THEN r.retained_users END), 0
            ) / c.cohort_size,
            2
        )
        ELSE NULL
    END AS M4,

    CASE
        WHEN LAST_DAY(c.cohort_start + INTERVAL 5 MONTH)
             <= d.cutoff_date
        THEN ROUND(
            100.0 * COALESCE(
                MAX(CASE WHEN r.month_number = 5
                    THEN r.retained_users END), 0
            ) / c.cohort_size,
            2
        )
        ELSE NULL
    END AS M5

FROM cohort_sizes c

CROSS JOIN data_cutoff d

LEFT JOIN retention r
    ON c.cohort_month = r.cohort_month

GROUP BY
    c.cohort_month,
    c.cohort_start,
    c.cohort_size,
    d.cutoff_date;


-- ============================================================
-- VIEW 9: EXPERIMENT SCORECARD
-- ============================================================


CREATE OR REPLACE VIEW vw_experiment_scorecard AS

WITH experiment_population AS (

    SELECT
        user_id,
        variant
    FROM experiment_assignments
    WHERE experiment_id = 1
    GROUP BY user_id, variant
),

kyc_metrics AS (

    SELECT
        user_id,
        MAX(status = 'completed') AS completed_kyc
    FROM kyc_applications
    GROUP BY user_id
),

support_metrics AS (

    SELECT
        user_id,
        1 AS contacted_support
    FROM support_tickets
    GROUP BY user_id
),

activation_metrics AS (

    SELECT
        user_id,
        MAX(event_name = 'first_successful_transaction') AS activated
    FROM events
    GROUP BY user_id
),

experiment_users AS (

    SELECT
        ep.user_id,
        ep.variant,

        COALESCE(k.completed_kyc, 0) AS completed_kyc,
        COALESCE(s.contacted_support, 0) AS contacted_support,
        COALESCE(a.activated, 0) AS activated

    FROM experiment_population ep

    LEFT JOIN kyc_metrics k
        ON ep.user_id = k.user_id

    LEFT JOIN support_metrics s
        ON ep.user_id = s.user_id

    LEFT JOIN activation_metrics a
        ON ep.user_id = a.user_id
)

SELECT
    variant,

    COUNT(*) AS assigned_users,

    ROUND(
        100.0 * SUM(completed_kyc) / COUNT(*),
        2
    ) AS kyc_completion_rate_pct,

    ROUND(
        100.0 * SUM(contacted_support) / COUNT(*),
        2
    ) AS support_contact_rate_pct,

    ROUND(
        100.0 * SUM(activated) / COUNT(*),
        2
    ) AS activation_rate_pct

FROM experiment_users

GROUP BY variant;
