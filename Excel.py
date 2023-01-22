from __future__ import unicode_literals
import streamlit as st
import pandas as pd
import base64
import os
from io import BytesIO

#title of microservice
#st.image('russell.gif')
st.set_option('deprecation.showfileUploaderEncoding', False)
st.title('Drop Empty Columns Export')

st.sidebar.title("HI Lydia")



def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    processed_data = output.getvalue()
    return processed_data


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="extract.xlsx">Download XLXS</a>' # decode b'abc' => abc



def get_table_download_link_csv(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="extract.csv">Download csv file</a>'
    return href


user_file = st.sidebar.file_uploader("Upload your File:")
if user_file is not None:
    try:
        with st.spinner("Uploading your File..."):
            df = pd.read_csv(user_file, dtype=str, on_bad_lines='skip')

            df = df[df['Which Kingdomcity location are you from?']=='Kuala Lumpur, Malaysia']
            df = df.dropna(axis=1, how='all')
            st.success('Done!')
        st.subheader("Your File")
        st.write(df)
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
    except Exception as e:
        st.error(
            f"Sorry, there was a problem processing your file./n {e}"
        )
        user_file = None