from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="UAC Care Transition Analytics",
    page_icon="📊",
    layout="wide",
)

DATA_PATH = Path(__file__).parent / "data" / "HHS_Unaccompanied_Alien_Children_Program.csv"
APPREHENDED = "Children apprehended and placed in CBP custody*"
CBP_STOCK = "Children in CBP custody"
TRANSFERRED = "Children transferred out of CBP custody"
HHS_STOCK = "Children in HHS Care"
DISCHARGED = "Children discharged from HHS Care"


@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    for col in [APPREHENDED, CBP_STOCK, TRANSFERRED, HHS_STOCK, DISCHARGED]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.sort_values("Date").reset_index(drop=True)
    df["Net HHS flow"] = df[TRANSFERRED] - df[DISCHARGED]
    df["Transfer efficiency"] = df[TRANSFERRED].div(df[CBP_STOCK].replace(0, pd.NA))
    df["Discharge effectiveness"] = df[DISCHARGED].div(df[HHS_STOCK].replace(0, pd.NA))
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Weekday"] = df["Date"].dt.day_name()
    return df


def ratio(numerator: float, denominator: float) -> float:
    return float(numerator / denominator) if denominator else 0.0


def calculate_kpis(df: pd.DataFrame) -> dict:
    transfer_ratio = ratio(df[TRANSFERRED].sum(), df[CBP_STOCK].sum())
    discharge_ratio = ratio(df[DISCHARGED].sum(), df[HHS_STOCK].sum())
    throughput = ratio(df[DISCHARGED].sum(), df[APPREHENDED].sum())
    avg_discharge = df[DISCHARGED].mean() if len(df) else 0
    cv = (df[DISCHARGED].std(ddof=0) / avg_discharge) if avg_discharge else 0
    stability = max(0.0, min(100.0, 100 * (1 - cv)))
    return {
        "transfer_ratio": transfer_ratio,
        "discharge_ratio": discharge_ratio,
        "throughput": throughput,
        "backlog_change": float(df[HHS_STOCK].iloc[-1] - df[HHS_STOCK].iloc[0]) if len(df) else 0,
        "avg_net_hhs": float(df["Net HHS flow"].mean()) if len(df) else 0,
        "stability": stability,
        "total_apprehended": int(df[APPREHENDED].sum()),
        "total_transferred": int(df[TRANSFERRED].sum()),
        "total_discharged": int(df[DISCHARGED].sum()),
    }


def metric_label(value: float, mode: str, decimals: int = 1) -> str:
    return f"{value:.{decimals}%}" if mode == "Ratios" else f"{value:,.0f}"


def normalize_date_range(selected_dates, fallback):
    """Normalize Streamlit's date_input output during range selection.

    A range date_input can briefly return one date while the user is choosing
    the second endpoint.  Unpacking that transient value directly causes the
    dashboard to fail with ``ValueError: not enough values to unpack``.
    """
    if isinstance(selected_dates, (tuple, list)):
        dates = [value for value in selected_dates if value is not None]
        if len(dates) >= 2:
            start_date, end_date = dates[:2]
        elif len(dates) == 1:
            start_date = end_date = dates[0]
        else:
            return fallback
    elif selected_dates is None:
        return fallback
    else:
        start_date = end_date = selected_dates

    if start_date > end_date:
        start_date, end_date = end_date, start_date
    return start_date, end_date


df = load_data()
st.title("Care Transition Efficiency & Placement Outcome Analytics")
st.caption("UAC reporting observations | October 9–December 21, 2025")

with st.sidebar:
    st.header("Controls")
    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    raw_date_range = st.date_input(
        "Reporting date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
    )
    start_date, end_date = normalize_date_range(raw_date_range, (min_date, max_date))
    mode = st.radio("Metric view", ["Counts", "Ratios"], index=0)
    st.divider()
    st.subheader("Alert thresholds")
    transfer_alert = st.slider("Transfer efficiency floor", 0.0, 1.0, 0.25, 0.01)
    discharge_alert_pct = st.slider("Discharge effectiveness floor", 0.0, 2.0, 0.5, 0.1, format="%.1f%%")
    discharge_alert = discharge_alert_pct / 100
    backlog_alert = st.number_input("Backlog change alert", min_value=0, value=0, step=10)
    stability_alert = st.slider("Outcome stability floor", 0, 100, 70, 5)

