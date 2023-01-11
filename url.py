import pandas as pd
import streamlit as st
st.title("URL 분리 _ver1.0")
# 저장할 csv 파일


uploaded_file = st.file_uploader("파일을 선택 해주세요.")
filenames = []

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding='cp949')
    # urls = df["첨부파일이미지경로"]
    urls = df["상세이미지경로"]

    for url in urls:
        url = str(url)
        # print(url)

        filename = url.split("/")[-1].replace("nan", "")
        url = url[:url.rfind("/")+1]

        filenames.append([url, filename])

    print("시작~~~~")
    df[["url", "filename"]] = filenames
    df_result = df[["url", "filename"]]
    df_result.to_csv("경로2.csv", index=False)

    def convert_df(df_result):
        return df_result.to_csv(index=False).encode('cp949')

    csv = convert_df(df_result)
    st.download_button(
        "다운로드",
        csv,
        "url_divide.csv",
        "text/csv",
        key='download-csv'
    )
    st.success('url 분리 완료 되었습니다.', icon="✅")
    st.success('Done!')
    print("완료")
    st.dataframe(df_result)
