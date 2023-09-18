"""
Prototype of utils for testing with mypy
"""

import inspect
from typing import Any
from mypy import api
from os.path import abspath, dirname, basename
#from os.path import split as path_split


def get_mypy_version():
    """
    Returns the version of mypy used for the tests
    """

    return api.run(["--version"])[0].split('(')[0]


def absolute_path_mypy_result(file_name: str) -> tuple[str, str, int]:
    """
    Returns the mypy result for a file, given the absolute path to that file
    Somehow this finds the pyprojet.toml at the root of the project

    @param file_name: file name, ideally from the __file__ variable of a python file
    @return: mypy.api.run result (3-tuple of string (mypy stdout, the type errors), string (mypy stderr output), and int (mypy exit code))
    """

    abs_file = abspath(file_name)

    mypy_result = api.run([abs_file])#, "--config-file", "pyproject.toml"])

    ### OLD VERSION:
    ## NEEDS a pyproject.toml file in the root directory
    ## HARDCODED: root directory is 2 directories up from this file
    #mypy_result = api.run([f"{abs_path}/test_types.py",
                      #"--config-file",
                      #f"{path_split(path_split(abs_path)[0])[0]}/pyproject.toml"
                    #])

    return mypy_result


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


def object_mypy_error_report(function_or_class_name: Any, file_name: str) -> tuple[tuple[int, str], ...]:
    """
    Returns the errors and line numbers from a mypy.api.run result,
    where the function or class definition is involved

    @param function_or_class_name: function or class
    @param file_name: file name, ideally from the __file__ variable
    @return: tuple containing tuples of line numbers and error messages
    """

    mypy_result = absolute_path_mypy_result(file_name)
    errors, errors_line_numbers = get_type_errors_and_line_numbers(mypy_result)
    start_lineno, end_lineno = get_function_or_class_line_numbers(function_or_class_name)

    errors_mentioning_object = []

    for index, error in enumerate(errors):
        if start_lineno <= errors_line_numbers[index] <= end_lineno:
            errors_mentioning_object.append((errors_line_numbers[index],
                                            f"mypy error message: {error}"))

    return tuple(errors_mentioning_object)
