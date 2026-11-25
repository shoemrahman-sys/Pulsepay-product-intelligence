# PulsePay — End-to-End Product Analytics Case Study

> An end-to-end product analytics portfolio project investigating user activation, retention, acquisition quality, a KYC conversion incident, and an A/B experiment for a fictional fintech payments product.

---

## Project Overview

PulsePay is a fictional digital payments product used to simulate the type of analytical problems faced by Product Analysts in consumer fintech.

The project analyzes the complete user journey:

**Acquisition → Signup → KYC → Activation → Transaction → Retention**

The objective was not simply to build a dashboard. The project demonstrates an end-to-end product analytics workflow:

1. Define product and business questions.
2. Generate a synthetic product dataset.
3. Model the data in MySQL.
4. Analyze product health and user behavior with SQL.
5. Diagnose a product conversion incident.
6. Evaluate acquisition quality.
7. Perform cohort and retention analysis.
8. Evaluate an A/B experiment and its statistical considerations.
9. Build a decision-oriented Power BI dashboard.
10. Translate analytical findings into product recommendations.

---

## Business Context

PulsePay's product team wants to understand three major areas.

### 1. Activation and Retention

Where do users drop out of the onboarding journey, and which early behaviors are associated with stronger later retention?

### 2. KYC Conversion Incident

Why did KYC completion deteriorate for a segment of users, and what was the potential downstream business impact?

### 3. Product Experimentation

Did a simplified KYC experience improve completion without negatively affecting support contacts or downstream activation?

---

## Key Findings

### 1. Android 5.4 showed a major KYC performance gap

The investigation identified Android app version `5.4` as a materially underperforming segment.

| Metric | Android 5.4 |
|---|---:|
| KYC attempts | 5,129 |
| Actual KYC completions | 2,805 |
| Failed attempts | 1,420 |
| Abandoned attempts | 904 |
| Document-upload errors | 1,420 |
| Actual KYC completion rate | 54.69% |
| Android 5.3 reference completion rate | 76.18% |
| Completion-rate gap | -21.49 percentage points |

Android 5.4 had substantially lower completion than Android 5.3 and an elevated document-upload error count.

This provides a plausible technical investigation hypothesis, but it does not independently prove that the app version caused the decline.

**Product recommendation:** Prioritize investigation of the Android document-upload flow, compare the affected release with the previous stable version, and introduce version-level monitoring for KYC completion and upload failures.

### 2. The incident may have had meaningful downstream impact

Using Android 5.3 as a reference baseline:

| Metric | Estimate |
|---|---:|
| Android 5.4 attempts | 5,129 |
| Actual KYC completions | 2,805 |
| Expected completions at reference performance | 3,907 |
| Estimated additional KYC completions | 1,102 |
| Observed post-KYC activation rate | 62.75% |
| Estimated additional activated users | 692 |

The estimates are based on:

```text
Expected Completions
=
Android 5.4 Attempts
×
Android 5.3 Completion Rate
```

```text
Estimated Lost KYC Completions
=
Expected Completions
-
Actual Completions
```

```text
Estimated Lost Activated Users
=
Estimated Lost KYC Completions
×
Observed Post-KYC Activation Rate
```

These figures are counterfactual estimates rather than proven causal losses.

The analysis suggests that product-quality issues during onboarding may propagate beyond the immediate funnel step and affect downstream activation.

### 3. Early product behavior is associated with stronger retention

Users were segmented according to the number of successful transactions completed during their first seven days.

| First-7-Day Successful Transactions | Users | D30 Retention |
|---|---:|---:|
| 0 | 35,380 | 1.10% |
| 1 | 7,050 | 5.24% |
| 2 | 3,629 | 9.03% |
| 3–4 | 3,031 | 11.72% |
| 5+ | 910 | 16.11% |

Users with more successful transactions during their first seven days showed higher observed D30 retention.

This provides a behavioral framework for activation:

