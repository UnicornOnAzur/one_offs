"""
This module provides functions to demonstrate writing CSV files using both
the pandas library and the standard csv library. It includes examples of
handling UTF-8 encoding with Byte Order Marks (BOM) and adding prefixes
to data entries.
"""
# Standard library
import codecs  # For the BOM
import csv
import _csv  # For type hinting the
import io
import typing
# Third party
import pandas as pd
# Constants
FLD: str = "output/"


def encoding_a_csv() -> None:
    """
    This function demonstrates how to write CSV files using pandas and the
    standard csv library, including handling of UTF-8 encoding and the
    addition of a Byte Order Mark (BOM).
    """
    names: typing.List[str] = ["John", "محمد", "François", "Иван", "José"]
    df: pd.DataFrame = pd.DataFrame({"Name": names})
    byte_order_marker: str = codecs.BOM_UTF8.decode("utf-8")  # Convert to text

    # Pandas: write CSV without and with encoding
    df.to_csv(f"{FLD}pd_without_encoding.csv", index=False, encoding="utf-8")
    df.to_csv(f"{FLD}pd_with_encoding.csv", index=False, encoding="utf-8-sig")

    # Pandas: write CSV with manually adding the BOM
    with io.StringIO() as output, open(f"{FLD}pd_with_manual_encoding.csv",
                                       mode="w", encoding="utf-8") as file:
        df.to_csv(output, index=False, lineterminator="\n")
        csv_with_bom: str = byte_order_marker + output.getvalue()
        file.writelines(csv_with_bom)

    # CSV: write CSV with encoding
    with open(f"{FLD}csv_with_encoding.csv", mode="w",
              encoding="utf-8-sig", newline="") as file:
        writer: _csv.Writer = csv.writer(file)
        writer.writerow(["Name"])
        for name in names:
            writer.writerow([name])

    # CSV: write CSV with manually added BOM
    with open(f"{FLD}csv_with_manual_encoding.csv", mode="w",
              encoding="utf-8", newline="") as file:
        writer: _csv.Writer = csv.writer(file)
        writer.writerow([byte_order_marker + "Name"])
        for name in names:
            writer.writerow([name])


def adding_a_prefix() -> None:
    """
    This function demonstrates how to write CSV files with and without a
    prefix for the data, using both pandas and the standard csv library.
    """
    prefix: str = chr(13)
    data: typing.Dict[str, typing.List[str]] = {
        "Phone number": ["0612345678"],
        "Leading zeros": ["00878"],
        "Exponential notation": ["2E+10"]}
    df: pd.DataFrame = pd.DataFrame(data)

    # Pandas: write to CSV without prefix
    df.to_csv(f"{FLD}pd_without_prefix.csv", index=False)

    # Pandas: add prefix and write to CSV
    df: pd.DataFrame = df.apply(lambda x: prefix + x)
    df.to_csv(f"{FLD}pd_with_prefix.csv", index=False)

    # CSV: write to CSV without prefix
    with open(f"{FLD}csv_without_prefix.csv", mode="w", newline="") as file:
        writer: _csv.Writer = csv.writer(file)
        writer.writerow(data.keys())
        writer.writerow([data_[0] for data_ in data.values()])

    # CSV: add prefix and write to CSV
    with open(f"{FLD}csv_with_prefix.csv", mode="w", newline="") as file:
        writer: _csv.Writer = csv.writer(file)
        writer.writerow(data.keys())
        writer.writerow([prefix + data_[0] for data_ in data.values()])


if __name__ == "__main__":
    encoding_a_csv()
    adding_a_prefix()
