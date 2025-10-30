#!/usr/bin/env python3
"""
ripit - Intuitive pattern search wrapper for ripgrep
Provides simple pattern syntax that compiles to regex for code searching.
"""
import subprocess
import sys
import shutil
from typing import List, Optional


def _check_ripgrep():
    """Check if ripgrep is installed"""
    if not shutil.which('rg'):
        raise ImportError(
            "ripgrep (rg) not found. Install it first:\n"
            "  macOS: brew install ripgrep\n"
            "  Ubuntu/Debian: apt install ripgrep\n"
            "  Fedora: dnf install ripgrep\n"
            "  Windows: choco install ripgrep\n"
            "  Or visit: https://github.com/BurntSushi/ripgrep#installation"
        )


class Ripit:
    """Main ripit search interface"""

    def __init__(self, default_args: Optional[List[str]] = None):
        """
        Initialize Ripit searcher.

        Args:
            default_args: Default arguments to pass to ripgrep (e.g., ['--type', 'py'])
        """
        _check_ripgrep()
        self.default_args = default_args or []

    def _convert_pattern(self, pattern: str) -> str:
        """
        Convert ripit patterns to regex.

        Patterns:
            <> - matches anything (.*)
            <name> - matches identifiers (\\w+)
            <num> - matches digits (\\d+)
        """
        # Escape literal characters FIRST (before pattern substitution)
        # Escape literal parentheses
        pattern = pattern.replace('(', r'\(')
        pattern = pattern.replace(')', r'\)')

        # Escape literal brackets
        pattern = pattern.replace('[', r'\[')
        pattern = pattern.replace(']', r'\]')

        # Escape literal curly braces
        pattern = pattern.replace('{', r'\{')
        pattern = pattern.replace('}', r'\}')

        # Convert ripit patterns to regex AFTER escaping
        pattern = pattern.replace('<>', '.*')
        pattern = pattern.replace('<name>', r'\w+')
        pattern = pattern.replace('<num>', r'\d+')

        return pattern

    def search(self, pattern: str, *args) -> str:
        """
        Search for pattern and return raw output.

        Args:
            pattern: ripit pattern to search for
            *args: additional arguments to pass to ripgrep

        Returns:
            Raw output from ripgrep
        """
        regex_pattern = self._convert_pattern(pattern)
        cmd = ['rg', regex_pattern] + self.default_args + list(args)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout
        except FileNotFoundError:
            raise ImportError("ripgrep (rg) not found in PATH")

    def lines(self, pattern: str, *args) -> List[str]:
        """
        Search for pattern and return list of matching lines.

        Args:
            pattern: ripit pattern to search for
            *args: additional arguments to pass to ripgrep

        Returns:
            List of matching lines
        """
        output = self.search(pattern, *args)
        return [line for line in output.splitlines() if line.strip()]

    def count(self, pattern: str, *args) -> int:
        """
        Count matches for pattern.

        Args:
            pattern: ripit pattern to search for
            *args: additional arguments to pass to ripgrep

        Returns:
            Number of matching lines
        """
        output = self.search(pattern, '-c', *args)
        # Sum up counts from all files
        total = 0
        for line in output.splitlines():
            if ':' in line:
                # Format is "filename:count"
                count_str = line.split(':')[-1]
                try:
                    total += int(count_str)
                except ValueError:
                    pass
        return total


# Convenience functions for quick usage
def search(pattern: str, *args) -> str:
    """Quick search function"""
    return Ripit().search(pattern, *args)


def lines(pattern: str, *args) -> List[str]:
    """Quick lines function"""
    return Ripit().lines(pattern, *args)


def count(pattern: str, *args) -> int:
    """Quick count function"""
    return Ripit().count(pattern, *args)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: ripit <pattern> [ripgrep args...]", file=sys.stderr)
        sys.exit(1)

    pattern = sys.argv[1]
    args = sys.argv[2:]

    output = search(pattern, *args)
    print(output, end='')

