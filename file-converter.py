import streamlit as st
import pandas as pd 
import os
from io import BytesIO 

st.markdown(
    """
    <style>
    .stApp{
    background-color:black;
    color:white;
    } 
</style>    
    """,

    unsafe_allow_html=True
)

#tiitle and description
st.tiitle("Datasweeper Sterling Integrator By Muhammad Junaid")
st.write("Transform your files between CSV amd Excel format with built-in data cleaning")

#file upload
upload_files = st.file_uploader("upload your files(accepts CSV or Excel):",type=["csv","xlsx"],accept_multiple_files=(True))

if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
                else:
                    st.error(f"unsupported file type: {file_ext}")
                    continue

                    #file details
                    st.write("preview the head of the Dataframe")
                    st.dataframe(df.head())

                    #data cleaning option
                    st.subheader("Data Cleaning Option")
                    if st.checkbox(f"clean data for {file.name}"):
                        col1,col2 = st.columns(2)

                        with col1:
                            if st.button(f"remove duplicates from the file:{file.name}"):
                                df.drop_duplicates(inplace=True)
                                st.write("Duplicates remove")

                                with col2:
                                    if st.button(f"fill missing values for {file.name} "):
                                        numeric_cols = df.select_dtypes(includes=['number']).columns
                                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                                        st.write("Missing values have been filled!")

                                        st.subheader("select columns to keep")
                                        columns = st.multiselect(f"choose columns for {file.name}", df.columns, default= df.columns)
                                        df = df[columns]

                                        #data visualization
                                        st.subheader("Data visualization")
                                        if st.checkbox(f"show visualization for {file.name}";):
                                            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

                                            #conversation option

                                            st.subheader("conversation otion")
                                            conversation_type = st.radio(f"convert{file.name} to:",["CVS","Excel"],key=file.name)
                                            if st.button(f"convert{file.name}"):
                                                buffer=BytesIO()
                                                if conversation_type == "CSV":
                                                    df.to.csv(buffer,index=False)
                                                    file_name = file.name.replace(file_ext,".csv")
                                                    mime_type = "text/csv"

                                                    elif conversation_type == "Excel":
                                                    df.to.excel(buffer,index=False)
                                                    file_name = file.name.replace(file_ext,".xlsx")
                                                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                                    buffer.seek(0)

                                                    st.download_button(
                                                        label=f"download {file.name} as {conversation_type}"
                                                        data=buffer,
                                                        file_name=file_name,
                                                        mime=mime_type
                                                    )
                                                    st.success("all files processed successfully!")

