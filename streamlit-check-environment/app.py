# Standard library
import os
import platform
import threading
# Third party
import streamlit as st
import streamlit.runtime as runtime
import streamlit.runtime.scriptrunner_utils.script_run_context as run_context

st.set_page_config(layout="wide")
left, right = st.columns(2)
left.header("Using Streamlit")
with left.container(border=True):
    st.subheader("st.context")
    st.write(st.context.url)
    st.write(st.context.url.startswith("http://localhost"))
    st.space()
    st.subheader("ScriptRunContext")
    context: run_context.ScriptRunContext = run_context.get_script_run_ctx()
    st.write(context.context_info.url)
    st.write(context.context_info.url.startswith("http://localhost"))
    st.space()
    st.subheader("Runtime")
    runtime_instance = runtime.Runtime.instance()
    st.write(runtime_instance._main_script_path)
    st.write(not runtime_instance._main_script_path.startswith("/mount/"))
right.header("Other approaches")
with right.container(border=True):
    st.subheader("OS")
    for env in ("USER", "STREAMLIT_SERVER_RUN_ON_SAVE",
                "STREAMLIT_SERVER_ALLOW_RUN_ON_SAVE"):
        st.write(f"{env}: {os.getenv(env)}")
    st.write(os.getenv("USER") != "appuser")
    st.space()
    st.subheader("Platform")
    st.write(f"'{platform.processor()}'")
    st.write(platform.processor() != "")
    st.space()
    st.subheader("Threading")
    st.write(threading.current_thread().name)
    st.write(threading.current_thread().name.startswith("ScriptRunner"))
