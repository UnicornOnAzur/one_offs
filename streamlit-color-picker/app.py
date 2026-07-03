"""
Module for demonstrating theme colors in a Streamlit application.

This module provides functionality to read and write theme colors from
a TOML configuration file, reset the configuration to default values,
and manage user interactions through a Streamlit interface.

author:
"""
# Standard library
import glob
import pathlib
import toml
import typing
# Third party
import pandas as pd
import streamlit as st
# Constants
TOML_FILE_PATH: pathlib.Path = glob.glob("**/*streamlit-color-picker*/.streamlit/*.toml", recursive=True)[0]
TXT_FILE_PATH: pathlib.Path = glob.glob("**/*streamlit-color-picker*/default.txt", recursive=True)[0]
HEADER: str = "theme"


def read_toml_to_dict() -> typing.Dict[str, str]:
    with open(TOML_FILE_PATH) as file:
        return toml.load(file)[HEADER]


def write_session_state_to_toml() -> None:
    with open(TOML_FILE_PATH, "w") as file:
        file.write(f"[{HEADER}]\n")
        toml.dump({key: st.session_state[key] for key in COLOR_FIELDS}, file)


def reset_toml_file_to_default() -> None:
    with (open(TXT_FILE_PATH) as text_file,
          open(TOML_FILE_PATH, "w") as toml_file):
        toml_file.write(text_file.read())


@lambda _: _()
def init() -> None:
    global COLOR_FIELDS
    COLOR_FIELDS = []
    st.set_page_config(layout="wide")
    theme: typing.Dict[str, str] = read_toml_to_dict()
    for key, value in theme.items():
        st.session_state[key] = value
        COLOR_FIELDS.append(key)


def set_new_color_in_theme():
    """Sets a new color in the theme based on user input and updates the
    TOML configuration file.

    Returns:
        None
    """
    st.session_state[st.session_state["color_field"]] =\
        st.session_state["color"]
    write_session_state_to_toml()


def color_cells_by_value(values: pd.Series) -> typing.List[str]:
    """Applies background color styles to cells based on their values.

    Parameters:
        values: A list of color values.

    Returns:
        A list of CSS style strings for background colors.
    """
    return [f"background-color: {value}" for value in values]


def main() -> None:
    sidebar = st.sidebar
    sidebar.header("Sidebar")
    left, right = st.columns(2)
    # LEFT: changing colors and displaying the current value
    left.header("Change a color")
    form = left.form("form")
    form.color_picker("Choose a color",  key="color")
    form.selectbox("Where do you want to set the color?",
                   options=COLOR_FIELDS, key="color_field")
    if form.form_submit_button():
        set_new_color_in_theme()
    left.subheader("The current colors")
    left.table(pd.DataFrame().from_dict(read_toml_to_dict(), orient="index"
                                        ).style.apply(color_cells_by_value,
                                                      axis=1, subset=[0]),
               hide_header=True)
    # RIGHT: Showcasing the use of the colors by Streamlit
    right.header("See the colors")
    rc1, rc2, rc3 = right.columns(3)
    rc1.button("Reset toml file", type="primary",
               on_click=reset_toml_file_to_default)
    rc2.button("Secondary button", type="secondary")
    rc3.button("Tertiary button", type="tertiary")
    rc1.link_button("Link button", url="")
    rc2.download_button("Download button", data="")
    rc3.file_uploader("Uploader")
    right.multiselect("Multiselect", options=COLOR_FIELDS,
                      default=COLOR_FIELDS[-1])
    container = right.container(border=True)
    container.subheader("Inside a container")
    container.markdown(("This is Markdown test. "
                        "This is `inline code` in Markdown. "
                        "This is a link to the [Streamlit docs]()."))
    container.code("for i in range(9): print(i)")
    right.dataframe(data=pd.DataFrame(["value"], columns=["Header"]))


if __name__ == "__main__":
    main()