> Activation should represent meaningful early product value, not merely account creation.

Because this analysis is observational, the relationship should not be interpreted as proof that increasing early transaction frequency will automatically cause higher retention.

### 4. Acquisition volume and acquisition quality are different

Acquisition channels were evaluated using downstream product outcomes rather than signup volume alone.

| Channel | Users | KYC Completion | Activation | D30 Retention | Quality Score |
|---|---:|---:|---:|---:|---:|
| Referral | 8,585 | 64.72% | 44.37% | 3.92% | 32.26 |
| Paid Search | 8,931 | 61.11% | 38.62% | 3.38% | 29.02 |
| Partnership | 4,515 | 61.24% | 38.34% | 3.05% | 28.81 |
| Organic | 13,924 | 59.95% | 38.02% | 3.39% | 28.55 |
| Influencer | 3,969 | 59.64% | 38.40% | 2.95% | 28.47 |
| Paid Social | 10,076 | 55.83% | 32.70% | 2.42% | 25.21 |

A weighted quality index was created:

- 40% Activation
- 40% D30 Retention
- 20% KYC Completion

Referral has the highest composite score in the latest export, while Paid Social has the lowest.

**Product implication:** Marketing investment should consider downstream user quality instead of optimizing only for top-of-funnel acquisition volume.

The score is a prioritization framework, not a direct measure of profitability or customer lifetime value.

### 5. The KYC experiment has not established a winner

The latest experiment scorecard includes **6,032 assigned users**.

| Metric | Control | Treatment |
|---|---:|---:|
| Assigned users | 3,012 | 3,020 |
| KYC completion rate | 62.55% | 62.48% |
| Support contact rate | 13.48% | 13.64% |
| Activation rate | 39.18% | 39.60% |

Observed differences:

- KYC completion: -0.07 percentage points
- Support contact: +0.16 percentage points
- Activation: +0.42 percentage points

The latest assignment counts are close to the intended 50/50 allocation:

- Expected control: 3,016
- Expected treatment: 3,016
- Approximate SRM chi-square: 0.0106
- Approximate SRM p-value: 0.918

These counts do not indicate a statistically significant allocation imbalance, assuming the scorecard represents the complete eligible assignment population.

**Important experiment limitation:** The latest descriptive scorecard has not yet been reconciled with the older inferential analysis. The older analysis reported a different allocation and different metric rates. Its p-values and confidence interval must not be reused as the statistical results for the latest scorecard.

**Experiment decision:**

> Do not declare the treatment a winner.

The latest descriptive differences do not establish a treatment effect. The experiment population must be reconciled before calculating and publishing the corresponding inferential results.

---

## Product Analytics Framework

The project follows this analytical structure:

```text
Product Health
      ↓
Activation Funnel
      ↓
Root-Cause Investigation
      ↓
Retention & Cohorts
      ↓
Acquisition Quality
      ↓
Experimentation
      ↓
Product Decision
```

---

## Dashboard

The Power BI report is structured as a four-page product analytics command center.

### 1. Executive Overview

Focuses on:

- Product KPIs
- North Star metric
- Onboarding funnel
- Acquisition quality
- Executive product findings

### 2. Growth & Retention

Focuses on:

- Early product behavior
- D30 retention
- Monthly cohort retention
- Acquisition-channel quality

### 3. KYC Incident Investigation

Focuses on:

- KYC performance by app version
- Document-upload failures
- Weekly KYC trends
- Estimated business impact
- Product recommendations

### 4. Experiment Lab

Focuses on:

- Control vs treatment allocation
- Primary metric
- Guardrail metric
- Downstream activation
- Experiment validation
- Experiment decision

---

### 01 — Executive Overview

![Executive Overview](screenshots/01-executive-overview.png)

### 02 — Growth & Retention

![Growth & Retention](screenshots/02-growth-retention.png)

### 03 — KYC Incident Investigation

