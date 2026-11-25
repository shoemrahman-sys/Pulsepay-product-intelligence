# PulsePay Analytical Methodology

## Purpose

This document explains the analytical definitions, assumptions, statistical methods, and limitations used in the PulsePay Product Analytics project.

The goal is to make the analysis:

- Transparent
- Reproducible
- Interpretable
- Explicit about uncertainty

---

# 1. Analytical Workflow

The project follows this workflow:

```text
Define the product question
        ↓
Validate the available data
        ↓
Define metrics
        ↓
Analyze aggregate product health
        ↓
Segment performance
        ↓
Investigate anomalies
        ↓
Estimate potential impact
        ↓
Evaluate user behavior
        ↓
Test product hypotheses
        ↓
Quantify uncertainty
        ↓
Make a product recommendation
```

The workflow moves from descriptive analysis toward diagnosis, impact estimation, and evidence-based decision-making.

---

# 2. Product Health

Product health is evaluated using:

- Total registered users
- Total transactions
- Successful transactions
- Successful transacting users
- Transaction success rate
- Total successful transaction value
- Weekly successful transacting users

Latest executive-level results:

| Metric | Result |
|---|---:|
| Total users | 50,000 |
| Total transactions | 65,047 |
| Successful transactions | 61,179 |
| Transaction success rate | 94.05% |
| Successful transacting users | 19,102 |
| Successful transactor rate | 38.20% |
| Successful transaction value | 22,259,562.41 |

These metrics establish the overall product-health baseline before deeper diagnostic analysis begins.

---

# 3. North Star Metric

## Weekly Successful Transacting Users

The project's North Star metric counts:

> Distinct users completing at least one successful transaction during a calendar week.

### Rationale

Account creation alone does not indicate that the user received meaningful value.

Successful transaction activity is a stronger indicator of actual usage for a digital payments product.

### Limitation

A single successful transaction does not necessarily indicate long-term product adoption.

The metric should therefore be interpreted alongside:

- Transaction frequency
- Retention
- Cohort behavior
- Transaction success rate

---

# 4. Funnel Methodology

The onboarding journey is modeled as:

```text
Account Created
→ OTP Verified
→ KYC Started
→ KYC Completed
→ Bank Linked
→ First Successful Transaction
```

Distinct users reaching each stage are counted.

Latest funnel results:

| Stage | Users | Conversion from Previous Stage |
|---|---:|---:|
| Account Created | 50,000 | — |
| OTP Verified | 47,047 | 94.09% |
| KYC Started | 40,948 | 87.04% |
| KYC Completed | 30,118 | 73.55% |
| Bank Linked | 26,513 | 88.03% |
| First Successful Transaction | 19,102 | 72.04% |

Overall registration-to-activation rate:

```text
19,102 / 50,000 = 38.20%
```

### Interpretation

The largest absolute user drop occurs between KYC Started and KYC Completed:

```text
40,948 - 30,118 = 10,830 users
```

This makes KYC completion an important investigation area.

A funnel drop does not by itself explain why users fail to progress.

### Limitation

The stages represent distinct user counts. They should not automatically be interpreted as proof that every user completed the stages in the exact displayed order.

Segmented and event-level analysis is required to investigate progression and diagnose user loss.

---

# 5. Activation Methodology

The project distinguishes between two activation concepts.

## Technical Activation

A user completes their first successful transaction.

## Behavioral Activation

A user establishes repeated meaningful usage during the early lifecycle.

The project evaluates the number of successful transactions completed within the first seven days.

Users are grouped into:

```text
0 transactions
1 transaction
2 transactions
3–4 transactions
5+ transactions
```

D30 retention is then compared across these groups.

Latest results:

| First-7-Day Successful Transactions | Users | D30 Retained Users | D30 Retention |
|---|---:|---:|---:|
| 0 | 35,380 | 321 | 1.10% |
| 1 | 7,050 | 312 | 5.24% |
| 2 | 3,629 | 277 | 9.03% |
| 3–4 | 3,031 | 298 | 11.72% |
| 5+ | 910 | 125 | 16.11% |

### Interpretation

Users with higher early transaction frequency show higher observed D30 retention.

This relationship may make early transaction behavior useful as:

- An activation signal
- A segmentation feature
- A lifecycle intervention target

### Causal Limitation

The relationship is observational.

Users who transact frequently may already differ in motivation, financial needs, intent, or other characteristics.

Therefore:

> Association between early usage and retention does not prove that forcing additional early transactions will cause retention to increase.

---

# 6. D30 Retention Definition

For this project, a user is considered D30 retained when they complete a successful transaction during the defined day-30 observation window.

The implemented SQL uses:

```text
Day 30 through Day 37 after signup
```

