"""
Module for demonstrating theme colors in a Streamlit application. This module
provides functionality to read and write theme colors from a TOML
configuration file, reset the configuration to default values, and manage user
interactions through a Streamlit interface.

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
import toml
# Constants
COLOR_FIELDS: list[str] = []
THEME_HEADER: str = "theme"
StreamlitObject = st._DeltaGenerator
StreamlitPageSegment = StreamlitObject | types.ModuleType
WrappedFunction = typing.Callable[[str, StreamlitPageSegment], None]


###############################################################################
# General                                                                     #
###############################################################################
def is_app_running_locally() -> bool:
    """
    This function checks the current URL from the script run context to
    ascertain if it contains 'localhost', indicating a local run.

    Parameters:
        None

    Returns:
        True if the application is running locally, False otherwise.
    """
    if (url := st.context.url) is not None:
        return url.startswith("http://localhost")
    return False


@lambda _: _()
@st.cache_data()
def determine_path() -> typing.Tuple[str, str]:
    """
    Determines the file paths for TOML and TXT files based on the current URL.

    Parameters:
        None

    Returns:
        The file paths for the TOML and TEXT file.
    """
    folder_path: str = "" if is_app_running_locally() else\
        "**/*streamlit-color-picker*/"
    toml_file_path: str = next(glob.iglob(f"{folder_path}.streamlit/*.toml",
                                          recursive=True))
    text_file_path: str = next(glob.iglob(f"{folder_path}default.txt",
                                          recursive=True))
    return toml_file_path, text_file_path


TOML_FILE_PATH, TXT_FILE_PATH = determine_path


def color_cells_by_value(values: pd.Series) -> typing.List[str]:
    """
    Creates CSS background color styles for cells based on their values.

    Parameters:
        values: A list of color values.

    Returns:
        A list of CSS style strings for background colors.
    """
    return [f"background-color: {value}" for value in values]


###############################################################################
# Streamlit widget related functions                                          #
###############################################################################
def set_widget_in_columns(
        number_of_columns: int = 2
        ) -> typing.Callable[[WrappedFunction], WrappedFunction]:
    """
    A decorator to arrange the widget in a specified number of columns.

    Parameters:
        number_of_columns : The number of columns to arrange the outputs.

    Returns:
        A wrapper function that manages column placement.
    """
    def decorator(func):
        """
        Wraps the original function to manage column placement. Initializes
        wrapper.count and wrapper.columns to maintain state.

        Parameters:
            func : The function to be wrapped.

        Returns:
            The wrapper function that manages column placement.
        """
        @functools.wraps(func)
        def wrapper(name: str, page_segment: StreamlitPageSegment) -> None:
            """
            Manages the placement of widgets in columns. Uses wrapper.count and
            wrapper.columns to maintain state.

            Parameters:
                name : The field name and page segment.
                page_segment: The Streamlit page element where the columns are
                created in.

            Returns:
                None
            """
            if not wrapper.columns:
                wrapper.columns = page_segment.columns(number_of_columns)
            func(name, wrapper.columns[wrapper.count % number_of_columns])
            wrapper.count += 1
        wrapper.count = 0
        wrapper.columns = []
        return wrapper
    return decorator


@set_widget_in_columns(3)
def create_color_picker(field_name: str, column: StreamlitPageSegment) -> None:
    """
    Creates a color picker widget in the specified column.

    Parameters:
        field_name : The name of the field for the color picker.
        column : The column where the color picker will be placed.

    Returns:
        None
    """
    column.color_picker(field_name, key=field_name)


def create_download_button(column: StreamlitObject) -> None:
    """
    Creates a download button in the specified column for downloading a TOML
    configuration file.


    Parameters:
        column: The column where the color picker will be placed.

    Returns:
        None
    """
    with open(TOML_FILE_PATH, "rb") as file:
        column.download_button("Download button", data=file,
                               file_name="config.toml")


def create_file_uploader(column: StreamlitObject, name: str) -> None:
    """
    Creates a file uploader in the specified column for uploading a TOML file.

    Parameters:
        column: The column where the uploader will be placed.
        name: The unique name of the uploader.

    Returns:
        None
    """
    uploaded_file: typing.Optional[
        st.runtime.uploaded_file_manager.UploadedFile] = column.file_uploader(
        "Upload a TOML file.", type=".toml",
        key=f"uploader_{name}_{st.session_state.uploader_key}")
    if uploaded_file is not None:
        with open(TOML_FILE_PATH, "w") as file:
            toml_input = tomllib.load(uploaded_file)
            toml.dump(toml_input, file)
        st.session_state.uploader_key += 1


def create_page_segment(segment: StreamlitObject, header_text: str) -> None:
    """
    Creates a segmented page layout in Streamlit with various interactive
    components.

    Parameters:
    segment : The Streamlit segment object to which components will be added.
    header_text : The text to be displayed as the header of the segment.
    """
    segment.header(header_text)
    # Create three columns within the segment
    col1: StreamlitObject
    col2: StreamlitObject
    col3: StreamlitObject
    col1, col2, col3 = segment.columns(3)
    # Left column
    col1.button("Reset toml file", type="primary",
                on_click=reset_toml_file_to_default)
    col1.link_button("Link button", url="")
    col1.success("Success!")
    col1.badge("Badge", color="primary")  # To show the use of primaryColor
    col1.exception(ValueError())
    # Middle column
    col2.button("Secondary button", type="secondary")
    create_download_button(col2)
    col2.warning("Warning!")
    col2.info("Info!")
    col2.toggle("Toggle")
    # Right column
    col3.button("Tertiary button", type="tertiary")
    create_file_uploader(col3, header_text)
    col3.error("Error!")
    col3.metric("Metric", value=1)
    # Expander
    with segment.expander(label="Expander", expanded=True):
        tab1, tab2 = st.tabs(["tab1", "tab2"])
        tab1.pills(label="Pills", options=COLOR_FIELDS)
        tab2.help(print)
    # Multiselect
    segment.multiselect("Multiselect", options=COLOR_FIELDS,
                        default=COLOR_FIELDS[:3])
    # Container
    container: StreamlitObject = segment.container(border=True)
    container.subheader("Inside a container")
    container.markdown(("This is Markdown test. "
                        "This is `inline code` in Markdown. "
                        "This is a link to the [Streamlit docs]()."))
    container.code("for i in range(9): print(i)")
    # Bottom
    segment.dataframe(data=pd.DataFrame(["value"], columns=["Header"]))
    segment.caption("Caption")


###############################################################################
# TOML related functions                                                      #
###############################################################################
def read_toml_to_dict() -> typing.Dict[str, str]:
    """
    Read the TOML file to a dictionary and read the keys within the 'theme'
    header.

    Parameters:
        None

    Returns:
        A dictionary containing the keys and values under the theme header.

    Raises:
        KeyError: If the specified theme header is missing in the TOML file.
    """
    with open(TOML_FILE_PATH, "rb") as file:
        try:
            return tomllib.load(file)[THEME_HEADER]
        except KeyError:
            st.toast(f"TOML is missing a {THEME_HEADER} header")
            reset_toml_file_to_default()
            return tomllib.load(file)[THEME_HEADER]


def write_session_state_to_toml() -> None:
    """
    Creates a TOML file by creating a dictionary from the session state and add
    a header.

    Parameters:
        None

    Returns:
        None
    """
    with open(TOML_FILE_PATH, "w") as file:
        toml.dump({THEME_HEADER:
                   {key: st.session_state[key] for key in COLOR_FIELDS}}, file)


def reset_toml_file_to_default() -> None:
    """
    Resets the TOML file to its default state by copying content from a text
    file.

    Parameters:
        None

    Returns:
        None
    """
    with (open(TXT_FILE_PATH) as text_file,
          open(TOML_FILE_PATH, "w") as toml_file):
        toml_file.write(text_file.read())


###############################################################################
# MAIN loop                                                                   #
###############################################################################
def main() -> None:
    """
    Main function to run the Streamlit application.

    Returns:
        None
    """
    # Create variables for the app
    st.set_page_config(layout="wide")
    theme: typing.Dict[str, str] = read_toml_to_dict()
    if "uploader_key" not in st.session_state:
        st.session_state["uploader_key"] = 0
    for key, value in theme.items():
        if "Color" not in key:  # skip values that aren't colors
            continue
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
    theme_settings_table: pd.DataFrame = pd.DataFrame().from_dict(
        read_toml_to_dict(), orient="index")
    left.table(theme_settings_table.style.apply(
        color_cells_by_value, axis=1,
        subset=[0] if not theme_settings_table.empty else None
        ), hide_header=True)
    # RIGHT: Showcasing the use of the colors by Streamlit
    create_page_segment(right, "See the colors")
    # SIDEBAR: Showcasing the use of the colors by Streamlit
    sidebar = st.sidebar
    create_page_segment(sidebar, "See the colors in the sidebar")


if __name__ == "__main__":
    main()
