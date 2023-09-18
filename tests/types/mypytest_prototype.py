"""
Prototype of utils for testing with mypy

object_mypy_error_report is essentially a hack to get a mypy report on a single object instead of the whole file
and so get it to work with pytest function-by-function testing
mypy doesn't provide this functionality, and to test different functions we would need to create a new file for each
This might be better to not overload the tests, but the directory becomes messy
"""

import inspect
from typing import Any
from mypy import api
from os.path import abspath


def get_mypy_version() -> str:
    """
    Returns the version of mypy used for the tests
    """

    return api.run(["--version"])[0].split("(")[0]


def get_type_errors_and_line_numbers(mypy_result: tuple[str, str, int]) -> tuple[list[str], list[int]]:
    """
    Returns the errors and line numbers from a mypy.api.run result
    Discards all of the other information (notes, warnings, general resume)

    @param mypy_result: mypy.api.run result
    @return: errors (strings from mypy report), line numbers
    """

    lines = mypy_result[0].split("\n")
    error_lines = [line for line in lines if "error:" in line]

    error_line_numbers = []
    for line in error_lines:
        error_line_numbers.append(int(line.split(":")[1]))

    return error_lines, error_line_numbers


def debug_mypy(file_name: str) -> None:
    """
    A bunch of prints on mypy --strict results on the whole file to debug

    @param file_name: file name, ideally from the __file__ variable
    """
    print(f"{get_mypy_version()}strict results on {file_name}")

    abs_file = abspath(file_name)
    mypy_result = api.run([abs_file, "--strict"])
    errors, errors_line_numbers = get_type_errors_and_line_numbers(mypy_result)

    print("\nmypy typing errors for the whole file:")
    for error in errors:
        print(error)
    print(f"\nmypy typing error line numbers: {errors_line_numbers}")
    print(f"\nmypy stderr output: {mypy_result[1]}")
    print(f"\nmypy exit code: {mypy_result[2]}\n")


def get_function_or_class_line_numbers(function_or_class: Any) -> tuple[int, int]:
    """
    Returns the starting and ending line numbers where a function or class is defined

    @param function_or_class: function or class object (NOT a str)
    @return: 2-tuple containing the starting and ending line numbers
    """

    source_lines = inspect.getsourcelines(function_or_class)
    start_lineno = source_lines[1]
    end_lineno = len(source_lines[0]) + start_lineno

    return start_lineno, end_lineno


def object_mypy_error_report(
    function_or_class_name: Any, file_name: str, strict: bool = False
) -> tuple[tuple[int, str], ...]:
    """
    Returns the errors and line numbers from a mypy.api.run result,
    where the function or class definition is involved

    @param function_or_class_name: function or class
    @param file_name: file name, ideally from the __file__ variable
    @return: tuple containing tuples of line numbers and error messages
    """

    abs_file = abspath(file_name)

    if strict:
        mypy_result = api.run([abs_file, "--strict"])
    else:
        mypy_result = api.run([abs_file])

    errors, errors_line_numbers = get_type_errors_and_line_numbers(mypy_result)
    start_lineno, end_lineno = get_function_or_class_line_numbers(function_or_class_name)

    errors_mentioning_object = []

    for index, error in enumerate(errors):
        if start_lineno <= errors_line_numbers[index] <= end_lineno:
            errors_mentioning_object.append((errors_line_numbers[index], f"mypy error message: {error}"))

    return tuple(errors_mentioning_object)