selected = df[(df["Date"].dt.date >= start_date) & (df["Date"].dt.date <= end_date)].copy()
if selected.empty:
    st.error("No reporting observations are available for the selected date range.")
    st.stop()
kpis = calculate_kpis(selected)

st.info(
    "The ratios are weighted across reporting observations. Because this dataset is a set of aggregate snapshots, "
    "cumulative flows should not be interpreted as tracking the same children from intake to placement."
)

cards = st.columns(6)
if mode == "Counts":
    cards[0].metric("CBP intake", f"{kpis['total_apprehended']:,}")
    cards[1].metric("Transferred to HHS", f"{kpis['total_transferred']:,}")
    cards[2].metric("HHS discharges", f"{kpis['total_discharged']:,}")
else:
    cards[0].metric("Transfer efficiency", f"{kpis['transfer_ratio']:.1%}")
    cards[1].metric("Discharge effectiveness", f"{kpis['discharge_ratio']:.2%}")
    cards[2].metric("Pipeline throughput", f"{kpis['throughput']:.1%}")
cards[3].metric("HHS stock change", f"{kpis['backlog_change']:+,.0f}")
cards[4].metric("Average net HHS flow", f"{kpis['avg_net_hhs']:+,.1f}")
cards[5].metric("Outcome stability", f"{kpis['stability']:.1f}/100")

st.subheader("Threshold alerts")
alerts = []
if kpis["transfer_ratio"] < transfer_alert:
    alerts.append(f"Transfer efficiency is below the {transfer_alert:.0%} floor.")
if kpis["discharge_ratio"] < discharge_alert:
    alerts.append(f"Discharge effectiveness is below the {discharge_alert:.1%} floor.")
if kpis["backlog_change"] > backlog_alert:
    alerts.append(f"HHS care stock increased by {kpis['backlog_change']:,.0f} children across the selected period.")
if kpis["stability"] < stability_alert:
    alerts.append(f"Outcome stability is below the {stability_alert}/100 floor.")
if alerts:
    for alert in alerts:
        st.warning(alert)
else:
    st.success("No selected-period thresholds were breached.")

