"""
This module demonstrates the use of Python's built-in functions such as zip,
enumerate, and map. It provides various examples of how these functions can
be utilized to manipulate iterators and visualize data using matplotlib.

author: UnicornOnAzur
"""
# Standard library
import typing
# Third party
import matplotlib.pyplot as plt
# Matplotlib settings
plt.rcParams["axes.titlesize"] = 7


def _stringify_iterator(
    description: str,
    iterator: typing.Iterator
        ) -> str:
    """
    Converts an iterator to a string representation.

    Parameters:
        description : A description of the iterator.
        iterator : The iterator to be converted.

    Returns:
        A string representation of the iterator.
    """
    if not (items := tuple(iterator)):  # Check if the iterator is empty
        return f"{description} ()"  # Return description with empty brackets
    return f"{description} {'  '.join(map(str, items))}"


def zip_function():
    """
    Demonstrates the use of the zip function with various arguments.
    """
    a, b, c = ["1", "1", "1"], range(2, 8, 2), (3, 6, 9)
    print(_stringify_iterator("zip() with no arguments:", zip()))
    print(_stringify_iterator("zip() with one arguments:", zip(a)))
    print(_stringify_iterator("zip() with two arguments:", zip(a, b)))
    print(_stringify_iterator("zip() with three arguments:", zip(a, b, c)))


def zip_function_with_unpack_on_enumerate():
    """
    Demonstrates the use of enumerate and zip with unpacking.
    """
    data = range(20, 1, -2)
    print(_stringify_iterator("enumarate:", enumerate(data)))
    print(_stringify_iterator("map a tuple on enumerate:",
                              map(tuple, enumerate(data))))
    print(_stringify_iterator("map a list on enumerate:",
                              map(list, enumerate(data))))
    #
    print(_stringify_iterator("enumarate and zip:", zip(enumerate(data))))
    print(_stringify_iterator("map a tuple on enumerate and zip:",
                              map(tuple, zip(enumerate(data)))))
    print(_stringify_iterator("map a list on enumerate and zip:",
                              map(list, zip(enumerate(data)))))
    #
    print(_stringify_iterator("unpack enumarate into zip:",
                              zip(*enumerate(data))))


def zip_on_two_lists():
    """
    Demonstrates the use of zip with two lists and various mappings.
    """
    data, index = range(20, 1, -2), range(0, 20, 2)
    print(_stringify_iterator("zip() on two lists", zip(index, data)))
    print(_stringify_iterator("zip() on unpacking a list of lists:",
                              zip(*[index, data])))
    print(_stringify_iterator("mapping a tuple on the zip:",
                              map(tuple, zip(index, data))))
    print(_stringify_iterator("mapping a list on the zip:",
                              map(list, zip(index, data))))
    print(_stringify_iterator("a double zip:", zip(zip(index, data))))
    print(_stringify_iterator("mapping a tuple on the double zip:",
                              map(tuple, zip(zip(index, data)))))
    print(_stringify_iterator("mapping a list on the double zip:",
                              map(list, zip(zip(index, data)))))


def matrix_transposing():
    """
    Demonstrate the similarity in transposing a matrix.
    """
    row1 = [1, 2, 3]
    row2 = [4, 5, 6]
    row3 = [7, 8, 9]
    matrix = [row1, row2, row3]
    print(_stringify_iterator("zip(row1, row2, row3):", zip(row1, row2, row3)))
    print(_stringify_iterator("zip(*matrix):", zip(*matrix)))


def plot():
    """
    Creates a plot demonstrating different inputs using matplotlib.
    """
    fig, axes = plt.subplots(ncols=4, figsize=(7, 4),
                             subplot_kw={'xticks': [], 'yticks': []})
    fig.subplots_adjust(wspace=.2, left=.01, right=.99, bottom=.01)
    fig.suptitle("Demonstration of the different inputs")
    sizes = [(i, i**3) for i in range(10)]
    size_d, size_c = list(zip(*sizes))
    axes[0].set_title("Unpack list of lists")
    axes[0].plot(*sizes)
    axes[1].set_title("List zip of unpacked list")
    axes[1].plot(list(zip(*sizes)))
    axes[2].set_title("Unpacked list zip of unpacked list")
    axes[2].plot(*list(zip(*sizes)))
    axes[3].set_title("Separate lists")
    axes[3].plot(size_d, size_c)
    fig.savefig("output/demo.png")


def demo():
    """
    Executes the demonstration functions.
    """
    zip_function()
    print("="*20)
    zip_function_with_unpack_on_enumerate()
    print("="*20)
    zip_on_two_lists()
    print("="*20)
    matrix_transposing()
    plot()


if __name__ == "__main__":
    demo()
