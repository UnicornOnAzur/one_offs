# Third party
import streamlit as st


# Main page
st.title("Title")
# Creating three columns: left, center, and right
left, center, right = st.columns(3)
with left:
    # Create container to display a border
    with st.container(border=True):
        st.header("Left")
        for i in range(15):
            st.write(str(i))
with center:
    with st.container(border=True):
        st.header("Center")
with right:
    with st.container(border=True):
        st.header("Right")
st.caption("Caption")
# Sidebar
with st.sidebar:
    st.header("Sidebar")