![KYC Incident Investigation](screenshots/03-kyc-incident-investigation.png)

### 04 — Experiment Lab

![Experiment Lab](screenshots/04-experiment-lab.png)

---

## Executive Product Health

Latest exported results:

| Metric | Result |
|---|---:|
| Registered users | 50,000 |
| Total transactions | 65,047 |
| Successful transactions | 61,179 |
| Transaction success rate | 94.05% |
| Successful transacting users | 19,102 |
| Successful transactor rate | 38.20% |
| Successful transaction value | 22,259,562.41 |

The overall registration-to-successful-transaction conversion is 38.20%.

The largest absolute onboarding drop occurs between KYC Started and KYC Completed, with 10,830 fewer users reaching completion.

---

## North Star Metric

The primary product-usage metric used in the project is:

### Weekly Successful Transacting Users

A user is counted when they complete at least one successful transaction during an ISO calendar week.

This metric was selected because it represents meaningful product usage rather than passive account ownership.

---

## Activation Framework

The project distinguishes between:

### Technical activation

The user completes a first successful transaction.

### Behavioral activation

The user establishes repeated product usage during the early lifecycle.

The analysis evaluates successful transactions during the first seven days as a potential behavioral activation signal and compares this behavior with D30 retention.

The overall 38.20% registration-to-activation metric is cumulative. It should not be interpreted as a seven-day activation rate.

---

## Experiment Methodology

The KYC experiment was evaluated using:

- Experiment allocation validation
- Duplicate-assignment checks
- Sample-ratio-mismatch testing
- Primary metric comparison
- Absolute lift
- Relative lift
- Two-proportion z-test methodology
- P-value interpretation
- Confidence interval interpretation
- Guardrail metrics
- Downstream activation

The latest scorecard provides descriptive metric rates. Its inferential results still require reconciliation with the underlying experiment population.

A higher treatment metric was not automatically interpreted as a successful experiment.

Statistical uncertainty and experiment integrity are part of the final decision framework.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Database | MySQL 8 |
| SQL Development | MySQL Workbench |
| Data Generation | Python |
| Data Analysis | Python, Pandas |
| Statistical Testing | Python |
| Visualization | Power BI |
| Version Control | Git |
| Repository | GitHub |

---

## Repository Structure

