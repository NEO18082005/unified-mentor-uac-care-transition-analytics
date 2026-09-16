# Care Transition Efficiency & Placement Outcome Analytics

## 1. Background and objective

The Unaccompanied Alien Children (UAC) program is a multi-stage care and reunification pipeline. Children are referred from CBP, enter HHS/ORR care, receive screening and case-management services, and may then be released to a vetted sponsor. This study evaluates movement through that pipeline rather than looking only at the number of children in care.

The objectives are to measure CBP-to-HHS transfer efficiency, evaluate discharge outcomes, identify periods of accumulation pressure, and provide an operational monitoring dashboard for stakeholders.

## 2. Data and preparation

The source is the provided `HHS_Unaccompanied_Alien_Children_Program.csv` file. It contains 720 valid reporting observations from January 12, 2023 through December 21, 2025. The downloaded file is ordered newest to oldest and contains blank trailing rows. The analysis removes rows without a reporting date, parses dates, removes thousands separators from numeric fields, sorts observations chronologically, and validates the six expected fields.

The source is an aggregate reporting series. It does not provide child-level identifiers, facility, geography, sponsor category, case age, or event timestamps. Consequently, the measures below are operational signals and not individual-level probabilities or time-to-placement estimates.

## 3. KPI definitions

### Transfer Efficiency Ratio

`Total transfers out of CBP custody ÷ total children in CBP custody`

This weighted ratio describes the observed transfer flow relative to the CBP custody stock.

### Discharge Effectiveness

`Total discharges from HHS care ÷ total children in HHS care`

This is a stock-to-flow indicator. It should not be read as the probability that a particular child is discharged.

### Pipeline Throughput

`Total HHS discharges ÷ total apprehensions reported`

This compares aggregate reported outflow and inflow. It is not a cohort completion rate because records are not linked across stages.

### Backlog Accumulation Signal

`Transfers − discharges`

Positive values indicate that the reported transfer flow exceeded the reported discharge flow in that observation. The dashboard also reports the change in the HHS stock between the first and last selected observations.

### Outcome Stability Score

`100 × (1 − coefficient of variation of reported discharges)`, bounded to 0–100.

This project-defined index summarizes consistency of discharge volume. It is not an official HHS measure. Higher values indicate more consistent reported discharge volumes.

## 4. Exploratory findings

### Overall movement

Across the 720 observations, the source reports 67,337 apprehensions, 92,641 transfers, and 124,853 discharges. The weighted transfer efficiency ratio is 75.03%, the weighted discharge effectiveness ratio is 2.86%, and the flow-comparison throughput ratio is 185.42%.

The HHS care stock decreased from 6,566 on January 12, 2023 to 2,484 on December 21, 2025, a net decrease of 4,082 children or 62.2%. Reported transfers exceeded discharges in 238 observations and discharges exceeded transfers in 475 observations. The aggregate transfer-minus-discharge signal is −32,212, which is consistent with the long-run reduction in the observed HHS stock but should not be treated as a cohort reconciliation.

### Year-over-year pattern

The weighted transfer ratio was 78.35% in 2023, 75.61% in 2024, and 50.41% in 2025. The weighted discharge effectiveness ratio was 3.33%, 2.92%, and 1.14%, respectively. These results show lower observed rates in 2025, although the 2025 period includes a transition in the underlying volumes and should be interpreted with the reporting coverage and stock levels in mind.

### Backlog and exception observations

The largest positive single-observation imbalance occurred on February 12, 2024, when 440 transfers and 234 discharges produced a net increase signal of 206. The largest negative imbalance occurred on January 11, 2024, when 11 transfers and 476 discharges produced a net decrease signal of 465.

Positive and negative daily signals alternate across the series, so a single high-pressure observation is not proof of a sustained backlog. The dashboard therefore combines daily bars with the HHS stock trend and user-defined alert thresholds.

### Discharge consistency

Reported discharges averaged 173.4 per observation with a population standard deviation of 125.6. This gives an Outcome Stability Score of 27.6/100 under the project definition. The maximum discharge count was 505 on August 31, 2023, while the minimum was 0 on November 30, 2025. The wide range indicates that volume consistency is a meaningful monitoring concern.

### Reporting cadence

There are 161 gaps longer than one calendar day, and the largest gap is 10 days. Weekday comparisons are therefore descriptive and not a balanced experiment. Friday has only two observations, while Tuesday, Thursday, and Wednesday have substantially more. The dashboard does not claim that a weekday causes faster or slower transitions.

## 5. Bottleneck interpretation

The full-period series suggests that the principal operational question is not simply whether total discharges are large. The more useful questions are whether transfers keep pace with CBP custody, whether discharges are consistent relative to HHS stock, and whether high-pressure observations persist.

The lower 2025 transfer and discharge effectiveness ratios warrant investigation of changes in referral mix, reporting coverage, intake and screening capacity, transportation, sponsor documentation, and discharge processing. The available aggregate data cannot identify which mechanism caused the change. Facility-level and case-level fields are required for that conclusion.

## 6. Recommendations

1. Use the dashboard thresholds to create a weekly exception queue for positive net HHS flow, low transfer efficiency, low discharge effectiveness, or low stability.
2. Add event timestamps for referral, CBP transfer decision, physical transfer, HHS intake, sponsor approval, and discharge to measure median and 90th-percentile transition time.
3. Add case-age bands, facility, region, sponsor category, documentation status, and reason-for-delay fields to locate bottlenecks.
4. Review the 2025 rate changes alongside operational staffing, transportation, screening demand, reporting completeness, and policy changes.
5. Reconcile stock and flow definitions with data owners before using any ratio as an official performance target.
6. Refresh the dashboard from the official HHS data source on a defined schedule and record the extraction date in each published analysis.

## 7. Limitations

- The data is aggregate and not child-level.
- Reporting dates are irregular, so calendar-day and weekday comparisons are unbalanced.
- Transfers and discharges are not linked to the same children.
- Stock and flow measures have different meanings and denominators.
- The project-defined stability score is a monitoring index, not an official program KPI.
- No causal claim about sponsor vetting, facility performance, or staffing can be made from this file alone.

## 8. Conclusion

The complete source covers January 2023 through December 2025 and shows a substantial reduction in observed HHS care stock, high aggregate transfer and discharge flows relative to the later-period stock levels, and low consistency in discharge volume. The Streamlit dashboard turns these signals into an interactive monitoring layer with independent start and end date controls, count/ratio KPI views, threshold alerts, flow visualization, trend charts, and bottleneck detail. The next improvement should be a timestamped, case-level data model that can measure actual time to transfer and safe sponsor release.
