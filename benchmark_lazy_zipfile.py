"""
This module benchmarks the time and memory usage of reading small and large
zip files using two different lazy loading implementations. It provides
functions to handle zip files, perform benchmarks, and visualize the results
using matplotlib.

author:
"""
# Standard library
import pathlib
import timeit
import typing
# Third party
import matplotlib.pyplot as plt
import memory_profiler
# Local imports
import lazy_zipfile
import lazy_zipfile_v2
# Constants
TEST_FILE_SMALL: pathlib.WindowsPath =\
    pathlib.Path("C:/Users/joost/code/test_small.zip")
FILE_SMALL: str = "fig1.png"
TEST_FILE_LARGE: pathlib.WindowsPath =\
    pathlib.Path("C:/Users/joost/code/test_big.zip")
FILE_LARGE: str = "Git-2.47.0.2-64-bit.exe"


def handle_small_1() -> None:
    """Read the contents of a small zip file using lazy_zipfile."""
    next(lazy_zipfile.lazy_read_zip_file_contents(TEST_FILE_SMALL)[FILE_SMALL])


def handle_small_2() -> None:
    """Read the contents of a small zip file using lazy_zipfile_v2."""
    lazy_zipfile_v2.lazy_read_zip_file_contents(TEST_FILE_SMALL)[FILE_SMALL]


def handle_large_1() -> None:
    """Read the contents of a large zip file using lazy_zipfile."""
    next(lazy_zipfile.lazy_read_zip_file_contents(TEST_FILE_LARGE)[FILE_LARGE])


def handle_large_2() -> None:
    """Read the contents of a large zip file using lazy_zipfile_v2."""
    lazy_zipfile_v2.lazy_read_zip_file_contents(TEST_FILE_LARGE)[FILE_LARGE]


def benchmark_time(iterations: int = 1) -> typing.Tuple[float,
                                                        float,
                                                        float,
                                                        float]:
    """Benchmark the time taken to read small and large zip files."""
    result1_small = timeit.timeit("handle_small_1()",
                                  globals=globals(),
                                  number=iterations)
    result2_small = timeit.timeit("handle_small_2()",
                                  globals=globals(),
                                  number=iterations)
    result1_small = timeit.timeit("handle_large_1()",
                                  globals=globals(),
                                  number=iterations)
    result2_large = timeit.timeit("handle_large_2()",
                                  globals=globals(),
                                  number=iterations)
    return result1_small, result2_small, result1_small, result2_large


def benchmark_memory(interval: float) -> typing.Tuple[typing.List[float],
                                                      typing.List[float],
                                                      typing.List[float],
                                                      typing.List[float]]:
    """Benchmark the memory usage of reading small and large zip files."""
    memory_used1_small = memory_profiler.memory_usage((handle_small_1),
                                                      interval=interval)
    memory_used1_large = memory_profiler.memory_usage((handle_large_1),
                                                      interval=interval)
    memory_used2_small = memory_profiler.memory_usage((handle_small_2),
                                                      interval=interval)
    memory_used2_large = memory_profiler.memory_usage((handle_large_2),
                                                      interval=interval)
    return (memory_used1_small, memory_used1_large,
            memory_used2_small, memory_used2_large)


def main():
    """Main function to execute benchmarks and plot results."""
    timed_results = []
    for it in [1, 10, 100, 1_000]:
        print(it, step := benchmark_time(it))
        timed_results.append(step)
    sized_results = benchmark_memory(.01)
    fig, axes = plt.subplots(nrows=2)
    x1, y1, x2, y2 = list(zip(*timed_results))
    axes[0].scatter(x1, y2, color="green", label="small")
    axes[0].scatter(x2, y2, color="red", label="large")
    axes[0].set_xlim([0, max([max(x1), max(x2)]) + 1])
    axes[0].set_ylim([0, max([max(y1), max(y2)]) + 1])
    for res, color, name in zip(sized_results,
                                ["#003f5c", "#58508d", "#bc5090", "#ff6361"],
                                ["small_1", "large_1", "small_2", "large_2"]):
        axes[1].plot(res, color=color, label=name)
    axes[1].legend(loc="upper left")
    axes[1].set_xlim([0, len(sized_results[0])])
    axes[1].set_ylim([0, max(map(max, sized_results)) + 50])
    plt.show(block=True)


if __name__ == "__main__":
    main()
