import streamlit as st
import pandas as pd
from collections import Counter
import io
import plotly.express as px

st.set_page_config(page_title="Conference Target Summary", layout="wide")

st.title("Conference LeadScope")


uploaded_files = st.file_uploader("Upload one or more CSV files", type="csv", accept_multiple_files=True)

if uploaded_files:
    all_conferences = set()
    file_conference_counts = {}

    # Process each uploaded CSV
    for uploaded_file in uploaded_files:
        file_name = uploaded_file.name.replace(".csv", "")
        df = pd.read_csv(uploaded_file)

        if "Tradeshow" not in df.columns:
            st.warning(f"'Tradeshow' column not found in {uploaded_file.name}")
            continue

        # Clean and count tradeshow entries
        conferences = df["Tradeshow"].dropna().astype(str).str.strip()
        conference_counts = Counter(conferences)
        file_conference_counts[file_name] = conference_counts
        all_conferences.update(conferences)

    # Build initial result table
    all_conferences = sorted(all_conferences)
    result_df = pd.DataFrame({"Conference": all_conferences})

    # Add count columns per file
    for file_name, counts in file_conference_counts.items():
        result_df[file_name] = result_df["Conference"].map(lambda x: counts.get(x, 0))

    # Add total column
    count_columns = list(file_conference_counts.keys())
    result_df["Total"] = result_df[count_columns].sum(axis=1)

    # Optional sorting
    sort_option = st.radio(
        "Sort table by total count?",
        options=["Yes", "No"],
        index=0,
        horizontal=True
    )

    if sort_option == "Yes":
        result_df = result_df.sort_values(by="Total", ascending=False).reset_index(drop=True)

    # Show the table
    st.subheader("Summary Table")
    st.dataframe(result_df, use_container_width=True)

    # Download option
    csv_buffer = io.StringIO()
    result_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="Download Summary Table",
        data=csv_buffer.getvalue(),
        file_name="conference_summary.csv",
        mime="text/csv"
    )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Plot bar charts per disease
    st.subheader("Summary Plot")
    for file_name in count_columns:
        top10 = result_df[["Conference", file_name]].sort_values(by=file_name, ascending=False).head(10)
        fig = px.bar(
            top10,
            x=file_name,
            y="Conference",
            orientation="h",
            title=f"Top 10 Conferences – {file_name}",
            text_auto=True,
            height=400
        )
        fig.update_layout(yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Please upload one or more CSV files to begin.")
