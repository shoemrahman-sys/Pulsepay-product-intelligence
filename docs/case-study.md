# PulsePay Product Analytics Case Study

## From Product Health to Product Decision

**Author:** Abdul Rahman Shoem
**Role:** Product Analyst
**Tools:** MySQL · SQL · Python · Pandas · Statistical Testing · Power BI

## Executive Summary

PulsePay is a fictional digital payments product created as an end-to-end product analytics case study.

The analysis examined the user lifecycle across:

**Acquisition → Signup → KYC → Activation → Transaction → Retention**

The investigation focused on four major product questions:

1. Where does friction exist in the onboarding and activation journey?
2. Which product segments show significant performance deterioration?
3. Which acquisition and early-user behaviors are associated with stronger downstream engagement?
4. Did a proposed KYC experience demonstrate enough improvement to justify rollout?

The most significant investigation signal was a substantial KYC performance gap for **Android app version 5.4**.

The affected segment recorded:

- 5,129 KYC attempts
- 54.69% KYC completion
- 1,420 document-upload errors

Android 5.3 recorded a reference completion rate of **76.18%**, representing a **21.49 percentage-point gap**.

Using Android 5.3 as a counterfactual reference, the analysis estimated:

- Approximately 1,102 additional KYC completions at reference performance
- Approximately 692 additional downstream activated users

These are estimated potential impacts, not proven causal losses.

The KYC experiment scorecard showed:

- Control KYC completion: 62.55%
- Treatment KYC completion: 62.48%
- Control activation: 39.18%
- Treatment activation: 39.60%

The treatment did not outperform control on the primary metric in the latest scorecard. The differences were small, and the descriptive scorecard alone does not establish statistical significance.

The resulting product recommendation was:

> **Prioritize investigation of the Android 5.4 KYC issue, improve monitoring of downstream product behavior, and do not declare the KYC treatment a winner based on the current scorecard.**

---

# 1. Product Context

Digital payment products depend on users successfully progressing through several critical stages:

```text
Acquisition
    ↓
Account Creation
    ↓
Identity Verification
    ↓
Bank Linking
    ↓
First Successful Transaction
    ↓
Repeated Product Usage
    ↓
Retention
```

A failure at an early stage can reduce the number of users available to activate and eventually become retained customers.

For PulsePay, the analytical objective was not simply to report metrics.

The objective was to understand:

> **Where is product value being lost, why might it be happening, and what should the product team do next?**

---

# 2. Analytical Approach

The project followed a layered analytical framework.

## Layer 1 — Product Health

Establish the overall state of the product using:

- User volume
- Successful transactions
- Transaction success rate
- Successful transacting users
- Transaction value
- Weekly meaningful usage

## Layer 2 — Funnel Analysis

Measure progression through:

```text
Account Created
→ OTP Verified
→ KYC Started
→ KYC Completed
→ Bank Linked
→ First Successful Transaction
```

## Layer 3 — Root-Cause Investigation

Segment product performance by:

- Device type
- App version
- KYC outcome
- Failure reason
- Time

## Layer 4 — Retention Analysis

Evaluate:

- D30 retention
- Early transaction behavior
- Monthly cohorts

## Layer 5 — Acquisition Quality

Compare acquisition sources using downstream outcomes rather than signup volume alone.

## Layer 6 — Experimentation

Evaluate a proposed product change using:

- Primary metric
- Guardrail metric
- Downstream metric
- Experiment allocation
- Statistical evidence
- Confidence intervals
- Sample-ratio-mismatch checks

---

# 3. Product Health and Meaningful Usage

A central analytical decision was distinguishing between **registration** and **meaningful product usage**.

A user creating an account does not necessarily mean that the product has delivered value.

For a payments product, a stronger behavioral signal is:

> **Completing a successful transaction.**

The project's North Star metric was therefore defined as:

## Weekly Successful Transacting Users

A user is counted if they complete at least one successful transaction during a calendar week.

The latest pipeline evidence reported:

| Product health metric | Result |
|---|---:|
| Total registered users | 50,000 |
| Total transactions | 65,047 |
| Successful transactions | 61,179 |
| Transaction success rate | 94.05% |
| Successful transacting users | 19,102 |
| Successful transactor rate | 38.20% |
| Successful transaction value | 22,259,562.41 |

This metric was chosen because it represents actual product usage rather than passive account ownership.

---

# 4. Onboarding Funnel Analysis

The onboarding funnel was used to identify where users were dropping out of the product journey.

The latest exported results were:

| Funnel stage | Users | Conversion from previous stage |
|---|---:|---:|
| Account Created | 50,000 | — |
| OTP Verified | 47,047 | 94.09% |
| KYC Started | 40,948 | 87.04% |
| KYC Completed | 30,118 | 73.55% |
| Bank Linked | 26,513 | 88.03% |
| First Successful Transaction | 19,102 | 72.04% |

