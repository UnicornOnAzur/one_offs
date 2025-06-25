# Standard library
import pathlib
# Third party
import streamlit as st


#
st.set_page_config(layout="wide")
st.html(pathlib.Path("streamlit_styles_high.css"))
#
st.title("Title")
left, center, right = st.columns(3, gap=None)
with left:
    with st.container(border=True):
        st.header("Left")
        for i in range(15):
            st.write(i)
with center:
    with st.container(border=True):
        st.header("Center")
with right:
    with st.container(border=True):
        st.header("Right")
st.caption("Caption")

with st.sidebar:
    st.header("Sidebar")
