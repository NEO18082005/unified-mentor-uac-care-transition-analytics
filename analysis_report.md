# Care Transition Efficiency & Placement Outcome Analytics

## 1. Background

The UAC program is a multi-stage care and reunification pipeline. Children move from apprehension and CBP custody to HHS care, then to discharge and sponsor placement. Monitoring only the active stock can hide delays, uneven handoffs, and periods where inflows exceed successful exits.

This analysis reframes the source data around process movement and backlog pressure.

## 2. Data and preparation

The source file is `HHS_Unaccompanied_Alien_Children_Program.csv`, shared through the provided [Google Drive link](https://drive.google.com/file/d/1xZo782T4EfnkC0BmCwJTb0DZYYHoOXKm/view?usp=sharing). It contains 49 reporting observations from October 9 through December 21, 2025.

The dataset includes:

- daily reported apprehensions placed in CBP custody;
- children in CBP custody;
- children transferred out of CBP custody;
- children in HHS care; and
- children discharged from HHS care.

The date field was parsed as a calendar date and the numeric fields were converted to integers. Derived fields include transfer efficiency, discharge effectiveness, net HHS flow, month, and weekday.

## 3. KPI definitions

### Transfer Efficiency Ratio

`Total transfers out of CBP custody ÷ total children in CBP custody`

This is a weighted ratio across observations. It is a process signal, not an individual-level probability.

### Discharge Effectiveness

`Total discharges from HHS care ÷ total children in HHS care`

The denominator is a stock measure, so this percentage should be interpreted as a stock-to-flow indicator.

### Pipeline Throughput

`Total HHS discharges ÷ total apprehensions reported`

This ratio compares reported outflow and inflow. It is not a cohort completion rate because the source does not identify the same children across records.

### Backlog Accumulation

`Transfers − discharges`

Positive values indicate that more children entered HHS care through the reported transfer flow than exited through reported discharges in that observation.

### Outcome Stability Score

`100 × (1 − coefficient of variation of daily discharges)`, bounded to 0–100.

Higher values indicate more consistent discharge volumes. This is a monitoring index created for this project, not an official HHS measure.

## 4. Exploratory findings

### System movement

Across the 49 observations, reported apprehensions totaled 357, transfers totaled 495, and discharges totaled 462. The HHS care stock rose from 2,192 on October 9 to 2,484 on December 21, an increase of 292 children or 13.3%.

The net HHS flow was positive in 26 observations and negative in 23. The total positive imbalance across observations was 33 children. The largest positive single-observation imbalance occurred on November 23, when 22 transfers were reported against 1 discharge, a net increase of 21.

### Transfer performance

The weighted transfer efficiency ratio for the full period was 29.4%. Monthly performance declined from 39.2% in October to 27.5% in November and 22.8% in December.

The highest observed daily transfer ratio was 96.3% on October 23, with 26 transfers against 27 children in CBP custody. The lowest was 9.3% on December 10, with 5 transfers against 54 children in CBP custody. These extremes show why trend and threshold monitoring are more useful than relying on a single daily value.

### Discharge performance

The weighted discharge effectiveness ratio was 0.40%. Discharges averaged 9.4 per reporting observation, with a population standard deviation of 3.9 and a coefficient of variation of 0.42. This produces an Outcome Stability Score of 58.5/100.

The highest reported discharge count was 19 on November 6. The lowest was 0 on November 30. The monthly weighted discharge effectiveness ratio was 0.47% in October, 0.36% in November, and 0.39% in December.

### Weekday and weekend pattern

The data does not contain a balanced set of calendar days, so weekday comparisons are descriptive only. Sunday observations had the highest weighted transfer ratio at 37.4% and the highest average net HHS flow at +3.9. Thursday observations had the highest weighted discharge effectiveness at 0.51% and nearly balanced average net flow at +0.1.

## 5. Bottleneck interpretation

The primary bottleneck signal is accumulation in HHS care, not a sustained decline in every flow measure. HHS stock rose across the period even though the selected observation-level imbalance was relatively small. This suggests that the starting stock, earlier unobserved inflows, reporting gaps, or timing differences may contribute to the stock trend.

The October-to-December decline in transfer efficiency is the clearest process warning. A falling transfer ratio alongside a rising HHS stock warrants investigation of CBP handoff capacity, transportation, screening completion, bed availability, and reporting cadence.

Discharge volume is comparatively stable but low relative to the HHS stock. The stability score is moderate rather than strong because daily discharge counts range from 0 to 19.

## 6. Recommendations

1. **Create a weekly exception workflow.** Flag reporting observations where net HHS flow is positive, transfer efficiency falls below the chosen floor, or discharge effectiveness falls below the chosen floor.
2. **Decompose the handoff delay.** Add timestamps for apprehension, CBP transfer decision, physical transfer, HHS intake, sponsor approval, and discharge.
3. **Measure aging directly.** Add case-age bands and median/90th percentile days in CBP and HHS care.
4. **Segment bottlenecks.** Add location, facility, transfer reason, sponsor readiness, and documentation status.
5. **Review December deterioration.** Compare operational staffing, transport availability, holidays, screening demand, and reporting completeness with October and November.
6. **Use the dashboard as a monitoring layer.** Keep the threshold controls configurable and document any policy floors used by stakeholders.

## 7. Limitations

- The dataset contains aggregate observations rather than individual child records.
- Reporting dates are not daily; gaps prevent reliable calendar-day rate calculations.
- The source does not identify whether a transfer and discharge refer to the same children.
- Stock measures and flow measures use different units of observation, so ratios are operational indicators rather than precise probabilities.
- No facility, geography, case-mix, sponsor, or reason-for-delay fields are available.

## 8. Conclusion

The period shows a growing HHS care stock, declining transfer efficiency, and moderate variability in discharge performance. The dashboard operationalizes these signals with date filters, ratio/count toggles, bottleneck charts, and threshold alerts. The next analytical step should be to add individual-level timestamps and segmentation fields so the program can move from directional monitoring to measured transition-time improvement.
