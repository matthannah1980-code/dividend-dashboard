import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(
    page_title="Dividend Portfolio Dashboard",
    page_icon="📈",
    layout="wide"
)

# Initialize Session State Variables
if "holdings_df" not in st.session_state:
    st.session_state["holdings_df"] = pd.DataFrame(columns=[
        "Symbol", "Asset Name", "Est. Monthly Income", "Est. Annual Income", "Est. Yield"
    ])
if "total_eai" not in st.session_state:
    st.session_state["total_eai"] = 0.0

# Sidebar Statement Management
st.sidebar.title("Statement Management")
st.sidebar.markdown("Upload Monthly Brokerage PDF Statement")
uploaded_file = st.sidebar.file_uploader("Choose PDF file", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.success("Statement uploaded successfully!")
    st.sidebar.info("Parsing data...")
    
    # --- INSERT YOUR PDF PARSING LOGIC HERE ---
    # Example extracted values binding to session state:
    extracted_eai = 29286.50
    extracted_holdings = [
        {"Symbol": "SCHD", "Asset Name": "Schwab U.S. Dividend Equity ETF", "Est. Monthly Income": 450.00, "Est. Annual Income": 5400.00, "Est. Yield": 3.45},
        {"Symbol": "O", "Asset Name": "Realty Income Corp", "Est. Monthly Income": 320.00, "Est. Annual Income": 3840.00, "Est. Yield": 5.20},
        {"Symbol": "MAIN", "Asset Name": "Main Street Capital Corp", "Est. Monthly Income": 280.00, "Est. Annual Income": 3360.00, "Est. Yield": 6.10},
        {"Symbol": "APLE", "Asset Name": "Apple Hospitality REIT Inc", "Est. Monthly Income": 190.00, "Est. Annual Income": 2280.00, "Est. Yield": 6.05},
        {"Symbol": "EXG", "Asset Name": "Eaton Vance Tax-Managed Global Diversified Equity Income Fund", "Est. Monthly Income": 650.00, "Est. Annual Income": 7800.00, "Est. Yield": 8.50}
    ]
    
    # Save parsed data to session state
    st.session_state["total_eai"] = extracted_eai
    st.session_state["holdings_df"] = pd.DataFrame(extracted_holdings)
    
    st.sidebar.success(f"Successfully extracted Total EAI: ${st.session_state['total_eai']:,.2f}")

# Main Dashboard Interface
st.title("📊 Dividend Portfolio Cash Flow Dashboard")

# Summary Metric Display
st.metric(label="Estimated Annual Income (EAI)", value=f"${st.session_state['total_eai']:,.2f}")

st.markdown("---")

# Complete Portfolio Holdings Overview Table
st.markdown("### 📋 Complete Portfolio Holdings Overview (Scrollable Spreadsheet View)")

if not st.session_state["holdings_df"].empty:
    st.dataframe(
        st.session_state["holdings_df"],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Symbol": "Symbol",
            "Asset Name": "Asset Name",
            "Est. Monthly Income": st.column_config.NumberColumn("Est. Monthly Income", format="$%.2f"),
            "Est. Annual Income": st.column_config.NumberColumn("Est. Annual Income", format="$%.2f"),
            "Est. Yield": st.column_config.NumberColumn("Est. Yield", format="%.2f%%")
        }
    )
else:
    st.warning("Upload a statement via the sidebar to populate your holdings automatically, or use this view to inspect assets. Click any column header to sort.")