```text
pulsepay-product-analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│       └── final_results/
│
├── dashboard/
│   └── PulsePay_Product_Analytics.pbix
│
├── docs/
│   ├── case-study.md
│   ├── data-dictionary.md
│   ├── methodology.md
│   ├── metric_dictionary.md
│   └── project_charter.md
│
├── python/
│   ├── data_generation/
│   │   ├── generate_pulsepay_data.py
│   │   └── load_data_to_mysql.py
│   │
│   └── analysis/
│       ├── experiment_analysis.py
│       └── export_final_results.py
│
├── sql/
│   ├── 01_setup/
│   ├── 02_analysis/
│   │   ├── 001_product_health.sql
│   │   ├── 002_activation_funnel.sql
│   │   ├── 003_root_cause_analysis.sql
│   │   ├── 004_retention_analysis.sql
│   │   ├── 005_cohort_analysis.sql
│   │   └── 006_acquisition_analysis.sql
│   │
│   ├── 03_experiments/
│   │   └── 001_kyc_ab_test.sql
│   │
│   └── 04_dashboard/
│       ├── 001_create_dashboard_views.sql
│       └── 002_create_incident_impact_view.sql
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Analytical Outputs

The project includes reproducible exports for:

- Executive KPIs
- Weekly North Star metric
- Onboarding funnel
- KYC performance by device and app version
- Weekly KYC trends
- Acquisition quality
- Activation and retention
- Cohort retention
- Experiment scorecard
- KYC incident impact

These outputs are stored under:

```text
data/processed/final_results/
```

---

## Reproducibility

### 1. Create and activate a Python virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate the synthetic dataset

```bash
python python/data_generation/generate_pulsepay_data.py
```

### 4. Create the MySQL schema and load the data

Run the setup SQL scripts from:

```text
sql/01_setup/
```

### 5. Run the analysis

Run the SQL files from:

```text
sql/02_analysis/
sql/03_experiments/
```

### 6. Create dashboard views

Run:

```bash
sql/04_dashboard/001_create_dashboard_views.sql
sql/04_dashboard/002_create_incident_impact_view.sql
```

### 7. Run statistical experiment analysis

```bash
python python/analysis/experiment_analysis.py
```

### 8. Export final analytical results

```bash
python python/analysis/export_final_results.py
```

---

## Data Disclosure

This project uses a **synthetic dataset generated specifically for portfolio and educational purposes**.

PulsePay is a fictional product.

The project does not contain real customer, financial, KYC, or personally identifiable information.

The dataset was designed to simulate product analytics patterns, including:

- Funnel drop-off
- User activation
- Retention behavior
- Acquisition-channel differences
- App-version performance differences
- KYC failure patterns
- Product experimentation

Because the data is synthetic, findings demonstrate analytical methodology and decision-making rather than real-world business performance.

---

## Analytical Limitations

### Synthetic data

The patterns originate from a simulated dataset and should not be interpreted as evidence about a real fintech product.

### Observational retention analysis

The relationship between early transaction behavior and later retention is associative and does not establish causality.

### Funnel interpretation

Distinct user counts at each stage do not independently prove exact chronological progression for every user.

### Incident impact estimation

The Android 5.3 completion rate is used as a reference counterfactual for Android 5.4. The estimated impact assumes that the affected segment could reasonably have performed at the reference rate.

### Version attribution

The recorded signup app version may not represent the app version at the time of the KYC attempt.

### Experiment population reconciliation

The latest experiment scorecard and older inferential analysis use different assignment counts and metric rates. Inferential results must be reconciled before making a definitive experiment claim.

### Cohort maturity

Recent cohorts have incomplete observation periods. Missing future months must not be interpreted as zero retention.

---

## Product Recommendations

Based on the analysis:

1. **Investigate and remediate the Android 5.4 KYC document-upload experience.**
2. **Introduce automated KYC monitoring segmented by device and app version.**
3. **Track behavioral activation rather than relying only on account creation.**
4. **Design interventions that help new users establish meaningful early product usage.**
5. **Evaluate acquisition channels using downstream activation and retention quality.**
6. **Do not ship experiment treatments based only on directional metric movement.**
7. **Reconcile the latest experiment population before making rollout conclusions.**
8. **Define experiment power and minimum detectable effect before future tests.**

---

## What This Project Demonstrates

This project demonstrates practical experience with:

- Product metric definition
- North Star metrics
- Funnel analysis
- Activation analysis
- Retention analysis
- Cohort analysis
- Root-cause investigation
- Product incident analysis
- Acquisition quality analysis
- A/B testing methodology
- Statistical significance
- Confidence intervals
- Sample-ratio-mismatch checks
- SQL analytics
- Python analysis
- MySQL data modeling
- Power BI reporting
- Product recommendations
- Analytical limitations and responsible interpretation
- Translating analysis into product decisions

The project also includes a Product Requirements Document (PRD) proposing a response to the Android 5.4 KYC drop-off.

[Add the actual PRD link here.]

---

## Project Status

- **Core analytics:** Complete
- **SQL dashboard data layer:** Complete
- **Python automation and exports:** Executed successfully
- **Power BI dashboard:** Complete
- **Case study and methodology documentation:** Updated
- **Metric dictionary:** Updated
- **Experiment inferential reconciliation:** Pending

---

## Author

**Author-name : Abdul Rahman Shoem

Product Analytics | Data Analytics | SQL | Python | Power BI

GitHub: https://github.com/shoemrahman-sys
