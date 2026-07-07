# Standard library
import typing
# Third party
import streamlit as st


def process_file():
    st.toast("Received your file")
    st.session_state.unique_key += 1


# Initialize session state for unique key if not already present
if "unique_key" not in st.session_state:
    st.session_state.unique_key = 0
# Set the layout of the Streamlit page
st.title("Demonstrating resetting the file uploader")
left, right = st.columns(2)
# Display the session state in the left column
left.json(st.session_state)
# Display the three file uploaders
right.header("Single file allowed")
right.subheader("Using rerun")
uploaded_file: typing.Optional[
        st.runtime.uploaded_file_manager.UploadedFile] = right.file_uploader(
            "Upload a file", key=f"uploader_key_{st.session_state.unique_key}")
if uploaded_file is not None:
    st.session_state.unique_key += 1
    st.rerun()
right.subheader("Using user interaction")
uploaded_file_1: typing.Optional[
        st.runtime.uploaded_file_manager.UploadedFile] = right.file_uploader(
            "Upload a file", key=f"uploader_key1_{st.session_state.unique_key}"
            )
if uploaded_file_1 is not None:
    st.session_state.unique_key += 1
right.button("Click")
right.subheader("Using 'on_change'")
right.file_uploader(
    "Upload a file", key=f"uploader_key2_{st.session_state.unique_key}",
    on_change=process_file)
right.subheader("Within a st.form")
form: st._DeltaGenerator = right.form("form1", clear_on_submit=True)
form.file_uploader("Upload a file", key="uploader_in_form1")
form.form_submit_button()
