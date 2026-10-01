import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import pdfplumber
import re

st.set_page_config(page_title="Dividend Income Dashboard", layout="wide")

st.title("📈 Matthew's Portfolio Dividend & Cash Flow Tracker")
st.markdown("Monitor your estimated annual income (EAI), historical monthly growth, and projected cash flow intervals.")

# Default fallback data based on August Statement
total_eai = 14643.25
labels = ['EXG', 'APLE', 'MAIN', 'O', 'SCHD', 'Other Holdings']
eai = [3404.08, 3345.10, 1926.73, 1702.46, 441.09, 14643.25 - (3404.08 + 3345.10 + 1926.73 + 1702.46 + 441.09)]

# Sidebar file uploader for new PDF statements
st.sidebar.header("Statement Management")
uploaded_file = st.sidebar.file_uploader("Upload Monthly Vanguard PDF Statement", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.success("Statement uploaded successfully! Parsing data...")
    
    extracted_eai_list = []
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                matches = re.findall(r"Est\. annual income:\s*\$([0-9,]+\.[0-9]{2})", text)
                for m in matches:
                    extracted_eai_list.append(float(m.replace(",", "")))
                    
    if extracted_eai_list:
        total_eai = sum(extracted_eai_list)
        st.sidebar.info(f"Successfully extracted Total EAI: ${total_eai:,.2f}")

colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0', '#ffb3e6']

# Main Layout Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Daily Income", f"${total_eai / 365.25:,.2f}")
col2.metric("Weekly Income", f"${total_eai / 52.18:,.2f}")
col3.metric("Monthly Income", f"${total_eai / 12:,.2f}")
col4.metric("Annual Income (EAI)", f"${total_eai:,.2f}")

st.markdown("---")

# Unified Side-by-Side Visualizations (Even Height & Alignment)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Pie Chart Subplot
ax1.pie(eai, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors, wedgeprops={'edgecolor': 'white', 'linewidth': 1.5})
ax1.set_title("EAI Breakdown by Asset", fontweight='bold')
ax1.axis('equal')

# Bar Chart Subplot
intervals = ['Daily', 'Weekly', 'Monthly', 'Annual']
income_intervals = [total_eai / 365.25, total_eai / 52.18, total_eai / 12, total_eai]
bar_colors = ['#3498db', '#2ecc71', '#e67e22', '#9b59b6']

bars = ax2.bar(intervals, income_intervals, color=bar_colors, width=0.6, edgecolor='black', linewidth=0.8)
ax2.set_title("Cash Flow Intervals", fontweight='bold')
ax2.set_ylabel("Income ($)")
ax2.grid(axis='y', linestyle='--', alpha=0.7)

for bar in bars:
    height = bar.get_height()
    ax2.annotate(f"${height:,.2f}",
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontweight='bold', fontsize=9)

plt.tight_layout()
st.pyplot(fig)

st.markdown("---")

# Multi-Month Tracking View
st.subheader("📊 Multi-Month Income Progression & Compounding")
history_data = {
    "Month": ["June 2026", "July 2026", "August 2026", "September 2026", "October 2026 (Est.)"],
    "Monthly Projected Income": [1120.50, 1155.00, 1220.27, 1260.00, total_eai / 12],
    "Portfolio EAI": [13446.00, 13860.00, 14643.25, 15120.00, total_eai]
}
hist_df = pd.DataFrame(history_data)

fig3, ax3 = plt.subplots(figsize=(10, 4))
ax3.plot(hist_df["Month"], hist_df["Monthly Projected Income"], marker='o', color='#2ecc71', linewidth=2.5, markersize=8)
ax3.set_title("Historical Monthly Income Growth Trend", fontweight='bold')
ax3.set_ylabel("Monthly Income ($)")
ax3.grid(True, linestyle='--', alpha=0.7)

for i, txt in enumerate(hist_df["Monthly Projected Income"]):
    ax3.annotate(f"${txt:,.2f}", (hist_df["Month"][i], txt), textcoords="offset points", xytext=(0,10), ha='center', fontweight='bold')

st.pyplot(fig3)

st.markdown("---")

# Complete Interactive Holdings Data Grid
st.subheader("📋 Complete Portfolio Holdings Overview (Scrollable Spreadsheet View)")

complete_holdings = {
    "Symbol": [
        "VBTLX", "VTSAX", "EXG", "GLU", "NEA", "UTG", "VYM", "VCLT", "SDIV", "DIV", 
        "SPFF", "SDEM", "SPHD", "SPLV", "SCHD", "MMM", "ABBV", "AQN", "AEP", "APLE", 
        "ARTNA", "AZN", "T", "BALL", "BAC", "BP", "CPT", "CPB", "CCL", "KO", 
        "ED", "CSX", "DG", "D", "EPR", "ELS", "FPI", "FRT", "F", "GE", 
        "GEHC", "GEO", "LAND", "GNL", "HRL", "INTC", "IRM", "JNJ", "KRC", "KHC", 
        "KR", "MAIN", "MCD", "MPT", "MSFT", "MDLZ", "NTDOY", "NUE", "ONL", "PBA", 
        "PFE", "O", "QSR", "RITM", "SOLV", "SO", "STAG", "SBUX", "TGT", "UGI", 
        "VZ", "VTRS", "VICI", "V", "WMT", "WBD", "WEN", "YUM", "SUN"
    ],
    "Asset Name": [
        "Vanguard Total Bond Market", "Vanguard Total Stock Market", "Eaton Vance Global Div Income", "Gabelli Global Utility", "Nuveen Quality Municipal", "Reaves Utility Income Fund", "Vanguard High Dividend Yield ETF", "Vanguard Long Term Corp Bond ETF", "Global X SuperDividend ETF", "Global X SuperDividend US ETF",
        "Global X SuperIncome Preferred", "Global X MSCI SuperDiv Emerging", "Invesco S&P 500 High Div Low Vol", "Invesco S&P 500 Low Volatility", "Schwab US Dividend Equity ETF", "3M Company", "AbbVie Inc", "Algonquin Power & Utilities", "American Electric Power", "Apple Hospitality REIT",
        "Artesian Resources Corp", "AstraZeneca PLC", "AT&T Inc", "Ball Corp", "Bank of America Corp", "BP PLC", "Camden Property Trust", "Campbells Co", "Carnival Corp", "Coca-Cola Company",
        "Consolidated Edison", "CSX Corp", "Dollar General Corp", "Dominion Energy", "EPR Properties", "Equity Lifestyle Properties", "Farmland Partners Inc", "Federal Realty Investment Tr", "Ford Motor Co", "GE Aerospace",
        "GE Healthcare Technologies", "GEO Group Inc", "Gladstone Land Corp", "Global Net Lease Inc", "Hormel Foods Corp", "Intel Corp", "Iron Mountain Inc", "Johnson & Johnson", "Kilroy Realty Corp", "Kraft Heinz Co",
        "Kroger Co", "Main Street Capital Corp", "McDonalds Corp", "Medical Properties Trust", "Microsoft Corp", "Mondelez International", "Nintendo Ltd ADR", "Nucor Corp", "Orion Properties Inc", "Pembina Pipeline Corp",
        "Pfizer Inc", "Realty Income Corp", "Restaurant Brands International", "Rithm Capital Corp", "Solventum Corp", "Southern Company", "STAG Industrial Inc", "Starbucks Corp", "Target Corp", "UGI Corp",
        "Verizon Communications", "Viatris Inc", "VICI Properties Inc", "Visa Inc", "Walmart Inc", "Warner Bros Discovery", "Wendys Co", "Yum Brands Inc", "Sunoco LP Partnership"
    ],
    "Est. Annual Income": [
        285.46, 357.89, 3404.08, 61.36, 39.73, 70.96, 35.57, 22.41, 89.39, 51.43,
        45.24, 39.79, 117.89, 16.96, 441.09, 32.85, 89.48, 16.95, 32.34, 3345.10,
        20.91, 13.07, 137.63, 16.99, 29.76, 2.67, 25.87, 28.03, 66.36, 67.94,
        25.56, 57.41, 38.42, 26.64, 41.49, 17.49, 30.06, 18.19, 89.34, 5.77,
        0.14, 0.00, 18.85, 47.53, 42.85, 0.00, 74.53, 12.32, 29.13, 93.56,
        12.33, 1926.73, 25.03, 10.75, 7.68, 24.02, 32.11, 24.53, 0.30, 51.80,
        140.26, 1702.46, 65.09, 130.62, 0.00, 45.84, 146.67, 64.02, 5.42, 90.11,
        87.48, 4.20, 109.78, 8.29, 57.33, 0.00, 18.90, 32.96, 144.06
    ],
    "Est. Yield": [
        "4.08%", "1.02%", "7.89%", "6.91%", "7.25%", "6.68%", "2.22%", "5.65%", "9.02%", "6.41%",
        "6.64%", "4.90%", "4.55%", "2.17%", "3.00%", "1.82%", "2.70%", "4.59%", "3.10%", "6.02%",
        "3.60%", "1.99%", "4.29%", "1.27%", "2.07%", "4.71%", "3.99%", "6.59%", "2.51%", "2.39%",
        "3.32%", "1.11%", "1.86%", "4.04%", "6.18%", "3.38%", "3.50%", "3.92%", "4.30%", "0.56%",
        "0.20%", "N/A", "6.10%", "8.28%", "5.35%", "N/A", "3.00%", "2.02%", "5.95%", "6.23%",
        "2.71%", "5.40%", "2.82%", "9.07%", "0.72%", "3.35%", "2.44%", "0.90%", "2.81%", "4.30%",
        "6.04%", "5.31%", "3.34%", "9.97%", "N/A", "3.45%", "4.12%", "2.33%", "2.88%", "3.90%",
        "5.66%", "2.91%", "7.02%", "0.71%", "0.94%", "N/A", "3.37%", "1.96%", "5.27%"
    ]
}

df_all = pd.DataFrame(complete_holdings)

# Calculate Est. Monthly Income dynamically
df_all["Est. Monthly Income"] = (df_all["Est. Annual Income"] / 12).round(2)

# Reorder columns to include Monthly Income
df_all = df_all[["Symbol", "Asset Name", "Est. Monthly Income", "Est. Annual Income", "Est. Yield"]]

# Display scrollable table with height fixed to approx 10 rows (~400px), enabling column sorting by clicking headers
st.dataframe(df_all, use_container_width=True, height=400, hide_index=True)
st.caption("Displaying all holdings in a scrollable frame (showing ~10 rows at a time). Click any column header to sort.")