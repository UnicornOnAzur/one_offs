"""
This module provides functionality for demonstraying interactive forms using
Streamlit. It includes methods for handling user input and managing session
state.

Functions:
- call_back_function: Collects input values and stores the result in session
state.
- create_form: Creates a form with number input and segmented control,
handling various submission scenarios.
"""
# Third party
import streamlit as st
# Constants
OPTIONS = range(5)


def call_back_function(*args, **kwargs) -> None:
    # Collecting values from session state and arguments
    vals = [st.session_state[key] for key in kwargs.get("keys", [])] +\
        list(args)
    result = ", ".join(map(str, vals))  # Joining values into a string
    if vals == [0.0, None]:  # Checking if values are default
        result = ":red[variables are not yet updated]"
    # Storing the result in session state
    st.session_state["callback_result"] = result


def create_form_using_with_statement(
        column, form_key, number_key,
        segment_key, use_on_click=False, with_args=False) -> None:
    with column.form(form_key):
        t = st.number_input("Pick a number", key=number_key)
        s = st.segmented_control("Slide", options=OPTIONS, key=segment_key)
        if use_on_click and with_args:
            st.form_submit_button(on_click=call_back_function, args=(t, s))
        elif use_on_click:
            st.form_submit_button(on_click=call_back_function,
                                  kwargs={"keys": (number_key, segment_key)})
        elif with_args:
            clicked = st.form_submit_button()
            if clicked:
                call_back_function(t, s)
        else:
            clicked = st.form_submit_button()
            if clicked:
                call_back_function(keys=(number_key, segment_key))


def create_form_with_direct_call(
        column, form_key, number_key,
        segment_key, use_on_click=False, with_args=False) -> None:
    form = column.form(form_key)
    t = form.number_input("Pick a number", key=number_key)
    s = form.segmented_control("Slide", options=OPTIONS, key=segment_key)
    if use_on_click and with_args:
        form.form_submit_button(on_click=call_back_function, args=(t, s))
    elif use_on_click:
        form.form_submit_button(on_click=call_back_function,
                                kwargs={"keys": (number_key, segment_key)})
    elif with_args:
        clicked = form.form_submit_button()
        if clicked:
            call_back_function(t, s)
    else:
        clicked = form.form_submit_button()
        if clicked:
            call_back_function(keys=(number_key, segment_key))


st.set_page_config(layout="wide")
left, right = st.columns([.1, .9])
# Set column headers
col1, col2, col3, col4 = right.columns(4)
col1.subheader("Using keys")
col2.subheader("Using keys and 'on_click'")
col3.subheader("Using variables")
col4.subheader("Using variables and 'on_click'")
# Top row
with st.container(border=True):
    st.subheader("With statement")
    col1, col2, col3, col4 = st.columns(4)
    create_form_using_with_statement(col1, "form_1", "number_1", "segment_1")
    create_form_using_with_statement(col2, "form_3", "number_3", "segment_3",
                                     use_on_click=True)
    create_form_using_with_statement(col3, "form_5", None, None,
                                     with_args=True)
    create_form_using_with_statement(col4, "form_7", None, None,
                                     use_on_click=True, with_args=True)
# Bottom row
with st.container(border=True):
    st.subheader("Direct")
    col1, col2, col3, col4 = st.columns(4)
    create_form_with_direct_call(col1, "form_2", "number_2", "segment_2")
    create_form_with_direct_call(col2, "form_4", "number_4", "segment_4",
                                 use_on_click=True)
    create_form_with_direct_call(col3, "form_6", None, None, with_args=True)
    create_form_with_direct_call(col4, "form_8", None, None, use_on_click=True,
                                 with_args=True)
# Showing the result from session state
st.write(f'Callback result: {st.session_state.get("callback_result",
                                                  "no result yet")}')