The overall percentage of registered users reaching a first successful transaction was **38.20%**.

The largest absolute user-count reduction occurred between KYC Started and KYC Completed, where the difference was 10,830 users.

This makes KYC a priority area for further investigation.

**Measurement note:** These stage counts represent distinct users observed at each stage. They are not necessarily a strictly chronological, user-by-user funnel unless event ordering is explicitly enforced.

---

# 5. Activation and Early User Behavior

The project distinguishes between two concepts of activation.

## Technical Activation

A user completes their first successful transaction.

## Behavioral Activation

A user establishes repeated meaningful product usage during the early lifecycle.

The analysis grouped users according to the number of successful transactions during their first seven days:

```text
0 transactions
1 transaction
2 transactions
3–4 transactions
5+ transactions
```

The latest D30 retention export showed:

| First-seven-day transactions | Users | D30 retained users | D30 retention |
|---|---:|---:|---:|
| 0 | 35,380 | 321 | 1.10% |
| 1 | 7,050 | 312 | 5.24% |
| 2 | 3,629 | 277 | 9.03% |
| 3–4 | 3,031 | 298 | 11.72% |
| 5+ | 910 | 125 | 16.11% |

The observed pattern is clear: users with more successful transactions during their first seven days also show higher D30 retention in this dataset.

This is an association, not proof that encouraging additional transactions will necessarily cause retention to increase.

The findings can help identify opportunities for:

- Lifecycle messaging
- Product education
- Onboarding experiments
- Activation strategy
- Retention interventions

---

# 6. The KYC Incident

## Problem

KYC is a critical stage in the PulsePay onboarding journey.

Users who cannot complete identity verification cannot progress normally toward downstream product usage.

The analysis segmented KYC performance across:

- Device type
- App version
- Failure reason
- Time

A major performance gap was identified in:

> **Android app version 5.4**

## Evidence

The latest pipeline evidence reported:

| Metric | Android 5.4 |
|---|---:|
| KYC attempts | 5,129 |
| Completed KYC | 2,805 |
| Document-upload errors | 1,420 |
| KYC completion rate | 54.69% |

Android 5.3 was selected as the reference version.

Its KYC completion rate was:

**76.18%**

Therefore:

```text
76.18% reference completion
−
54.69% affected completion
=
21.49 percentage-point gap
```

The affected segment also showed elevated document-upload errors.

This suggests a plausible failure mechanism:

```text
Android 5.4
    ↓
Elevated document-upload errors
    ↓
Lower KYC completion
    ↓
Fewer users progressing toward activation
```

However, this evidence identifies an investigation priority rather than proving that the app version caused the deterioration.

Network connectivity, device characteristics, operating-system differences, and other factors could also contribute.

---

# 7. Estimating Business Impact

To translate the conversion problem into potential business impact, Android 5.3 was used as a counterfactual reference baseline.

The calculation asked:

> **How many Android 5.4 users might have completed KYC if the segment had performed at the Android 5.3 reference rate?**

## Expected completions at reference performance

```text
5,129 KYC attempts
×
76.18% reference completion rate
≈
3,907 expected KYC completions
```

Actual completions:

```text
2,805
```

Estimated difference:

```text
3,907
−
2,805
=
1,102 estimated additional KYC completions
```

The observed post-KYC activation rate was 62.75%.

Applying this rate:

```text
1,102
×
62.75%
≈
692 estimated additional activated users
```

## Interpretation

The analysis estimated:

> **Approximately 1,102 additional users might have completed KYC and approximately 692 might have reached downstream activation if Android 5.4 had performed at the Android 5.3 reference rate.**

This is a counterfactual estimate.

It does not prove that the app version alone caused exactly 1,102 lost KYC completions or 692 lost activated users.

The estimate depends on the assumption that Android 5.3 provides a reasonable comparison baseline for Android 5.4.

---

# 8. Product Recommendation for the Incident

## Immediate

1. Investigate the Android 5.4 document-upload flow.
2. Compare the affected implementation with Android 5.3.
3. Review technical logs for upload failures.
4. Validate device-, operating-system-, and network-specific failure patterns.

## Recovery

5. Release a fix through a controlled rollout, if the investigation confirms an issue.
6. Monitor KYC completion and document-upload errors.
7. Compare post-fix performance with the reference version.

## Prevention

8. Add automated monitoring by app version.
9. Alert on meaningful KYC deterioration.
10. Include conversion guardrails in future mobile releases.

The broader product lesson is:

> **Aggregate metrics can hide severe segment-level product failures.**

---

# 9. Acquisition Quality

Acquisition channels were evaluated across:

- Acquired users
- KYC completion
- Activation
- D30 retention

This was designed to challenge a common growth assumption:

