
import os
import platform
import threading

import streamlit as st
import streamlit.runtime.scriptrunner_utils.script_run_context as run_context


left, right = st.columns(2)
left.header("Using Streamlit")
with left.container(border=True):
    st.subheader("st.context")
    st.write(st.context.url)
    st.write("http://localhost" in st.context.url)
    st.space()
    st.subheader("ScriptRunContext")
    context: run_context.ScriptRunContext = run_context.get_script_run_ctx()
    st.write(context.context_info.url)
    st.write("http://localhost" in context.context_info.url)
    st.space()
    st.subheader("AppSession")
    st.space()
    st.subheader("Runtime")
    st.write(st.runtime.Runtime)
right.header("Other approaches")
with right.container(border=True):
    st.subheader("OS")
    st.write(os.getenv('USER'))
    st.space()
    st.subheader("Platform")
    st.write(platform.processor())
    st.write(platform.processor() != "")
    st.space()
    st.subheader("Threading")
    thread = threading.current_thread()
    st.write(type(thread).__module__)
