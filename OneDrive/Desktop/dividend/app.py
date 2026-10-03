from datetime import datetime
import io
import matplotlib.pyplot as plt
import pandas as pd
import pdfplumber
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Portfolio Dividend Tracker", page_icon="📈", layout="wide"
)

st.title("📈 Portfolio Cash Flow & Dividend Tracker")
st.write(
    "Upload your brokerage PDF statements to extract holdings, track monthly"
    " dividend income, and monitor cash flow."
)

st.markdown("---")

# File Uploader (No pre-loaded data)
uploaded_file = st.file_uploader(
    "Upload Brokerage PDF Statement", type=["pdf"]
)

if uploaded_file is not None:
  with st.spinner("Extracting portfolio data from PDF..."):
    extracted_rows = []
    with pdfplumber.open(uploaded_file) as pdf:
      for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
          for row in table:
            # Clean up row cells
            cleaned_row = [
                cell.strip() if cell is not None else "" for cell in row
            ]
            if any(cleaned_row):
              extracted_rows.append(cleaned_row)

    if extracted_rows:
      df = pd.DataFrame(extracted_rows)

      st.subheader("Extracted Holdings & Assets")
      st.dataframe(df, use_container_width=True)

      # Optional summary metrics or charts can be added here based on columns
    else:
      st.warning(
          "No tabular data could be automatically extracted from this PDF."
      )

else:
  st.info(
      "👈 Please upload a PDF statement using the file uploader above to"
      " begin."
  )