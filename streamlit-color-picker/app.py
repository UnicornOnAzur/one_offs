"""
Module for demonstrating theme colors in a Streamlit application.

This module provides functionality to read and write theme colors from
a TOML configuration file, reset the configuration to default values,
and manage user interactions through a Streamlit interface.

author: UnicornOnAzur
"""
# Standard library
import functools
import glob
import tomllib
import types
import typing
# Third party
import pandas as pd
import streamlit as st
import streamlit.runtime.scriptrunner_utils.script_run_context as run_context
import toml
# Constants
HEADER: str = "theme"


@lambda _: _()
def determine_path() -> None:
    """
    Determines the file paths for TOML and TXT files based on the current URL.
    """
    global FOLDER_PATH, TOML_FILE_PATH, TXT_FILE_PATH
    context: run_context.ScriptRunContext = run_context.get_script_run_ctx()
    current_url: str = context.context_info.url
    FOLDER_PATH = "" if "localhost" in current_url else\
        "**/*streamlit-color-picker*/"
    TOML_FILE_PATH = next(glob.iglob(f"{FOLDER_PATH}.streamlit/*.toml",
                                     recursive=True))
    TXT_FILE_PATH = next(glob.iglob(f"{FOLDER_PATH}default.txt",
                                    recursive=True))


def set_place_of_a_widget_on_a_row_of(number_of_columns: int = 2
                                      ) -> typing.Callable[...,
                                                           st._DeltaGenerator]:
    """
    A decorator to arrange the widget in a specified number of columns.

    Parameters:
        number_of_columns : The number of columns to arrange the outputs.

    Returns:
        A wrapper function that manages column placement.
    """
    def decorator(func: typing.Callable[
        [str, st._DeltaGenerator | types.ModuleType], st._DeltaGenerator]
              ) -> typing.Callable[..., st._DeltaGenerator]:
        """
        Wraps the original function to manage column placement. Initializes
        wrapper.count and wrapper.columns to maintain state.

        Parameters:
            func : The function to be wrapped.

        Returns:
            The wrapper function that manages column placement.
        """
        @functools.wraps(func)
        def wrapper(
                *args: typing.Tuple[str, st._DeltaGenerator | types.ModuleType]
                ) -> st._DeltaGenerator:
            """
            Manages the placement of widgets in columns. Uses wrapper.count and
            wrapper.columns to maintain state.

            Parameters:
                *args : The field name and page segment.

            Returns:
                st._DeltaGenerator: The widget created by the inner function.
            """
            name, page_segment = args
            if wrapper.count % number_of_columns == 0:
                wrapper.columns = page_segment.columns(number_of_columns)
            widget: st._DeltaGenerator = func(
                name, wrapper.columns[wrapper.count % number_of_columns])
            wrapper.count += 1
            return widget
        wrapper.count = 0
        wrapper.columns = []  # typing.List[st._DeltaGenerator]
        return wrapper
    return decorator


@set_place_of_a_widget_on_a_row_of(3)
def create_color_picker(
        field_name: str, column: st._DeltaGenerator
        ) -> st._DeltaGenerator:
    """
    Creates a color picker widget in the specified column.

    Parameters:
        field_name : The name of the field for the color picker.
        column : The column where the color picker will be placed.

    Returns:
        The color picker widget.
    """
    return column.color_picker(
        field_name, value=st.session_state.get(field_name, None),
        key=field_name)


def create_download_button(column: st._DeltaGenerator) -> bool:
    with open(TOML_FILE_PATH, "rb") as file:
        return column.download_button("Download button", data=file,
                                      file_name="config.toml")


def create_file_uploader(column: st._DeltaGenerator, name: str) -> None:
    uploaded_file: typing.Optional[
        st.runtime.uploaded_file_manager.UploadedFile] = column.file_uploader(
        "Upload a TOML file.", type=".toml",
        key=f"uploader_{name}_{st.session_state.uploader_key}")
    if uploaded_file is not None:
        with open(TOML_FILE_PATH, "w") as file:
            toml.dump(tomllib.load(uploaded_file), file)
        st.session_state.uploader_key += 1


def read_toml_to_dict() -> typing.Dict[str, str]:
    """
    Read the TOML file to a dictionary and read the keys within the 'theme'
    header.
    """
    with open(TOML_FILE_PATH, "rb") as file:
        return tomllib.load(file)[HEADER]


def write_session_state_to_toml() -> None:
    """
    Creates a TOML file by creating a dictionary from the session state and add
    a header.
    """
    with open(TOML_FILE_PATH, "w") as file:
        toml.dump({HEADER:
                   {key: st.session_state[key] for key in COLOR_FIELDS}}, file)


def reset_toml_file_to_default() -> None:
    with (open(TXT_FILE_PATH) as text_file,
          open(TOML_FILE_PATH, "w") as toml_file):
        toml_file.write(text_file.read())


def color_cells_by_value(values: pd.Series) -> typing.List[str]:
    """
    Applies background color styles to cells based on their values.

    Parameters:
        values: A list of color values.

    Returns:
        A list of CSS style strings for background colors.
    """
    return [f"background-color: {value}" for value in values]


def main() -> None:
    """
    Main function to run the Streamlit application.
    """
    # Create variables for the app
    global COLOR_FIELDS
    COLOR_FIELDS = []
    st.set_page_config(layout="wide")
    theme: typing.Dict[str, str] = read_toml_to_dict()
    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = 0
    for key, value in theme.items():
        st.session_state[key] = value
        COLOR_FIELDS.append(key)
    left, right = st.columns(2)
    # LEFT: changing colors and displaying the current value
    left.header("Change a color")
    form = left.form("form")
    for field in COLOR_FIELDS:
        create_color_picker(field, form)
    form.form_submit_button(on_click=write_session_state_to_toml)
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
    create_download_button(rc2)
    create_file_uploader(rc3, "rc3")
    right.multiselect("Multiselect", options=COLOR_FIELDS,
                      default=COLOR_FIELDS[-1])
    container = right.container(border=True)
    container.subheader("Inside a container")
    container.markdown(("This is Markdown test. "
                        "This is `inline code` in Markdown. "
                        "This is a link to the [Streamlit docs]()."))
    container.code("for i in range(9): print(i)")
    right.dataframe(data=pd.DataFrame(["value"], columns=["Header"]))
    # SIDEBAR: Mimick the right panel
    sidebar = st.sidebar
    sidebar.header("Sidebar")
    sc1, sc2, sc3 = sidebar.columns(3)
    sc1.button("Reset toml file", type="primary",
               on_click=reset_toml_file_to_default)
    sc2.button("Secondary button", type="secondary")
    sc3.button("Tertiary button", type="tertiary")
    sc1.link_button("Link button", url="")
    create_download_button(sc2)
    create_file_uploader(sc3, "sc3")
    sidebar.multiselect("Multiselect", options=COLOR_FIELDS,
                        default=COLOR_FIELDS[-1])
    container_sidebar = sidebar.container(border=True)
    container_sidebar.subheader("Inside a container")
    container_sidebar.markdown(("This is Markdown test. "
                                "This is `inline code` in Markdown. "
                                "This is a link to the [Streamlit docs]()."))
    container_sidebar.code("for i in range(9): print(i)")
    sidebar.dataframe(data=pd.DataFrame(["value"], columns=["Header"]))


if __name__ == "__main__":
    main()