> **The channel bringing the most users is not necessarily bringing the most valuable users.**

The latest exported results were:

| Acquisition channel | Users | KYC completion | Activation | D30 retention | Quality score |
|---|---:|---:|---:|---:|---:|
| Referral | 8,585 | 64.72% | 44.37% | 3.92% | 32.26 |
| Paid Search | 8,931 | 61.11% | 38.62% | 3.38% | 29.02 |
| Partnership | 4,515 | 61.24% | 38.34% | 3.05% | 28.81 |
| Organic | 13,924 | 59.95% | 38.02% | 3.39% | 28.55 |
| Influencer | 3,969 | 59.64% | 38.40% | 2.95% | 28.47 |
| Paid Social | 10,076 | 55.83% | 32.70% | 2.42% | 25.21 |

A relative acquisition-quality score was calculated using:

```text
40% Activation Rate
+
40% D30 Retention
+
20% KYC Completion
```

The weighting reflects a product-prioritization choice. It is not a universal formula.

Referral had the highest quality score in the latest export, while Paid Social had the lowest.

This suggests that acquisition decisions should consider downstream user quality, not just signup volume.

## Product Recommendation

Acquisition decisions should consider:

```text
Acquisition Volume
        +
Activation Quality
        +
Retention Quality
```

rather than:

```text
Sign-ups alone
```

A high-volume channel with weaker downstream behavior may be less valuable than a smaller channel producing more engaged users.

The quality score should be treated as a comparative prioritization measure, not a direct measure of profitability or customer lifetime value.

---

# 10. Cohort Retention

Monthly signup cohorts were analyzed based on successful transaction activity.

The cohort framework tracks:

```text
M0 = Signup month
M1 = One month after signup
M2 = Two months after signup
...
M5 = Five months after signup
```

The latest export showed:

| Signup cohort | Cohort size | M0 | M1 | M2 | M3 | M4 | M5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Jan 2026 | 8,965 | 32.81% | 18.63% | 1.55% | 0.07% | 0.00% | 0.00% |
| Feb 2026 | 8,064 | 32.25% | 21.07% | 1.26% | 0.04% | 0.00% | — |
| Mar 2026 | 8,838 | 31.10% | 18.49% | 1.44% | 0.06% | — | — |
| Apr 2026 | 8,647 | 32.08% | 20.06% | 1.13% | — | — | — |
| May 2026 | 8,910 | 30.56% | 17.25% | — | — | — | — |
| Jun 2026 | 6,576 | 32.13% | — | — | — | — | — |

Later-month cells for recent cohorts are unavailable because those cohorts have not yet had enough observation time.

They should be interpreted as not yet observed, not as zero retention.

The exported results also show a sharp decline in activity after M1. This deserves further investigation before drawing conclusions about long-term retention.

Cohort analysis helps answer:

- Are newer users retaining better?
- Is product quality improving over time?
- Are acquisition changes affecting user quality?
- Did a product incident affect specific cohorts?

---

# 11. The KYC Experiment

A separate experiment evaluated a proposed KYC experience.

## Hypothesis

> Simplifying the KYC experience will improve KYC completion without increasing support contacts or harming downstream activation.

## Primary Metric

**KYC Completion Rate**

## Guardrail Metric

**Support Contact Rate**

## Downstream Metric

**Activation Rate**

---

# 12. Experiment Results

The latest exported experiment scorecard contained 6,032 assigned users.

| Variant | Assigned users | KYC completion | Support contact | Activation |
|---|---:|---:|---:|---:|
| Control | 3,012 | 62.55% | 13.48% | 39.18% |
| Treatment | 3,020 | 62.48% | 13.64% | 39.60% |

## Primary Metric

The observed KYC completion difference was:

```text
Treatment: 62.48%
Control:   62.55%

Absolute difference:
−0.07 percentage points
```

The treatment did not improve the primary metric in the latest scorecard.

## Guardrail Metric

```text
Treatment support contact: 13.64%
Control support contact:   13.48%

Difference:
+0.16 percentage points
```

Support contact was slightly higher in treatment.

## Downstream Metric

```text
Treatment activation: 39.60%
Control activation:   39.18%

Difference:
+0.42 percentage points
```

Activation was slightly higher in treatment.

These are descriptive differences. They should not be interpreted as statistically established effects without a matching inferential analysis on the same assignment population.

---

# 13. Experiment Integrity and Interpretation

The latest scorecard reported:

```text
Total assigned users: 6,032

Control:   3,012
Treatment: 3,020
```

The expected allocation under a 50/50 design would be 3,016 users per variant.

The current scorecard counts are close to this expected allocation.

However, earlier experiment documentation contained a different allocation:

```text
Control:   3,102
Treatment: 2,930
```

That older allocation produced an SRM warning with a reported p-value of 0.0268.

These two populations cannot be treated as the same experiment result without reconciling their source and analysis logic.

