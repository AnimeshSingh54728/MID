import streamlit as st
import pandas as pd
import sqlite3
import io

# Title
st.title("🔎 Search Merchant Record")

# User input for ID
uid = st.text_input("Enter merchantexternalid:")

# When user submits ID
if uid:
    try:
        # Connect to local SQLite DB (make sure merged_data.db is in the same directory)
        conn = sqlite3.connect('merged_data.db')
        query = "SELECT * FROM cases WHERE merchantexternalid = ?"
        result = pd.read_sql_query(query, conn, params=(uid,))
        conn.close()

        if result.empty:
            st.error("❌ No record found with that unique ID.")
        else:
            st.success("✅ Record found:")
            st.dataframe(result)

            # Option to download as Excel
            buffer = io.BytesIO()
            result.to_excel(buffer, index=False, engine='openpyxl')
            st.download_button(
                label="📥 Download as Excel",
                data=buffer.getvalue(),
                file_name=f"record_{uid}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"An error occurred: {e}")
