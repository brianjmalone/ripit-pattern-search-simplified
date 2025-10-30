#!/usr/bin/env python3
"""
Comprehensive test suite for ripit.
Tests both the bash script and Python module against test_fixtures.py.
"""
import subprocess
import sys
import os
from pathlib import Path

# Add project directory to path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

import ripit as rs


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


class TestRunner:
    """Test runner for ripit patterns"""

    def __init__(self, bash_script_path, fixtures_path):
        self.bash_script = bash_script_path
        self.fixtures = fixtures_path
        self.passed = 0
        self.failed = 0
        self.tests_run = 0

    def run_bash(self, pattern: str) -> str:
        """Run bash script version of ripit"""
        try:
            result = subprocess.run(
                [self.bash_script, pattern, str(self.fixtures)],
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout
        except Exception as e:
            return f"ERROR: {e}"

    def run_python(self, pattern: str) -> str:
        """Run Python module version of ripit"""
        try:
            return rs.search(pattern, str(self.fixtures))
        except Exception as e:
            return f"ERROR: {e}"

    def test_pattern(self, name: str, pattern: str, expected_in_output: list,
                     should_match_count: int = None):
        """
        Test a ripit pattern against fixtures.

        Args:
            name: Test name
            pattern: ripit pattern to test
            expected_in_output: List of strings that should appear in output
            should_match_count: Minimum number of matches expected (optional)
        """
        self.tests_run += 1
        print(f"\n{Colors.BLUE}{Colors.BOLD}Test {self.tests_run}: {name}{Colors.END}")
        print(f"  Pattern: {Colors.YELLOW}{pattern}{Colors.END}")

        # Run bash version
        bash_output = self.run_bash(pattern)
        bash_matches = len(bash_output.splitlines()) if bash_output else 0

        # Run Python version
        python_output = self.run_python(pattern)
        python_matches = len(python_output.splitlines()) if python_output else 0

        # Check outputs match
        outputs_match = bash_output == python_output

        # Check expected strings are in output
        all_found = all(exp in bash_output for exp in expected_in_output)

        # Check match count if specified
        count_ok = True
        if should_match_count is not None:
            count_ok = bash_matches >= should_match_count

        # Determine pass/fail
        passed = outputs_match and all_found and count_ok

        if passed:
            self.passed += 1
            print(f"  {Colors.GREEN}✓ PASSED{Colors.END}")
            print(f"    Matches: {bash_matches}")
        else:
            self.failed += 1
            print(f"  {Colors.RED}✗ FAILED{Colors.END}")
            if not outputs_match:
                print(f"    {Colors.RED}Bash and Python outputs differ{Colors.END}")
                print(f"    Bash matches: {bash_matches}")
                print(f"    Python matches: {python_matches}")
            if not all_found:
                missing = [exp for exp in expected_in_output if exp not in bash_output]
                print(f"    {Colors.RED}Expected strings not found: {missing}{Colors.END}")
            if not count_ok:
                print(f"    {Colors.RED}Expected at least {should_match_count} matches, got {bash_matches}{Colors.END}")

        return passed

    def summary(self):
        """Print test summary"""
        print(f"\n{'=' * 60}")
        print(f"{Colors.BOLD}Test Summary{Colors.END}")
        print(f"{'=' * 60}")
        print(f"Total tests: {self.tests_run}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.END}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.END}")

        if self.failed == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}All tests passed!{Colors.END}")
            return 0
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}Some tests failed.{Colors.END}")
            return 1


