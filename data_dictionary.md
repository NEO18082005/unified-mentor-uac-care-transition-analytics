# Data Dictionary

| Field | Meaning | Type | Use in analysis |
|---|---|---|---|
| `Date` | Reporting date | Date | Filter and trend axis |
| `Children apprehended and placed in CBP custody*` | Daily intake volume | Integer | Pipeline inflow and throughput denominator |
| `Children in CBP custody` | Active CBP care load | Integer | Transfer-efficiency denominator |
| `Children transferred out of CBP custody` | Flow from CBP into HHS | Integer | Transfer-efficiency numerator and HHS inflow |
| `Children in HHS Care` | Active HHS care load | Integer | Discharge-effectiveness denominator and backlog stock |
| `Children discharged from HHS Care` | Reported HHS exits / sponsor placements | Integer | Discharge-effectiveness numerator and throughput |

## Data quality notes

- The source contains 49 reporting observations between October 9 and December 21, 2025.
- Reporting dates are not continuous daily observations.
- The dataset contains aggregate counts and no child-level identifiers or timestamps.
- Flows and stocks are not cohort-linked, so flow ratios are operational indicators rather than individual probabilities.
