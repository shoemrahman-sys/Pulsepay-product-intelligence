# PulsePay Metric Dictionary

## Purpose

This document defines the key product, onboarding, activation, retention, acquisition, incident, and experiment metrics used in the PulsePay Product Analytics project.

Each metric should have a consistent definition so that SQL analysis, Python outputs, dashboards, and business recommendations use the same interpretation.

---

# 1. North Star Metric

## Weekly Successful Transacting Users (WSTU)

**Definition:**

Number of unique users who complete at least one successful transaction during an ISO calendar week.

**Formula:**

```text
COUNT(DISTINCT user_id)
WHERE transaction_status = 'success'
GROUPED BY ISO calendar week
```

**Why it matters:**

It captures recurring delivery of the product's core value: successfully moving or spending money.

**Limitation:**

A single successful transaction does not necessarily indicate long-term adoption. WSTU should be interpreted alongside transaction frequency and retention.

---

# 2. Product Health Metrics

## Total Registered Users

**Definition:**

Total number of users registered in the PulsePay platform.

**Formula:**

```text
COUNT(DISTINCT user_id)
FROM users
```

**Latest result:** 50,000

**Why it matters:**

Provides the overall registered user population and context for other conversion metrics.

---

## Total Transactions

**Definition:**

Total number of transaction records in the transaction dataset.

**Formula:**

```text
COUNT(*)
FROM transactions
```

**Latest result:** 65,047

**Why it matters:**

Measures transaction activity across the platform.

**Limitation:**

Transaction records are not equivalent to unique transacting users.

---

## Successful Transactions

**Definition:**

Number of transaction records with a successful transaction status.

**Formula:**

```text
COUNT(*)
WHERE status = 'success'
```

**Latest result:** 61,179

---

## Successful Transacting Users

**Definition:**

Number of unique users who have completed at least one successful transaction.

**Formula:**

```text
COUNT(DISTINCT user_id)
WHERE status = 'success'
```

**Latest result:** 19,102

---

## Successful Transactor Rate

**Definition:**

Percentage of registered users who have completed at least one successful transaction.

**Formula:**

```text
Successful Transacting Users
/
Total Registered Users
× 100
```

**Latest result:** 38.20%

**Why it matters:**

Measures how much of the registered population has reached the product's core transaction activity.

**Limitation:**

This is a cumulative activation measure, not necessarily activation within a fixed number of days after signup.

---

## Transaction Success Rate

**Definition:**

Percentage of transaction attempts with status `success`.

**Formula:**

```text
Successful Transactions
/
All Transaction Attempts
× 100
```

**Latest result:** 94.05%

**Why it matters:**

Measures transaction reliability and the proportion of recorded attempts that succeed.

**Limitation:**

This is transaction-level, not user-level. One user may contribute multiple transaction attempts.

---

## Total Successful Transaction Value

**Definition:**

Sum of transaction amounts for successful transactions.

**Formula:**

```text
SUM(amount)
WHERE status = 'success'
```

**Latest result:** 22,259,562.41

**Why it matters:**

Provides a measure of successful transaction value processed by the platform.

**Limitation:**

This is synthetic project transaction value. It should not be represented as real financial revenue or profit.

---

# 3. Onboarding Funnel Metrics

## Funnel Stage Users

**Definition:**

Number of distinct users reaching each onboarding stage.

**Stages:**

1. Account Created
2. OTP Verified
3. KYC Started
4. KYC Completed
5. Bank Linked
6. First Successful Transaction

**Formula:**

```text
COUNT(DISTINCT user_id)
for each defined funnel stage
```

**Latest stage counts:**

| Stage | Users |
|---|---:|
| Account Created | 50,000 |
| OTP Verified | 47,047 |
| KYC Started | 40,948 |
| KYC Completed | 30,118 |
| Bank Linked | 26,513 |
| First Successful Transaction | 19,102 |

---

## Stage Conversion Rate

**Definition:**

Percentage of users reaching a funnel stage relative to the number of users reaching the previous stage.

**Formula:**

```text
Users at Current Stage
/
Users at Previous Stage
× 100
```

**Why it matters:**

Identifies where users experience the largest conversion losses in the onboarding journey.

**Limitation:**

Distinct stage counts do not independently prove exact chronological progression for every user.

---

## Overall Registration-to-Activation Rate

**Definition:**

Percentage of registered users who have completed at least one successful transaction.

**Formula:**

```text
Users with a First Successful Transaction
/
Total Registered Users
× 100
```

**Latest result:** 38.20%

**Interpretation:**

Measures cumulative conversion from registration to the product's core transaction activity.

---

# 4. Activation Metrics

## Technical Activation

**Definition:**

A user completes their first successful transaction.

**Purpose:**

Represents the point at which the user first experiences the product's core transaction value.

---

## First-Seven-Day Successful Transaction Count

