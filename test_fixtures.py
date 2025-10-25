#!/usr/bin/env python3
"""
Test fixtures for ripshit - contains realistic Python code with all searchable patterns.
This file serves as the corpus for testing ripshit pattern matching.
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Iterator
from contextlib import contextmanager
from dataclasses import dataclass


# Function definitions with various signatures
def simple_function():
    """Function with no parameters"""
    return 42


def function_with_params(name, value, count):
    """Function with multiple parameters"""
    return f"{name}: {value} x {count}"


def function_with_defaults(path="./data", timeout=30, verbose=False):
    """Function with default parameters"""
    if verbose:
        print(f"Loading from {path} with timeout {timeout}")
    return path


# Class definitions
class SimpleClass:
    """Basic class definition"""
    pass


class InheritedClass(SimpleClass):
    """Class with inheritance"""
    def __init__(self, value):
        self.value = value


class MultipleInheritance(SimpleClass, dict):
    """Class with multiple inheritance"""
    pass


# Decorators
@dataclass
class DataModel:
    """Class with decorator"""
    name: str
    count: int
    active: bool = True


@contextmanager
def custom_context():
    """Decorated function"""
    print("Setup")
    yield
    print("Teardown")


# Context managers
def file_operations():
    """Function demonstrating context managers"""
    with open("data.txt") as f:
        content = f.read()

    with open("output.json") as infile:
        data = json.load(infile)

    return content, data


def multiple_context():
    """Multiple context managers"""
    with custom_context() as ctx:
        print("Processing")

    with Path("test.txt").open() as file:
        lines = file.readlines()


# List comprehensions
def list_comprehensions():
    """Various list comprehension patterns"""
    # Basic list comprehension
    squares = [x * x for x in range(10)]

    # List comprehension with condition
    evens = [n for n in range(20) if n % 2 == 0]

    # Nested list comprehension
    matrix = [[i * j for j in range(3)] for i in range(3)]

    # List comprehension with multiple iterables
    pairs = [(x, y) for x in range(3) for y in range(3)]

    return squares, evens, matrix, pairs


# Dictionary comprehensions
def dict_comprehensions():
    """Various dictionary comprehension patterns"""
    # Basic dict comprehension
    squares_dict = {x: x * x for x in range(10)}

    # Dict comprehension with condition
    even_squares = {n: n ** 2 for n in range(20) if n % 2 == 0}

    # Dict from two lists
    keys = ['a', 'b', 'c']
    values = [1, 2, 3]
    mapping = {k: v for k, v in zip(keys, values)}

    return squares_dict, even_squares, mapping


# Set comprehensions
def set_comprehensions():
    """Set comprehension patterns"""
    # Basic set comprehension
    unique_lens = {len(word) for word in ['hello', 'world', 'test']}

    # Set comprehension with condition
    odd_squares = {x ** 2 for x in range(10) if x % 2 == 1}

    return unique_lens, odd_squares


# Generator expressions
def generator_expressions() -> Iterator:
    """Generator expression patterns"""
    # Basic generator
    squares_gen = (x * x for x in range(100))

    # Generator with condition
    even_gen = (n for n in range(1000) if n % 2 == 0)

    # Generator with function call
    lengths = (len(s) for s in ['short', 'medium', 'very_long_string'])

    return squares_gen, even_gen, lengths


# Lambda functions
def lambda_functions():
    """Lambda function patterns"""
    # Simple lambda
    add = lambda x, y: x + y

    # Lambda with single parameter
    square = lambda x: x * x

    # Lambda in sorted
    names = sorted(['Alice', 'bob', 'Charlie'], key=lambda s: s.lower())

    # Lambda in map
    doubled = list(map(lambda x: x * 2, range(5)))

    # Lambda in filter
    positives = list(filter(lambda x: x > 0, [-2, -1, 0, 1, 2]))

    return add, square, names, doubled, positives


# F-strings
def string_formatting():
    """F-string patterns"""
    name = "World"
    count = 42
    price = 19.99

    # Basic f-string
    greeting = f"Hello, {name}!"

    # F-string with expression
    result = f"The answer is {count * 2}"

    # F-string with formatting
    formatted = f"Price: ${price:.2f}"

    # Multi-line f-string
    report = f"""
    Name: {name}
    Count: {count}
    Price: ${price}
    """

    # Old-style format
    old_style = "Value: {}".format(count)
    complex_format = "{name} has {count} items".format(name=name, count=count)

    return greeting, result, formatted, report


# Imports (various patterns)
import sys
import math
from os import path
from collections import defaultdict, Counter
from typing import List as ListType
import numpy as np
from pathlib import Path as PathLib


# Exception handling
def exception_patterns():
    """Exception handling patterns"""
    try:
        result = 10 / 0
    except ZeroDivisionError as e:
        print(f"Error: {e}")

    try:
        data = json.loads("invalid")
    except (ValueError, TypeError) as err:
        print(f"Parse error: {err}")

    try:
        with open("missing.txt") as f:
            content = f.read()
    except FileNotFoundError as error:
        print("File not found")
    except IOError as io_err:
        print("IO error")


# Assertions and yields
def assertion_patterns():
    """Assert and yield patterns"""
    value = 10
    assert value > 0
    assert value < 100, "Value out of range"

    # Generator with yield
    def counter(max_val):
        for i in range(max_val):
            yield i

    # Yield with expression
    def fibonacci():
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b


# Method definitions
class DataProcessor:
    """Class demonstrating various method patterns"""

    def __init__(self, name):
        self.name = name
        self.data = []

    def process(self, items):
        """Method with self and parameter"""
        return [self._transform(item) for item in items]

    def _transform(self, item):
        """Private method"""
        return item.upper() if isinstance(item, str) else item

    def add_data(self, value, priority=1):
        """Method with default parameter"""
        self.data.append((value, priority))

    @classmethod
    def from_file(cls, filename):
        """Class method"""
        instance = cls(filename)
        return instance

    @staticmethod
    def validate(data):
        """Static method"""
        return len(data) > 0


# Variable assignments
def assignment_patterns():
    """Various assignment patterns"""
    # Simple assignments
    x = 42
    name = "test"
    count = 100

    # Numeric assignments
    pi = 3.14159
    answer = 42
    zero = 0

    # Tuple unpacking
    a, b = 1, 2
    first, second, third = "abc"
    x, y, z = [10, 20, 30]

    # Multiple assignment
    value = count = result = 0


# List slicing
def slicing_patterns():
    """List slicing patterns"""
    data = list(range(100))

    # Basic slices
    first_ten = data[0:10]
    last_five = data[-5:]
    middle = data[10:20]

    # Step slicing
    every_other = data[::2]
    reversed_data = data[::-1]

    # Slice with all parameters
    subset = data[5:50:3]

    return first_ten, last_five, middle


# Config-style patterns (for INI/YAML tests)
def config_patterns():
    """Config-like patterns"""
    config = {
        'database': {
            'host': 'localhost',
            'port': 5432,
        },
        'server': {
            'bind': '0.0.0.0',
            'workers': 4,
        },
        'logging': {
            'level': 'INFO',
            'file': 'app.log',
        }
    }
    return config


# Filename patterns in strings
def filename_patterns():
    """Functions with filename-like strings"""
    config_file = "app-config.json"
    data_file = "user_data.csv"
    log_file = "application.log"
    temp_file = "temp-file-123.txt"

    files = [
        "README.md",
        "setup.py",
        "test-data.json",
        "user_profile_2024.csv"
    ]

    return config_file, data_file, log_file, files


# Main execution
if __name__ == "__main__":
    print("Test fixtures loaded successfully")
    print(f"Functions: {len([f for f in dir() if callable(getattr(__builtins__, f, None))])}")