Therefore, the older SRM result and older inferential statistics are not used as conclusions for the latest scorecard.

**Important analytical distinction:** The latest descriptive scorecard does not, by itself, provide a valid p-value or confidence interval for the treatment effect.

A statistical test should be recalculated using the exact same experiment population, metric definitions, and eligibility rules as the scorecard before making an inferential rollout decision.

---

# 14. Experiment Decision

## Decision

> **DO NOT CLAIM A WINNER BASED ON THE CURRENT SCORECARD.**

The treatment showed:

- Slightly lower KYC completion
- Slightly higher support contact
- Slightly higher activation

The primary metric did not improve, and the descriptive differences do not establish a causal treatment effect.

## Recommended Next Steps

1. Reconcile the latest scorecard population with the experiment analysis output.
2. Verify assignment integrity and instrumentation.
3. Confirm the primary metric and guardrail definitions.
4. Define a minimum detectable effect.
5. Perform an experiment power calculation.
6. Recalculate statistical significance and confidence intervals on the matching population.
7. Continue or rerun the experiment if the setup and analysis are valid.
8. Do not ship solely because one downstream metric is numerically higher.

---

# 15. Dashboard Design

The Power BI report is organized around product decisions rather than isolated charts.

## Page 1 — Executive Overview

Answers:

> What is the current state of the product?

Includes:

- Executive KPIs
- North Star trend
- Onboarding funnel
- Acquisition quality

## Page 2 — Growth & Retention

Answers:

> What behaviors and acquisition sources are associated with durable usage?

Includes:

- Early behavior vs D30 retention
- Cohort retention
- Acquisition-channel quality

## Page 3 — KYC Incident

Answers:

> Where did KYC performance deteriorate, what is the likely mechanism, and what is the estimated impact?

Includes:

- Version-level KYC performance
- Document-upload errors
- Weekly trends
- Incident impact

## Page 4 — Experiment Lab

Answers:

> Should the proposed KYC experience be rolled out?

Includes:

- Experiment allocation
- Primary metric
- Guardrail metric
- Downstream activation
- Statistical evidence
- Product decision

---

# 16. Analytical Principles Demonstrated

This project applies several principles of responsible product analytics.

## Do not confuse correlation with causation

Early transaction behavior may predict retention without necessarily causing it.

## Do not confuse directional movement with statistical evidence

A metric being higher does not automatically make a treatment a winner.

## Validate experiment populations before interpreting outcomes

Assignment integrity and consistent population definitions are essential before drawing experiment conclusions.

## Segment aggregate metrics

Aggregate product health can hide severe problems affecting specific platforms or versions.

## Translate metrics into decisions

The purpose of analysis is not simply to produce charts.

The final question is:

> **What should the product team do next?**

---

# 17. Limitations

## Synthetic Data

PulsePay is fictional, and the dataset is synthetically generated for portfolio purposes.

## Counterfactual Incident Estimate

The incident-impact estimate assumes Android 5.3 is a reasonable reference for Android 5.4.

## Observational Retention Analysis

The relationship between early product behavior and retention does not establish causality.

## Cohort Retention

The sharp decline in later-month cohort activity requires further investigation before it can support a long-term retention conclusion.

## Experiment Population Consistency

Older experiment documentation and the latest scorecard contain different assignment counts and metric results. These must be reconciled before reporting a definitive inferential result.

## Statistical Power

A non-significant result does not prove that a treatment has exactly zero effect. An experiment may lack sufficient power to detect smaller effects.

---

# 18. Final Product Recommendations

Based on the latest exported analysis:

1. **Prioritize investigation of the Android 5.4 document-upload experience.**
2. **Implement version-level KYC monitoring and alerting.**
3. **Track meaningful product usage as a core activation signal.**
4. **Investigate interventions that help users establish early repeated usage.**
5. **Evaluate acquisition sources using downstream quality, not volume alone.**
6. **Investigate the sharp decline in later-month cohort activity.**
7. **Reconcile experiment populations before making statistical or rollout claims.**
8. **Define power and minimum detectable effect before future experiments.**
9. **Avoid rollout decisions based solely on directional metric movement.**

---

# Conclusion

The PulsePay project demonstrates an end-to-end product analytics workflow:

```text
Measure product health
        ↓
Identify funnel friction
        ↓
Segment the problem
        ↓
Investigate root cause
        ↓
Estimate business impact
        ↓
Understand retention behavior
        ↓
Evaluate acquisition quality
        ↓
Assess a proposed solution
        ↓
Quantify uncertainty
        ↓
Make a product recommendation
```

The central objective was not to create the largest possible dashboard.

It was to demonstrate how a Product Analyst can move from:

> **"What happened?"**

to:

> **"Why might it have happened?"**

and finally:

> **"What should the product team do next?"**