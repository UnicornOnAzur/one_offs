# -*- coding: utf-8 -*-
"""
@author: UnicornOnAzur

"""
# Standard library
import typing
import warnings
import zipfile


def lazy_read_zip_file_contents(path: str
                                ) -> typing.Dict[str,
                                                 typing.Generator[bytes,
                                                                  None,
                                                                  None]]:
    """
    Reads the contents of a ZIP file lazily by returning a dictionary
    comprehension where all the file names are mapped to a generator that
    yields the bytes content. The content can be retrieved by calling the
    generator.

    >>> zp_dict = lazy_read_zip_file_contents("file.zip")
    >>> file_contents = next(zp_dict[filename])

    Parameters
    ----------
    path : str
        The path to the ZIP file.

    Returns
    ------
    typing.Dict[str, typing.Generator[bytes, None, None]]:
        A dictionary with file names as keys and generators with the content as
        values.

    """
    def _read_file_contents(filename: str) -> typing.Generator[bytes,
                                                               None,
                                                               None]:
        """
        Reads the contents of a specific file within the ZIP file.

        Parameters
        ----------
        filename : str
            The name of the file in the ZIP file to read.

        Yields
        ------
        typing.Generator[bytes, None, None]
            The contents of the file.

        """
        with zipfile.ZipFile(path, allowZip64 = True) as zf:
            yield zf.read(filename)

    try:
        with zipfile.ZipFile(path, allowZip64 = True) as zip_file:
            return {file_name: _read_file_contents(file_name)
                    for file_name in zip_file.namelist()}
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
                content_size.append(sys.getsizeof(next(dic[key])))
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