left, right = st.columns(2)
with left:
    st.subheader("Care pipeline flow")
    sankey = go.Figure(
        go.Sankey(
            arrangement="snap",
            node=dict(label=["CBP intake", "CBP custody", "HHS care", "Sponsor placement"], pad=22, thickness=22),
            link=dict(
                source=[0, 1, 2],
                target=[1, 2, 3],
                value=[kpis["total_apprehended"], kpis["total_transferred"], kpis["total_discharged"]],
            ),
        )
    )
    sankey.update_layout(height=360, margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(sankey, use_container_width=True)
    st.caption("Flow widths show cumulative reported movements in the selected observations; they are not a cohort reconciliation.")

with right:
    st.subheader("Active care loads")
    loads = selected[["Date", CBP_STOCK, HHS_STOCK]].melt("Date", var_name="Stage", value_name="Children")
    loads["Stage"] = loads["Stage"].replace({CBP_STOCK: "CBP custody", HHS_STOCK: "HHS care"})
    fig_loads = px.line(loads, x="Date", y="Children", color="Stage", markers=True, color_discrete_sequence=["#F59E0B", "#2563EB"])
    fig_loads.update_layout(height=360, legend_title_text="", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_loads, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Transition and placement performance")
    ratios = selected[["Date", "Transfer efficiency", "Discharge effectiveness"]].melt("Date", var_name="Metric", value_name="Rate")
    ratios["Metric"] = ratios["Metric"].replace({"Transfer efficiency": "Transfer efficiency", "Discharge effectiveness": "Discharge effectiveness"})
    fig_ratios = px.line(ratios, x="Date", y="Rate", color="Metric", markers=True, color_discrete_sequence=["#7C3AED", "#059669"])
    fig_ratios.add_hline(y=transfer_alert, line_dash="dash", line_color="#7C3AED", annotation_text="Transfer floor")
    fig_ratios.add_hline(y=discharge_alert, line_dash="dash", line_color="#059669", annotation_text="Discharge floor")
    fig_ratios.update_yaxes(tickformat=".1%")
    fig_ratios.update_layout(height=380, legend_title_text="", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_ratios, use_container_width=True)

with right:
    st.subheader("Backlog pressure")
    backlog = selected[["Date", "Net HHS flow"]].copy()
    backlog["Signal"] = backlog["Net HHS flow"].apply(lambda x: "Accumulating" if x > 0 else "Reducing")
    fig_backlog = px.bar(backlog, x="Date", y="Net HHS flow", color="Signal", color_discrete_map={"Accumulating": "#DC2626", "Reducing": "#16A34A"})
    fig_backlog.add_hline(y=0, line_color="#111827")
    fig_backlog.update_layout(height=380, xaxis_title="", yaxis_title="Transfers − discharges", legend_title_text="", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig_backlog, use_container_width=True)

st.subheader("Monthly outcome trend")
monthly = selected.groupby("Month", as_index=False).agg(
    reporting_days=("Date", "count"),
    apprehended=(APPREHENDED, "sum"),
    transferred=(TRANSFERRED, "sum"),
    discharged=(DISCHARGED, "sum"),
    hhs_care=(HHS_STOCK, "last"),
)
monthly["transfer_efficiency"] = monthly["transferred"] / selected.groupby("Month")[CBP_STOCK].sum().values
monthly["discharge_effectiveness"] = monthly["discharged"] / selected.groupby("Month")[HHS_STOCK].sum().values
monthly["net_hhs_flow"] = monthly["transferred"] - monthly["discharged"]
trend = monthly.melt("Month", value_vars=["transferred", "discharged"], var_name="Flow", value_name="Children")
fig_monthly = px.bar(trend, x="Month", y="Children", color="Flow", barmode="group", color_discrete_sequence=["#2563EB", "#059669"])
fig_monthly.update_layout(height=360, legend_title_text="", margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig_monthly, use_container_width=True)

st.subheader("Bottleneck detail")
detail = selected[["Date", CBP_STOCK, TRANSFERRED, HHS_STOCK, DISCHARGED, "Net HHS flow", "Transfer efficiency", "Discharge effectiveness"]].copy()
detail["Risk"] = detail.apply(
    lambda r: "High" if (r["Net HHS flow"] > backlog_alert and r["Transfer efficiency"] < transfer_alert) else ("Watch" if r["Net HHS flow"] > backlog_alert else "Normal"),
    axis=1,
)
detail = detail.sort_values(["Risk", "Net HHS flow"], ascending=[True, False])
st.dataframe(
    detail.style.format({"Transfer efficiency": "{:.1%}", "Discharge effectiveness": "{:.2%}", "Net HHS flow": "{:+,.0f}"}),
    use_container_width=True,
    hide_index=True,
)

with st.expander("Methodology and data notes"):
    st.markdown(
        """
        **Definitions**

        - Transfer efficiency = total transfers out of CBP custody ÷ total children in CBP custody.
        - Discharge effectiveness = total HHS discharges ÷ total children in HHS care.
        - Pipeline throughput = total HHS discharges ÷ total apprehensions reported.
        - Net HHS flow = transfers − discharges. Positive values indicate accumulation pressure in the HHS stage.
        - Outcome stability = 100 × (1 − coefficient of variation of daily discharges), bounded to 0–100.

        The source contains 49 non-daily reporting observations. Weekday comparisons therefore describe observed reporting days, not a balanced calendar sample. Aggregate flows are used for operational signals, not individual-level time-to-placement estimates.
        """
    )