**Definition:**

Number of successful transactions completed by a user during the first seven days after signup.

**User groups:**

```text
0 transactions
1 transaction
2 transactions
3–4 transactions
5+ transactions
```

**Purpose:**

Used to investigate the relationship between early transaction behavior and subsequent retention.

**Latest results:**

| Early Transaction Group | Users | D30 Retention |
|---|---:|---:|
| 0 | 35,380 | 1.10% |
| 1 | 7,050 | 5.24% |
| 2 | 3,629 | 9.03% |
| 3–4 | 3,031 | 11.72% |
| 5+ | 910 | 16.11% |

**Limitation:**

This is a behavioral segmentation metric, not proof that increasing early transaction frequency will cause retention to increase.

---

# 5. Retention Metrics

## D7 Retention

**Definition:**

Percentage of users active on day 7 after signup, using the project's explicitly defined activity event and observation window.

**Important:**

D7 retention should only be reported when the activity definition and day-7 observation window are implemented and validated.

It is not interchangeable with D30 retention.

---

## D30 Retention

**Definition:**

Percentage of eligible users who complete at least one successful transaction during the defined day-30 observation window.

**Project observation window:**

```text
Day 30 through Day 37 after signup
```

**Formula:**

```text
Users with at least one successful transaction
during the D30 observation window
/
Eligible users
× 100
```

**Latest overall result:** 2.666%

**Latest retained users:** 1,333

**Why it matters:**

Measures whether users return to perform meaningful transaction activity after their initial onboarding period.

**Limitation:**

This is a project-specific retention definition. Results may differ from exact-day, rolling, unbounded, or calendar-month retention definitions.

---

## Cohort Retention

**Definition:**

Percentage of users in a signup-month cohort who complete successful transaction activity in a subsequent calendar month.

**Cohort grouping:**

```text
M0 = Signup month
M1 = One calendar month after signup
M2 = Two calendar months after signup
M3 = Three calendar months after signup
...
```

**Formula:**

```text
Users in a cohort active during the relevant month
/
Original cohort size
× 100
```

**Why it matters:**

Helps compare retention patterns across different signup cohorts.

**Limitation:**

Recent cohorts may not have complete observation periods. Missing future months must remain blank or unavailable, not be treated as zero retention.

---

# 6. KYC Metrics

## KYC Completion Rate

**Definition:**

Percentage of KYC attempts that are successfully completed.

**Formula:**

```text
Completed KYC Attempts
/
Total KYC Attempts
× 100
```

**Why it matters:**

Measures the efficiency of the KYC process and identifies potential onboarding friction.

**Important distinction:**

The dashboard's device/version analysis uses KYC attempt-level records. Its denominator is attempts, not necessarily distinct users.

This metric should not be described as a unique-user completion rate unless the calculation explicitly deduplicates users.

---

## KYC Failure Rate

**Definition:**

Percentage of KYC attempts that end in a failed status.

**Formula:**

```text
Failed KYC Attempts
/
Total KYC Attempts
× 100
```

**Why it matters:**

Helps identify operational or technical friction in identity verification.

---

## KYC Abandonment Rate

**Definition:**

Percentage of KYC attempts that are abandoned.

**Formula:**

```text
Abandoned KYC Attempts
/
Total KYC Attempts
× 100
```

**Why it matters:**

Helps distinguish users who fail verification from those who leave before completing the process.

---

## Document Upload Error Rate

**Definition:**

Percentage of KYC attempts associated with a document-upload error.

**Formula:**

```text
Document Upload Error Attempts
/
Total KYC Attempts
× 100
```

**Why it matters:**

Helps identify technical problems that may prevent users from completing identity verification.

**Limitation:**

An observed error association does not by itself establish the technical root cause.

---

# 7. Incident Impact Metrics

## KYC Completion Gap

**Definition:**

Difference between the reference KYC completion rate and the observed completion rate of the investigated segment.

**Formula:**

```text
Reference Completion Rate
-
Observed Completion Rate
```

**Latest Android 5.4 result:** 21.49 percentage points

---

## Estimated Lost KYC Completions

**Definition:**

Estimated difference between the expected KYC completions at the reference rate and the actual completions.

**Formula:**

```text
Expected Completions
-
Actual Completions
```

Where:

```text
Expected Completions
=
Affected Segment Attempts
×
Reference Completion Rate
```

**Latest estimate:** 1,102 KYC completions

---

## Estimated Lost Activated Users

**Definition:**

Estimated number of downstream activated users associated with the estimated KYC completion gap.

**Formula:**

```text
Estimated Lost KYC Completions
×
Observed Post-KYC Activation Rate
```

**Latest estimate:** 692 activated users

**Limitation:**

These are counterfactual estimates based on a reference performance assumption. They are not proven causal losses.

---

# 8. Acquisition Quality Metrics

## Acquisition Channel User Volume