This window reduces sensitivity to users returning slightly before or after an exact calendar day.

Latest overall D30 retention from the activation-retention export:

```text
1,333 retained users / 50,000 users = 2.666%
```

### Important Interpretation

This is a project-specific retention definition.

Other products may use:

- Exact Day 30 retention
- Rolling retention
- Unbounded retention
- Weekly retention
- Monthly retention

Metric definitions should be selected according to the product's natural usage frequency.

### Limitation

The retention metric depends on the selected observation window and the availability of sufficient follow-up data for each user.

It should not be compared directly with retention figures from products using different definitions or eligibility rules.

---

# 7. Cohort Retention Methodology

Users are grouped by signup month.

Successful transaction activity is evaluated by the number of calendar months elapsed since the cohort month.

The output includes:

```text
M0
M1
M2
M3
M4
M5
```

### Interpretation

Cohort analysis helps determine whether retention patterns differ across user generations.

For example, the latest export shows that January 2026 has:

| Cohort Month | M0 | M1 | M2 | M3 | M4 | M5 |
|---|---:|---:|---:|---:|---:|---:|
| January 2026 | 32.81% | 18.63% | 1.55% | 0.07% | 0% | 0% |

The sharp decline after M1 is a potential retention concern that deserves further investigation.

### Incomplete Cohorts

Recent cohorts may not have had enough time to reach later lifecycle months.

Missing future observations should not be interpreted as zero retention.

A blank value means that the relevant observation period is not yet available. It is different from an observed period with zero retained users.

### Limitation

Cohort trends should be interpreted with attention to cohort maturity, observation windows, and possible differences in acquisition mix.

---

# 8. KYC Incident Investigation

The incident investigation uses segmentation across:

- Device type
- App version
- KYC status
- Failure reason
- Time

The investigation identified Android 5.4 as an underperforming segment.

Latest results:

| Metric | Android 5.3 | Android 5.4 |
|---|---:|---:|
| KYC attempts | 14,786 | 5,129 |
| Completed | 11,264 | 2,805 |
| Failed | 2,207 | 1,420 |
| Abandoned | 1,315 | 904 |
| Document-upload errors | 0 | 1,420 |
| Completion rate | 76.18% | 54.69% |

The completion-rate difference is:

```text
76.18% - 54.69% = 21.49 percentage points
```

This combination of lower completion and elevated document-upload errors provides a plausible product-quality hypothesis.

### Causal Limitation

The analysis does not prove that the app version alone caused the observed decline.

The app version field represents the user's signup app version. It may not necessarily represent the version installed when the KYC attempt occurred.

Technical logs, release diagnostics, device-level investigation, controlled rollout evidence, or additional causal analysis would be required for stronger causal attribution.

The observed pattern should therefore be treated as an investigation signal rather than definitive proof of a software defect.

---

# 9. Incident Impact Estimation

Android 5.3 is used as a reference baseline for Android 5.4.

The counterfactual calculation is:

```text
Expected Completions
=
Android 5.4 KYC Attempts
×
Android 5.3 Completion Rate
```

Estimated completion difference:

```text
Expected Completions
-
Actual Android 5.4 Completions
```

Estimated downstream activated-user difference:

```text
Estimated Completion Difference
×
Observed Post-KYC Activation Rate
```

### Latest Results

| Metric | Estimate |
|---|---:|
| Android 5.4 KYC attempts | 5,129 |
| Actual completions | 2,805 |
| Actual completion rate | 54.69% |
| Android 5.3 reference completion rate | 76.18% |
| Expected completions at reference rate | 3,907 |
| Estimated lost KYC completions | 1,102 |
| Post-KYC activation rate | 62.75% |
| Estimated lost activated users | 692 |

### Interpretation

The analysis estimates that approximately 1,102 additional KYC completions and 692 additional activated users might have been achieved if Android 5.4 had performed at the Android 5.3 reference rate.

These are:

> Counterfactual estimates

They are not:

> Proven causal losses

The estimate assumes Android 5.3 is a reasonable performance reference for Android 5.4.

It also assumes the observed post-KYC activation rate is applicable to the estimated additional completions.

Differences in user mix, acquisition source, device conditions, and other factors could affect the actual impact.

---

# 10. Acquisition Quality Methodology

Acquisition channels are evaluated using:

- User volume
- KYC completion
- Activation
- D30 retention

A composite score is created:

```text
Acquisition Quality Score
=
40% × Activation Rate
+
40% × D30 Retention Rate
+
20% × KYC Completion Rate
```

Latest acquisition results:

