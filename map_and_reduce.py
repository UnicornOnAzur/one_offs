# -*- coding: utf-8 -*-
"""
author: UnicornOnAzur

This module provides a function to apply a series of functions to each element
of an iterable and reduce the results using a specified reduction strategy.
"""
# Standard library
import functools
import typing


def map_and_reduce(
    initial_values: typing.Any,
    functions: typing.Iterable[typing.Callable[[typing.Any], typing.Any]]
        ) -> typing.List[typing.Any]:
    """
    Applies a list of functions to each element of an iterable and reduces the
    results.

    Parameters:
        initial_value : An iterable containing the initial values.
        functions : A list of functions to apply.

    Returns:
        A list of results after applying the functions and reducing them.

    Raises:
        TypeError: If initial_value is not an iterable.
    """
    def _reduce_function(
        value,
        _functions: typing.Iterable[typing.Callable[[typing.Any], typing.Any]]
            ) -> typing.Any:
        """
        Reduces a value by applying a series of functions.

        Args:
            value : The initial value to reduce.
            _functions : A list of functions to apply.

        Returns:
            The reduced value after applying the functions.
        """
        return functools.reduce(
            lambda accumulated_value, func: func(accumulated_value),
            _functions,
            value
            )

    # Ensure initial_value is iterable
    if not isinstance(initial_values, typing.Iterable):
        raise TypeError("initial_value must be an iterable (list or tuple)")

    partial_function: typing.Callable = functools.partial(
        _reduce_function,
        _functions=functions)
    return list(map(partial_function, initial_values))


def demo():
    def multiply_by_10(value_in):
        return value_in * 10

    def remove_last_element(value_in):
        return value_in[:-1]

    def take_even_elements(value_in):
        return value_in[::2]

    def return_length(value_in):
        return len(value_in)

    functions_list: typing.List[typing.Callable] =\
        [multiply_by_10, remove_last_element,
         take_even_elements, return_length]
    value: str = ""
    values = ["", "g", [1]]

    print(f"{value=}")
    print(map_and_reduce(initial_values=value,
                         functions=functions_list))
    print(f"{values=}")
    print(map_and_reduce(initial_values=values,
                         functions=functions_list))


if __name__ == "__main__":
    demo()