**Definition:**

Number of registered users attributed to an acquisition channel.

**Formula:**

```text
COUNT(DISTINCT user_id)
GROUPED BY acquisition_channel
```

**Why it matters:**

Measures the scale of each acquisition source.

---

## Acquisition KYC Completion Rate

**Definition:**

KYC completion rate for users grouped by acquisition channel.

**Purpose:**

Evaluates how effectively each channel brings users who progress through identity verification.

---

## Acquisition Activation Rate

**Definition:**

Percentage of users in an acquisition channel who complete a successful transaction.

**Purpose:**

Evaluates downstream conversion quality by acquisition source.

---

## Acquisition D30 Retention Rate

**Definition:**

Percentage of users in an acquisition channel who satisfy the project's D30 retention definition.

**Purpose:**

Evaluates whether users acquired through a channel return to perform successful transactions.

---

## Acquisition Quality Score

**Definition:**

A composite prioritization score based on activation, D30 retention, and KYC completion.

**Formula:**

```text
Acquisition Quality Score
=
40% × Activation Rate
+
40% × D30 Retention Rate
+
20% × KYC Completion Rate
```

**Purpose:**

Provides a consistent framework for comparing downstream acquisition quality.

**Limitation:**

The weights are chosen for this project. The score does not directly measure customer acquisition cost, revenue, profitability, or lifetime value.

---

# 9. Experiment Metrics

## KYC Completion Rate — Primary Metric

**Definition:**

Percentage of experiment users who successfully complete KYC.

**Purpose:**

Measures the direct effect of the KYC flow treatment on verification completion.

---

## Support Contact Rate — Guardrail Metric

**Definition:**

Percentage of experiment users who contact support, based on the project's implemented support-contact calculation.

**Purpose:**

Monitors whether a treatment that changes onboarding performance also increases support demand.

**Interpretation:**

A higher support contact rate may indicate additional user friction, but it does not independently establish the cause of the increase.

---

## Activation Rate — Downstream Metric

**Definition:**

Percentage of experiment users who complete a successful transaction according to the experiment scorecard's activation definition.

**Purpose:**

Provides downstream context about whether onboarding changes are associated with successful transaction activity.

**Limitation:**

The metric should not be assumed to represent seven-day activation unless the underlying calculation explicitly uses that time window.

---

## Absolute Lift

**Definition:**

Difference between treatment and control metric rates.

**Formula:**

```text
Treatment Rate - Control Rate
```

**Unit:**

Percentage points for rate metrics.

---

## Relative Lift

**Definition:**

Percentage change in the treatment rate relative to the control rate.

**Formula:**

```text
(Treatment Rate - Control Rate)
/
Control Rate
× 100
```

**Why it matters:**

Provides relative context for the observed treatment difference.

---

## Sample Ratio Mismatch (SRM)

**Definition:**

A discrepancy between the observed experiment allocation and the expected allocation.

**Purpose:**

Checks whether the experiment population is distributed according to the intended assignment ratio.

**Statistical method:**

Chi-square goodness-of-fit test.

**Important:**

SRM is an experiment-integrity diagnostic. A statistically significant mismatch indicates that assignment, eligibility, filtering, or instrumentation should be investigated.

A non-significant result does not prove that every aspect of experiment implementation is correct.

---

## P-value

**Definition:**

The probability, assuming the null hypothesis and statistical model are correct, of observing a test statistic at least as extreme as the one obtained.

**Purpose:**

Helps evaluate the strength of evidence against the null hypothesis.

**Important:**

A p-value is not the probability that the experiment is wrong or that the null hypothesis is true.

---

## Confidence Interval

**Definition:**

A range of plausible values for the treatment effect under the statistical method and assumptions used.

**Purpose:**

Shows the uncertainty and precision around the estimated treatment effect.

**Interpretation:**

For a difference in rates, a confidence interval containing zero indicates that the data is compatible with no difference at the corresponding confidence level.

---

# 10. Metric Interpretation Principles

The following distinctions should be maintained throughout the project:

| Metric Type | What It Measures | What It Does Not Prove |
|---|---|---|
| Descriptive metrics | Observed product performance | Causality |
| Funnel conversion | Progression between stages | Exact reasons for user loss |
| Retention | Return activity | Why users return |
| Cohort analysis | Retention patterns over time | Causes of cohort differences |
| Segmentation | Differences between user groups | Causal impact of group attributes |
| Counterfactual estimates | Potential impact under assumptions | Actual causal losses |
| Experiment statistics | Evidence about treatment differences | Guaranteed business success |

---

# Final Principle

Every metric should answer three questions:

1. **What exactly is being measured?**
2. **How is it calculated?**
3. **What conclusions can and cannot be drawn from it?**

Consistent metric definitions help ensure that SQL queries, Python analysis, dashboards, and business recommendations communicate the same analytical story.