# Executive Summary

## Care Transition Efficiency & Placement Outcome Analytics

### Period covered

January 12, 2023 through December 21, 2025, across 720 valid reporting observations.

### What the data shows

The HHS care stock decreased from 6,566 to 2,484 children, a net decrease of 4,082 children or 62.2%. Across the reporting observations, 67,337 apprehensions, 92,641 transfers, and 124,853 discharges were reported.

The weighted transfer efficiency ratio was 75.03%. The weighted discharge effectiveness ratio was 2.86%. The reported discharge-to-apprehension throughput ratio was 185.42%. Because the source is an aggregate snapshot series without child-level linkage, throughput is a flow comparison and not a cohort completion rate.

### Main operational signals

1. Transfer efficiency was 78.35% in 2023, 75.61% in 2024, and 50.41% in 2025.
2. Discharge effectiveness was 3.33% in 2023, 2.92% in 2024, and 1.14% in 2025.
3. Reported transfers exceeded discharges in 238 observations, while discharges exceeded transfers in 475 observations.
4. The largest positive single-observation imbalance occurred on February 12, 2024, with 440 transfers and 234 discharges.
5. Discharges averaged 173.4 per observation, ranging from 0 to 505. The project-defined Outcome Stability Score was 27.6/100.
6. Reporting cadence is irregular, with 161 gaps longer than one day. Weekday comparisons should therefore be treated as descriptive only.

### Recommended actions

- Use configurable thresholds to create a recurring exception queue for accumulation pressure and weak transition indicators.
- Add timestamps for referral, transfer, HHS intake, sponsor approval, and discharge to measure actual transition time.
- Add facility, region, case age, sponsor category, documentation status, and reason-for-delay fields.
- Review 2025 rate changes alongside operations and reporting completeness before assigning a cause.
- Treat flow ratios as monitoring signals until data owners confirm stock/flow definitions and cohort coverage.

### Data limitation

This project uses aggregate reporting observations, not linked child records. It supports directional monitoring and operational triage, but not individual-level causal analysis, cohort conversion rates, or precise time-to-placement estimates.