| Channel | Users | KYC Completion | Activation | D30 Retention | Quality Score |
|---|---:|---:|---:|---:|---:|
| Referral | 8,585 | 64.72% | 44.37% | 3.92% | 32.26 |
| Paid Search | 8,931 | 61.11% | 38.62% | 3.38% | 29.02 |
| Partnership | 4,515 | 61.24% | 38.34% | 3.05% | 28.81 |
| Organic | 13,924 | 59.95% | 38.02% | 3.39% | 28.55 |
| Influencer | 3,969 | 59.64% | 38.40% | 2.95% | 28.47 |
| Paid Social | 10,076 | 55.83% | 32.70% | 2.42% | 25.21 |

### Purpose

The score provides a simple prioritization framework for comparing downstream acquisition quality.

Referral currently has the highest composite score and the strongest activation and D30 retention rates in the latest export.

Paid Social has the lowest score and weaker observed performance across the listed metrics.

### Limitation

The weighting is a product decision rather than an objective statistical truth.

Different businesses may assign different weights based on:

- Revenue
- Customer acquisition cost
- Lifetime value
- Strategic priorities
- Profitability

The score is a prioritization heuristic, not proof that one acquisition channel is more profitable.

---

# 11. Experiment Design

The KYC experiment compares:

```text
Control
vs
Treatment
```

## Primary Metric

KYC Completion Rate

## Guardrail Metric

Support Contact Rate

## Downstream Metric

Activation Rate

The primary decision should be based on the predefined primary metric while considering guardrail health and experiment validity.

The guardrail helps identify whether a change that improves the primary metric may also create additional user friction or support demand.

Activation provides downstream context but should not replace the predefined primary metric.

---

# 12. Experiment Validation

Before evaluating treatment effects, the analysis checks:

- Number of experiment users
- Available variants
- Allocation balance
- Duplicate assignments, where the underlying assignment data supports that validation
- Consistency of the analysis population

Latest scorecard results:

```text
Total assigned users: 6,032

Control:   3,012
Treatment: 3,020
```

For an intended 50/50 allocation, the expected count is:

```text
3,016 users per variant
```

The latest allocation is close to the intended split.

### Important Versioning Note

An older analysis reported:

```text
3,102 control
2,930 treatment
```

Those counts do not match the latest scorecard population.

The older assignment counts and associated statistical results must not be combined with the latest scorecard.

The experiment population and source data must be reconciled before publishing a definitive inferential analysis.

---

# 13. Sample Ratio Mismatch

The intended experiment allocation was:

```text
50% Control
50% Treatment
```

A chi-square goodness-of-fit test can be used to compare observed allocation with the expected split.

Using the latest scorecard counts:

```text
Control:   3,012
Treatment: 3,020

Expected:  3,016 per variant
```

The approximate chi-square statistic is:

```text
Chi-square ≈ 0.0106
P-value ≈ 0.918
```

At a 5% significance threshold, these counts do not indicate a statistically significant allocation imbalance.

### Interpretation

The latest scorecard allocation appears consistent with a 50/50 split, assuming the scorecard contains the complete eligible assignment population.

This does not independently establish that every aspect of experiment assignment and instrumentation was correct.

Potential experiment-integrity issues can still include:

- Assignment logic
- Eligibility filtering
- Instrumentation issues
- Missing data
- Post-assignment exclusions
- Duplicate or inconsistent records

### Historical Result Reconciliation

An older analysis reported:

```text
Chi-square = 4.9045
P-value = 0.0268
```

That result was based on the older 3,102 / 2,930 allocation counts.

It should not be reported as the SRM result for the latest 3,012 / 3,020 scorecard.

---

# 14. Primary Metric Statistical Test

The experiment compares two proportions:

```text
Control KYC Completion Rate
vs
Treatment KYC Completion Rate
```

A two-proportion z-test is appropriate for comparing independent proportions when the required assumptions are satisfied.

## Null Hypothesis

```text
H0:
Treatment completion rate
=
Control completion rate
```

## Alternative Hypothesis

```text
H1:
Treatment completion rate
≠
Control completion rate
```

A two-sided test is used because the analysis evaluates whether the treatment differs from control rather than assuming improvement in advance.

### Statistical Reporting Requirement

The test should use the same experiment population, assignment counts, and metric definitions as the published scorecard.

A statistical result from an older population must not be attached to a newer scorecard.

The latest scorecard currently provides descriptive rates. Its inferential results have not been reconciled and should not be inferred from the older analysis.

---

# 15. Latest Experiment Results

Latest descriptive scorecard:

| Metric | Control | Treatment | Difference |
|---|---:|---:|---:|
| Assigned users | 3,012 | 3,020 | — |
| KYC completion rate | 62.55% | 62.48% | -0.07 pp |
| Support contact rate | 13.48% | 13.64% | +0.16 pp |
| Activation rate | 39.18% | 39.60% | +0.42 pp |

Differences are calculated as:

```text
Treatment Rate - Control Rate
```

