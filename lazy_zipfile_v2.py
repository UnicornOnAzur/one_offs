# -*- coding: utf-8 -*-
"""
@author: UnicornOnAzur

A method to lazily read the contents of a ZIP file. This approach allows for
memory-efficient handling of potentially large files by yielding their contents
only when requested, rather than loading everything into memory at once.
"""
# Standard library
import itertools
import typing
import warnings
import zipfile


class LazyZIPdict(dict):
    """
    A dictionary subclass that lazily retrieves values from a zip object.

    This class overrides the __getitem__ method to return the next item from
    the iterator of the value associated with the given key. If the value is
    not an iterator, it raises a TypeError.
    """

    def __getitem__(self, key: str) -> bytes:
        """
        Retrieve the next item from the iterator associated with the given key.

        Parameters
        ----------
        key : str
            The key for which to retrieve the next item.

        Returns
        -------
        bytes
            The next item from the iterator.

        Raises
        ------
        TypeError
            If the value for the key is not iterable.
        """
        value: typing.Generator[bytes, None, None] = super().__getitem__(key)
        if not hasattr(value, '__iter__'):
            raise TypeError(f"The value for key '{key}' is not iterable.")
        return next(value)

    def contents(self):
        """
        Prints the keys of the object in a formatted manner.

        This method retrieves all the keys from the object and prints them,
        each on a new line. It is useful for quickly viewing the contents
        of the object.

        Returns
        -------
            None
        """
        print("\n".join(sorted(self.keys())))


def lazy_read_zip_file_contents(path: str
                                ) -> LazyZIPdict:
    """
    Reads the contents of a ZIP file lazily by returning a dictionary
    comprehension where all the file names are mapped to a generator that
    yields the bytes content. The content can be retrieved by calling the
    generator.

    >>> zp_dict = lazy_read_zip_file_contents("file.zip")
    >>> file_contents = zp_dict[filename]

    Parameters
    ----------
    path : str
        The path to the ZIP file.

    Returns
    -------
    LazyZIPdict
        A dictionary with file names as keys and the content as values.

    Raises
    ------
    warnings
        If the ZIP file is invalid or cannot be accessed.

    """
    try:
        with zipfile.ZipFile(path, "r", allowZip64=True) as zip_file:
            return LazyZIPdict({file_name: (file
                                            for file
                                            in itertools.repeat(
                                                zip_file.read(file_name))
                                            )
                                for file_name in zip_file.namelist()})
    # Handle the case where the ZIP file is invalid
    except (zipfile.BadZipFile, PermissionError) as exception:
        warnings.warn(f"{exception}: {path}")


def demo(depth: int = 3):
    """
    Demonstrates the usage of lazy_read_zip_file_contents by scanning for and
    opening zip files to map their content size againts the size of the
    generated dictionaries.

    Parameters
    ----------
    depth : int, default 3.
        The depth of the directory structure to search for ZIP files.

    Returns
    -------
    None.

    """
    import glob
    import os
    import sys
    import matplotlib.pyplot as plt

    sizes: typing.List[tuple] = []
    search_path: str = os.path.join(*[".."]*max(abs(depth), 1), "**", "*.zip")
    paths: typing.Generator[str, None, None] = glob.iglob(search_path,
                                                          recursive=True)

    for path in paths:
        dic: typing.Dict = lazy_read_zip_file_contents(path)
        # skip the file if its empty
        if not dic:
            continue

        size: int = sys.getsizeof(dic)
        content_size: typing.List = []
        for key in dic:
            try:
                content_size.append(sys.getsizeof(dic[key]))
            except RuntimeError as e:
                print(e)

        print(f"The size of the dictionary is: {size} bytes.")
        print(f"The size of the content is: {max(content_size)} bytes.")
        sizes.append((sum(content_size)/size, max(content_size)))

    if not sizes:
        print("No ZIP files were found.")
        return
    size_d, size_c = list(zip(*sizes))

    _, ax = plt.subplots(figsize=(10, 7))
    ax.scatter(size_d, size_c, c="orange")
    plt.xscale("log")
    plt.yscale("log")
    ax.set_xlabel("Rate of total content size to dictionary size in memory")
    ax.set_ylabel("Content Size")
    plt.title("Comparison of Dictionary and Content")
    plt.show()


if __name__ == "__main__":
    demo()