def main():
    """Run all ripit tests"""
    # Paths
    home = Path.home()
    bash_script = home / "bin" / "ripit"
    fixtures = Path(__file__).parent / "test_fixtures.py"

    # Check prerequisites
    if not bash_script.exists():
        print(f"{Colors.RED}ERROR: Bash script not found at {bash_script}{Colors.END}")
        return 1

    if not fixtures.exists():
        print(f"{Colors.RED}ERROR: Test fixtures not found at {fixtures}{Colors.END}")
        return 1

    print(f"{Colors.BOLD}ripit Test Suite{Colors.END}")
    print(f"Bash script: {bash_script}")
    print(f"Fixtures: {fixtures}")
    print(f"{'=' * 60}")

    runner = TestRunner(bash_script, fixtures)

    # Test 1: Basic <> pattern
    runner.test_pattern(
        "Match anything with <>",
        "import <>",
        ["import os", "import json", "import sys"],
        should_match_count=5
    )

    # Test 2: <name> pattern - identifiers
    runner.test_pattern(
        "Match identifiers with <name>",
        "def <name>():",
        ["def simple_function():", "def custom_context():"],
        should_match_count=2
    )

    # Test 3: Function definitions with parameters
    runner.test_pattern(
        "Function definitions with params",
        "def <name>(<>):",
        ["def function_with_params", "def __init__"],
        should_match_count=10
    )

    # Test 4: Class definitions
    runner.test_pattern(
        "Simple class definitions",
        "class <name>:",
        ["class SimpleClass:", "class DataProcessor:"],
        should_match_count=2
    )

    # Test 5: Class with inheritance
    runner.test_pattern(
        "Class with inheritance",
        "class <name>(<>):",
        ["class InheritedClass(SimpleClass):", "class MultipleInheritance"],
        should_match_count=2
    )

    # Test 6: Context managers
    runner.test_pattern(
        "Context managers with as",
        "with <> as <name>:",
        ["with open", "with custom_context"],
        should_match_count=3
    )

    # Test 7: List comprehensions
    runner.test_pattern(
        "List comprehensions",
        "[<> for <>]",
        ["squares = [x * x for x in range(10)]", "[i * j for j in range(3)]"],
        should_match_count=5
    )

    # Test 8: Dict comprehensions
    runner.test_pattern(
        "Dictionary comprehensions",
        "{<>: <> for <>}",
        ["squares_dict = {x: x * x", "even_squares = {n: n ** 2"],
        should_match_count=3
    )

    # Test 9: Set comprehensions
    runner.test_pattern(
        "Set comprehensions",
        "{<> for <>}",
        ["unique_lens = {len(word)", "odd_squares = {x ** 2"],
        should_match_count=2
    )

    # Test 10: Generator expressions
    runner.test_pattern(
        "Generator expressions",
        "(<> for <>)",
        ["squares_gen = (x * x for x", "even_gen = (n for n"],
        should_match_count=3
    )

    # Test 11: Lambda functions
    runner.test_pattern(
        "Lambda functions",
        "lambda <>:",
        ["add = lambda x, y:", "square = lambda x:"],
        should_match_count=5
    )

    # Test 12: Decorators
    runner.test_pattern(
        "Decorators",
        "@<name>",
        ["@dataclass", "@classmethod", "@staticmethod", "@contextmanager"],
        should_match_count=4
    )

    # Test 13: F-strings
    runner.test_pattern(
        "F-strings",
        'f"<>"',
        ['greeting = f"Hello, {name}!"', 'result = f"The answer is'],
        should_match_count=4
    )

    # Test 14: Old-style format
    runner.test_pattern(
        "String format method",
        '".format(<>)',
        ['"Value: {}".format(count)', 'format(name=name, count=count)'],
        should_match_count=2
    )

    # Test 15: Exception handling
    runner.test_pattern(
        "Exception handling",
        "except <> as <name>:",
        ["except ZeroDivisionError as e:", "except (ValueError, TypeError) as err:"],
        should_match_count=3
    )

    # Test 16: Assert statements
    runner.test_pattern(
        "Assert statements",
        "assert <>",
        ["assert value > 0", "assert value < 100"],
        should_match_count=2
    )

    # Test 17: Yield statements
    runner.test_pattern(
        "Yield statements",
        "yield <>",
        ["yield i", "yield a"],
        should_match_count=2
    )

    # Test 18: Methods with self
    runner.test_pattern(
        "Methods with self parameter",
        "def <name>(self, <>):",
        ["def __init__(self, name):", "def process(self, items):"],
        should_match_count=3
    )

    # Test 19: Tuple unpacking
    runner.test_pattern(
        "Tuple unpacking assignment",
        "<>, <> = <>",
        ["a, b = 1, 2", "a, b = b, a + b"],
        should_match_count=2
    )

    # Test 20: List slicing
    runner.test_pattern(
        "List slicing",
        "[<>:<>]",
        ["data[0:10]", "data[10:20]", "data[5:50:3]"],
        should_match_count=3
    )

    # Test 21: <num> pattern - digits
    runner.test_pattern(
        "Number assignments",
        "<name> = <num>",
        ["x = 42", "count = 100", "zero = 0", "answer = 42"],
        should_match_count=4
    )

    # Test 22: <name> pattern for imports
    runner.test_pattern(
        "Import identifiers",
        'import <name>',
        ["import os", "import json", "import sys", "import math"],
        should_match_count=4
    )

    # Test 25: For loops (with colons, not comprehensions)
    runner.test_pattern(
        "For loops with colons",
        "for <name> in <>:",
        ["for i in range"],
        should_match_count=1
    )

    # Test 26: Try-except blocks
    runner.test_pattern(
        "Try-except blocks",
        "try:",
        ["try:", "try:"],
        should_match_count=3
    )

    # Test 27: From imports
    runner.test_pattern(
        "From imports",
        "from <> import <>",
        ["from os import path", "from collections import defaultdict"],
        should_match_count=4
    )

    # Test 28: Class methods
    runner.test_pattern(
        "Class methods",
        "def <name>(cls, <>):",
        ["def from_file(cls, filename):"],
        should_match_count=1
    )

    # Test 29: Static methods
    runner.test_pattern(
        "Static methods",
        "def <name>(data):",
        ["def validate(data):"],
        should_match_count=1
    )

    # Test 30: Multiple inheritance
    runner.test_pattern(
        "Multiple inheritance",
        "class <name>(<>, <>):",
        ["class MultipleInheritance(SimpleClass, dict):"],
        should_match_count=1
    )

    # Print summary
    return runner.summary()


if __name__ == "__main__":
    sys.exit(main())