### Interpretation

- KYC completion is almost unchanged, with treatment slightly lower.
- Support contact is slightly higher in treatment.
- Activation is slightly higher in treatment.

These are descriptive differences only.

The latest scorecard does not establish whether these differences are statistically significant or whether they represent meaningful product effects.

### Historical Results

An older analysis reported:

```text
Control KYC completion:   60.67%
Treatment KYC completion: 62.22%

Absolute lift: +1.55 percentage points
Relative lift: +2.55%

Z-score: 1.2343
P-value: 0.2171

95% Confidence Interval:
[-0.91, +4.00] percentage points
```

These results belong to the older experiment analysis population and must not be presented as the inferential results for the latest scorecard.

---

# 16. Statistical Interpretation

Statistical significance should be evaluated using the inferential results calculated from the same population as the descriptive scorecard.

The older experiment analysis was not statistically significant at:

```text
alpha = 0.05
```

because:

```text
p-value > 0.05
```

Its confidence interval also included zero.

However, those results cannot be transferred to the latest scorecard without reconciling the underlying experiment population and calculations.

### Important

A non-significant result does not prove that:

```text
Treatment effect = exactly zero
```

Possible interpretations include:

- No meaningful effect exists
- A smaller effect exists
- The experiment lacked sufficient power
- Experiment integrity issues affected the result

For the latest scorecard, statistical significance and confidence intervals remain unresolved.

---

# 17. Experiment Decision Framework

The project does not use:

```text
Treatment metric > Control metric
=
Ship
```

Instead, the decision considers:

```text
Metric Direction
+
Statistical Evidence
+
Confidence Interval
+
Guardrail Health
+
Experiment Integrity
+
Business Impact
```

For the latest PulsePay scorecard:

- Primary metric moved slightly negatively.
- Support contact rate moved slightly upward.
- Activation moved slightly positively.
- The observed allocation is close to the intended 50/50 split.
- Latest inferential results have not been reconciled.

Therefore:

> Do not declare the treatment a winner or recommend a full rollout based on this scorecard alone.

The next analytical step is to reconcile the experiment population and calculate the primary metric's statistical test and confidence interval using the latest assignment data.

A rollout decision should also consider guardrail performance and the potential business consequences of the change.

---

# 18. Reproducibility

The project separates the analytical workflow into:

## Data Generation

```text
python/data_generation/
```

## SQL Analysis

```text
sql/02_analysis/
```

## Experiment Analysis

```text
sql/03_experiments/
python/analysis/
```

## Dashboard Semantic Layer

```text
sql/04_dashboard/
```

## Final Analytical Exports

```text
data/processed/final_results/
```

The automation pipeline exports analytical results for documentation and dashboard use.

This structure separates:

```text
Raw Data
→ Analysis Logic
→ Reusable Views
→ Statistical Analysis
→ Final Exports
→ Dashboard Outputs
```

The latest exported evidence should be treated as the reporting reference for the current documentation version.

---

# 19. Data Ethics and Disclosure

The dataset is entirely synthetic.

PulsePay is fictional.

No real:

- Customer data
- Financial information
- KYC information
- Personally identifiable information

is used.

The project is intended to demonstrate analytical methodology, technical implementation, product reasoning, and communication.

---

# 20. Key Limitations

## Synthetic Data

The findings are intentionally generated for portfolio demonstration and should not be represented as real business outcomes.

## Observational Analysis

Retention and early-usage relationships do not establish causality.

## Funnel Interpretation

Distinct user counts at each stage do not independently prove exact chronological progression for every user.

## Counterfactual Impact

Incident impact depends on the assumption that Android 5.3 is an appropriate reference for Android 5.4.

## Version Attribution

The recorded signup app version may not represent the app version at the time of the KYC attempt.

## Acquisition Quality Score

The composite score uses chosen weights and does not directly measure profitability or lifetime value.

## Experiment Population Reconciliation

Older experiment statistics and latest scorecard counts differ. Inferential results must be reconciled before making a definitive experiment claim.

## Experiment Power

A non-significant result may reflect insufficient statistical power rather than the complete absence of an effect.

## Cohort Maturity

Recent cohorts have incomplete observation periods. Missing future months must not be treated as zero retention.

---

# Final Analytical Principle

The project follows one central principle:

> Product analytics should not stop at reporting what happened.

The analytical workflow should move toward:

```text
What happened?
      ↓
Where did it happen?
      ↓
Why might it have happened?
      ↓
How large might the impact be?
      ↓
What evidence do we have?
      ↓
How certain are we?
      ↓
What should the product team do next?
```

The objective is not simply to produce metrics or charts.

It is to translate data into defensible product decisions while clearly communicating assumptions, uncertainty, and limitations.