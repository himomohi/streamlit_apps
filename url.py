import pandas as pd
import streamlit as st

# 1. Set Page Configuration
st.set_page_config(
    page_title="URL Extractor",
    page_icon="🔗",
    layout="wide"
)

# 2. Main Title
st.header("URL Extractor")

# 3. Upload Section
st.subheader("Upload your CSV file")
with st.expander("Upload CSV File", expanded=True):
    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        label_visibility="collapsed"
    )

filenames = []

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='cp949')
    urls = df["상세이미지경로"] # Assuming this is the correct column

    for url_entry in urls:
        url_entry = str(url_entry)
        
        if url_entry == "nan": # Handle potential 'nan' string values if column is not always populated
            path = ""
            filename = ""
        elif "/" not in url_entry: # Handle cases where there's no slash (e.g. just a filename)
            path = ""
            filename = url_entry
        else:
            filename = url_entry.split("/")[-1]
            path = url_entry[:url_entry.rfind("/")+1]
            if filename == "nan": # if the part after last / is nan
                filename = ""


        filenames.append([path, filename])

    df[["url", "filename"]] = filenames
    df_result = df[["url", "filename"]]
    # df_result.to_csv("경로2.csv", index=False) # Removed, as it's an intermediate step not needed for the app UI

    def convert_df_to_csv(df_to_convert):
        return df_to_convert.to_csv(index=False).encode('cp949')

    csv_data = convert_df_to_csv(df_result)

    # 5. Results Section
    st.markdown("---")
    st.subheader("Results")

    col1, col2 = st.columns([1, 3]) # Adjust column ratios as needed

    with col1:
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name="url_divided.csv",
            mime="text/csv",
            key='download-csv'
        )
        st.success('URL extraction complete!', icon="✅")

    with col2:
        st.dataframe(df_result)
else:
    st.info("Upload a CSV file to begin processing.")
