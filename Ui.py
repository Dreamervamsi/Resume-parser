import streamlit as st
import requests

st.markdown(
    """
    <h1 style='text-align: center;'>📁 AI-powered Resume parser</h1>
    
    """,
    unsafe_allow_html=True
)

st.divider()

with st.container():
    st.subheader("Upload File")
    
    file = st.file_uploader(
        "Choose a file",
        help="Supported formats depend on backend configuration"
    )

    if file:
        st.success(f"Selected file: {file.name}")

        if st.button("Upload File", use_container_width=True):
            with st.spinner("Uploading... please wait"):
                try:
                    files = {
                        "file": (file.name, file.getvalue(), file.type)
                    }

                    res = requests.post(
                        "http://localhost:8000/upload",
                        files=files
                    )

                    if res.status_code == 200:
                        st.success("Upload successful!")

                        st.subheader("Response")
                        st.write(res.json())

                    else:
                        st.error(f"Upload failed (Status: {res.status_code})")

                except requests.exceptions.RequestException as e:
                    st.error("Server connection error")
                    st.exception(e)
