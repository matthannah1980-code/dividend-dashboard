import matplotlib.pyplot as plt
import pandas as pd
import pdfplumber
import re
import streamlit as st

st.set_page_config(page_title="Portfolio Dividend & Cash Flow Tracker", layout="wide")

st.title("📈 Portfolio Dividend & Cash Flow Tracker")
st.markdown(
    "Monitor your estimated annual income (EAI), historical monthly growth,"
    " and projected cash flow intervals."
)

# Generic template / empty fallback data (no personal info/holdings pre-loaded)
total_eai = 0.00
labels = ["Holdings"]
eai = [0.00]

# Sidebar file uploader for new PDF statements
st.sidebar.header("Statement Management")
uploaded_file = st.sidebar.file_uploader(
    "Upload Monthly Brokerage PDF Statement", type=["pdf"]
)

if uploaded_file is not None:
  st.sidebar.success("Statement uploaded successfully! Parsing data...")

  extracted_eai_list = []
  with pdfplumber.open(uploaded_file) as pdf:
    for page in pdf.pages:
      text = page.extract_text()
      if text:
        matches = re.findall(
            r"Est\. annual income:\s*\$([0-9,]+\.[0-9]{2})", text
        )
        for m in matches:
          extracted_eai_list.append(float(m.replace(",", "")))

  if extracted_eai_list:
    total_eai = sum(extracted_eai_list)
    st.sidebar.info(f"Successfully extracted Total EAI: ${total_eai:,.2f}")

colors = ["#3498db", "#2ecc71", "#e67e22", "#9b59b6", "#e74c3c", "#1abc9c"]

# Main Layout Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric(
    "Daily Income", f"${(total_eai / 365.25) if total_eai > 0 else 0.00:,.2f}"
)
col2.metric(
    "Weekly Income", f"${(total_eai / 52.18) if total_eai > 0 else 0.00:,.2f}"
)
col3.metric("Monthly Income", f"${(total_eai / 12) if total_eai > 0 else 0.00:,.2f}")
col4.metric("Annual Income (EAI)", f"${total_eai:,.2f}")

st.markdown("---")

# Unified Side-by-Side Visualizations
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Pie Chart Subplot
ax1.pie(
    eai if total_eai > 0 else [1],
    labels=labels if total_eai > 0 else ["No Statement Loaded"],
    autopct="%1.1f%%" if total_eai > 0 else None,
    startangle=140,
    colors=colors,
    wedgeprops={"edgecolor": "white", "linewidth": 1.5},
)
ax1.set_title("EAI Breakdown by Asset", fontweight="bold")
ax1.axis("equal")

# Bar Chart Subplot
intervals = ["Daily", "Weekly", "Monthly", "Annual"]
income_intervals = [
    (total_eai / 365.25) if total_eai > 0 else 0,
    (total_eai / 52.18) if total_eai > 0 else 0,
    (total_eai / 12) if total_eai > 0 else 0,
    total_eai,
]
bar_colors = ["#3498db", "#2ecc71", "#e67e22", "#9b59b6"]

bars = ax2.bar(
    intervals,
    income_intervals,
    color=bar_colors,
    width=0.6,
    edgecolor="black",
    linewidth=0.8,
)
ax2.set_title("Cash Flow Intervals", fontweight="bold")
ax2.set_ylabel("Income ($)")
ax2.grid(axis="y", linestyle="--", alpha=0.7)

for bar in bars:
  height = bar.get_height()
  ax2.annotate(
      f"${height:,.2f}",
      xy=(bar.get_x() + bar.get_width() / 2, height),
      xytext=(0, 3),
      textcoords="offset points",
      ha="center",
      va="bottom",
      fontweight="bold",
      fontsize=9,
  )

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# Multi-Month Tracking View
st.subheader("📊 Multi-Month Income Progression & Compounding")
history_data = {
    "Month": ["Current (Est.)"],
    "Monthly Projected Income": [total_eai / 12 if total_eai > 0 else 0.00],
    "Portfolio EAI": [total_eai],
}
hist_df = pd.DataFrame(history_data)

fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(
    hist_df["Month"],
    hist_df["Monthly Projected Income"],
    marker="o",
    color="#2ecc71",
    linewidth=2.5,
    markersize=8,
)
ax3.set_title("Historical Monthly Income Growth Trend", fontweight="bold")
ax3.set_ylabel("Monthly Income ($)")
ax3.grid(True, linestyle="--", alpha=0.7)

for i, txt in enumerate(hist_df["Monthly Projected Income"]):
  ax3.annotate(
      f"${txt:,.2f}",
      (hist_df["Month"][i], txt),
      textcoords="offset points",
      xytext=(0, 10),
      ha="center",
      fontweight="bold",
  )

st.pyplot(fig3)

st.markdown("---")

# Complete Interactive Holdings Data Grid (Clean/Empty template ready for PDF upload)
st.subheader(
    "📋 Complete Portfolio Holdings Overview (Scrollable Spreadsheet View)"
)

complete_holdings = {
    "Symbol": [],
    "Asset Name": [],
    "Est. Monthly Income": [],
    "Est. Annual Income": [],
    "Est. Yield": [],
}

df_all = pd.DataFrame(complete_holdings)

st.dataframe(
    df_all, use_container_width=True, height=400, hide_index=True
)
st.caption(
    "Upload a statement via the sidebar to populate your holdings automatically,"
    " or use this view to inspect assets. Click any column header to sort."
)