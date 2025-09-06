# -*- coding: utf-8 -*-
"""
author: UnicornOnAzur

This script demonstrates the use of an Immediately Invoked Function Expression
(IIFE) in Python.
"""
import typing


def iife(func: typing.Callable) -> typing.Callable:
    """
    A decorator that immediately invokes the passed function.

    Parameters:
        func : The function to be invoked immediately.

    Returns:
        The return value of the invoked function.
    """
    return func()


@lambda _: _()
def func_version_1() -> int:
    """
    Function that prints a message and returns a value.

    Parameters:
        None
    
    Returns:
        int: A value
    """
    print("hello from version 1")
    return 1


@iife
def func_version_2() -> int:
    """
    Function that prints a message and returns a value.

    Parameters:
        None

    Returns:
        int: A value
    """
    print("hello from version 2")
    return 2


@iife
def _() -> None:
    """Open a web browser with the selected text as a query parameter."""
    import webbrowser
    import win32ui

    wnd = win32ui.GetForegroundWindow()

    # Get the selected text from the clipboard
    selected_text: str = wnd.GetWindowText()

    # Define the base URL
    base_url: str = "http://localhost:8501"

    # Append the selected text as a query parameter
    custom_url: str = f"{base_url}?query={selected_text}"

    # Open the URL in a new browser window
    webbrowser.open_new(custom_url)


if __name__ == "__main__":
    print(func_version_1)
    print(func_version_2)
