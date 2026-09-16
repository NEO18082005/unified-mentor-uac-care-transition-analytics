# Care Transition Efficiency & Placement Outcome Analytics

This project analyzes the Unified Mentor UAC dataset as a care-transition pipeline:

CBP custody → HHS care → sponsor placement

## Included deliverables

- `app.py` — interactive Streamlit dashboard
- `data/HHS_Unaccompanied_Alien_Children_Program.csv` — cleaned source dataset extracted from the shared Drive file
- `analysis_report.md` — research-style EDA, findings, limitations, and recommendations
- `executive_summary.md` — stakeholder-facing summary
- `requirements.txt` — Python dependencies
- `data_dictionary.md` — field definitions and limitations
- `tests/test_data_quality.py` — automated source-data checks

## Run the dashboard

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Select **New app**, choose the repository, and set the main file to `app.py`.
4. Click **Deploy**. Streamlit will install the dependencies from `requirements.txt`.

The application does not require secrets, API keys, or external databases.

## Quality checks

Run the included checks with:

```bash
python -m pytest tests
```

## KPI definitions

- Transfer Efficiency Ratio = total transfers out of CBP custody / total children in CBP custody.
- Discharge Effectiveness = total discharges from HHS care / total children in HHS care.
- Pipeline Throughput = total HHS discharges / total apprehensions reported.
- Backlog Accumulation = transfers minus discharges; positive values indicate HHS-stage accumulation pressure.
- Outcome Stability Score = 100 × (1 − coefficient of variation of daily discharges), bounded to 0–100.

## Important interpretation note

The dataset contains aggregate reporting snapshots rather than individual child records. It has 49 observations from October 9 through December 21, 2025, with gaps between reporting dates. Cumulative flow totals should not be interpreted as a cohort-level conversion rate or as proof that the same children are represented in each stage.
