# R\\.I\\.P\\. regex: Escaping Escaping Hell

(Irony: I had to escape \\ in Markdown for the title)

## What "ripit" Does

Converts intuitive patterns into regex so ripgrep can search code. 

## Why This Exists

**ripgrep is awesome.** 

Blazing fast, smart defaults, respects .gitignore, etc. Rust tools are great.

**But I often have to look up regex syntax.** 

I particularly loathe writing tricky escaping syntax when I am searching for special characters. 

**ripit is my workaday solution.** 

Much of ripgrep's power, much less regex-ery.

### The Core Idea: Aliasing for Regex

ripit is fundamentally an **aliasing system for regex patterns** - creating shortcuts for limited patterns I often need:

```bash
# Regex ..............ripit
.*                 →  <>
\w+                →  <name>
\d+                →  <num>

Three simple patterns:

- `<>` - matches anything
- `<name>` - matches identifiers (letters, digits, underscores)
- `<num>` - matches numbers (digits only)
```

**Everything else is literal.** Whitespace, punctuation, keywords - just type what is visible.

**Just like shell aliases** (`ll` for `ls -la`), ripit creates short, memorable names for common patterns. Plus, `<>`'s are way easier to type than escaping parentheses and backslashes. 

In ripit syntax, "<>" typically means "anything I don't want to match on".  You don't need to bend over backwards to escape literals, since you "escape" everything else, and type literals freely.

## Essential Lesson: AI-Assistants = Personalized Tooling

ripit was built in a single conversation with Claude.

**Before AI:**
- Custom tool = hours of dev time
- "Not worth it" for small frictions
- Risk of scope creep

**With AI:**
- Concept → working tool in <1 hour
- Rapid iteration on design
- Avoid idiosyncratic pain points

At the end of this document, I show how to create a Python module if you want access to ripit there. 

### The Problem: Escaping Escaping

Here's ripit vs regex side-by-side (I aliased it to 'rip' for convenience): 

**Function Definitions**
```bash
# Regex
rg "def\s+\w+\s*\([^)]*\)\s*:"

# ripit
rip 'def <name>(<>):'
```

**Class definitions**
```bash
# Regex
rg "class\s+\w+\s*\([^)]*\)\s*:"

# ripit
rip 'class <name>(<>):'
```

**Import Statements**
```bash
# Regex
rg "import\s+.*\s+from\s+.*"

# ripit
rip 'import <> from <>'
```

It's basically globbing, but with <> instead of *. 

Often, you can get away with "rg import" but this provides a bit more safety for a few keystrokes. 

```bash
# Usage: find context managers
ripit 'with <> as <name>:'

# Usage: find specific module imports
ripit 'import <name>'
```
**All ripgrep flags work** - add `-B 3 -A 5`, `-n`, `--max-depth 2`, so it remains pretty expressive. 

## Installation

```bash
# 1. Install ripgrep (required)
brew install ripgrep  # macOS
apt install ripgrep   # Ubuntu/Debian

# 2. Save this script as ~/bin/ripit
chmod +x ~/bin/ripit
```
### Bash Script

```bash
#!/bin/bash

pattern="$1"
shift

# Convert ripit patterns to regex
pattern="${pattern//<>/.*}"
pattern="${pattern//<name>/\\w+}"
pattern="${pattern//<num>/\\d+}"

# Escape literal parentheses
pattern="${pattern//(/\\(}"
pattern="${pattern//)/\\)}"

# Call ripgrep
rg "$pattern" "$@"
```

### Recommended for Keystroke Golfers:
```bash
alias rip='ripit' # in ~/.bashrc
```

### Basic Search Examples:
```bash
# Usage: find class definitions
rip 'class <name>:'

# Usage: find loops
rip 'for <name> in <>:'

# Usage: find joint conditionals
rip 'if <> and <>:'
```
#### ....with ripgrep Flags

```bash
# Usage: show context (3 lines before, 5 after)
rip 'def <name>(<>):' -B 3 -A 5

# Usage: show line numbers
rip 'class <name>:' -n

# Usage: limit search depth (like "look" alias)
rip 'import <name>' --max-depth 2

# Usage: count matches
rip 'def <name>():' -c

# Usage: show only filenames
rip 'TODO' -l

# Usage: search Python files only
rip 'def <name>(<>):' --type py

# Usage: search Jupyter notebooks
rip 'import <>' --type jupyter

# Usage: search MATLAB files
rip 'function <name>' --type matlab

# Usage: search multiple types
rip 'class <name>' --type py --type js
```

### Finding specific Python idioms 

```bash
# Usage: find list comprehensions
rip '[<> for <>]'

# Usage: find generator expressions
rip '(<> for <>)'

# Usage: find dictionary comprehensions
rip '{<>: <> for <>}'

# Usage: find set comprehensions
rip '{<> for <>}'

# Usage: find decorators
rip '@<name>'

# Usage: find string formatting (f-strings)
rip 'f"<>"'

# Usage: find old-style format strings
rip '".format(<>)'

# Usage: find class methods with self and other parameters
rip 'def <name>(self, <>):'

# Usage: find list slicing
rip '[<>:<>]'

# Usage: find unpacking assignments
rip '<>, <> = <>'
```

### When to Use Each

**Use full regex when:**
- Complex lookaheads/lookbehinds required
- Truly unusual patterns
- Regex-specific features are needed

**Use ripit when:**
- Exploring codebases quickly
- Finding common code patterns
- Readable patterns matter (for scripts that will be reused)

**Use plain search when:**
- Exact literal strings
- Simple word matching

## Origin Story

This project started with a simple bash script called `look` for shallow searches of codebases:

```bash
#!/bin/bash
# The original "look" script

# Check if an argument is provided
if [ $# -eq 0 ]; then
  echo "Error: Please provide a search string as an argument."
  exit 1
fi

# Define the search string
search_string="$1"

# Find files and search for the string
find . -maxdepth 1 -type f -exec grep -Hi "$search_string" {} \;

# aliased to "look" in ~/.bashrc
# alias look="~/bin/search.sh"
```

I still use that all the time, but it's inflexible. ripit is an extension of look. 

Yes, I should be using fd. I know. It's an old alias!

## Limitations and Known Issues

ripit is a practical hack, not a perfect solution. Here's what doesn't work:

### Pattern Order Matters

Because ripit does simple string replacement, patterns are processed in a specific order:
1. Literal characters are escaped first: `(`, `)`, `[`, `]`, `{`, `}`
2. Then ripit patterns are replaced: `<>`, `<name>`, `<num>`

**This means:** If you literally type `<name>` and want to search for that exact string, ripit will replace it. There's no escape mechanism for patterns.

### Regex Features Not Supported

ripit doesn't support advanced regex features:
- No lookaheads/lookbehinds
- No backreferences
- No optional groups (`?`, `+`, `*` on groups)
- No alternation (`|`)

**When you need these:** Use ripgrep directly with full regex.

### Edge Cases

Some patterns might not work as expected:
- Nested comprehensions can be tricky
- Complex multi-line patterns may fail
- Patterns with unusual whitespace might not match

**The philosophy:** ripit handles 80-90% of common searches. For the other 10-20%, use full regex or refine your pattern.

## Python Module (Optional)

Want to use ripit patterns in Python scripts? The Python module provides the same pattern syntax programmatically.

### Installation

```bash
cd ~/projects/ripit
pip install -e .
```

Or copy `ripit.py` to your project.

### Quick Start

```python
import ripit as rip

# Basic search - returns raw output string
output = rip.search('def <name>(<>):', '--type', 'py')
print(output)

# Get list of matching lines (non-empty only)
lines = rip.lines('class <name>:')
for line in lines:
    print(line)

# Count matches across all files
count = rip.count('import <>')
print(f"Found {count} import statements")
```

### API Reference

#### Convenience Functions

```python
# Quick one-off searches
rip.search(pattern: str, *args) -> str
rip.lines(pattern: str, *args) -> List[str]
rip.count(pattern: str, *args) -> int
```

All ripgrep arguments work: `'--type', 'py'`, `'-n'`, `'-C', '3'`, etc.

#### Ripit Class

For reusable searches with default arguments:

```python
# Create searcher with defaults
searcher = rip.Ripit(default_args=['--type', 'py', '-n'])

# All methods apply default args automatically
lines = searcher.lines('def <name>():')
count = searcher.count('@<name>')
output = searcher.search('class <name>(<>):')
```

**Methods:**
- `search(pattern, *args)` - Returns raw ripgrep output as string
- `lines(pattern, *args)` - Returns list of non-empty matching lines
- `count(pattern, *args)` - Returns total match count across files

### Python Examples

```python
import ripit as rip

# Find all function definitions and count them
funcs = rip.lines('def <name>(<>):', '--type', 'py')
print(f"Found {len(funcs)} functions")

# Search with context (3 lines before/after)
context = rip.search('class <name>:', '-C', '3')

# Find all TODO comments
todos = rip.lines('TODO', '--type', 'py')

# Count decorators in a specific directory
decorator_count = rip.count('@<name>', 'src/')

# Create project-specific searcher
py_searcher = rip.Ripit(default_args=['--type', 'py', '--max-depth', '3'])
imports = py_searcher.lines('from <> import <>')
classes = py_searcher.lines('class <name>:')
```

### When to Use Python Module vs CLI

**Use CLI when:**
- Interactive exploration of codebases
- One-off searches
- Quick answers needed NOW

**Use Python module when:**
- Building code analysis tools
- Automating searches in scripts
- Need programmatic access to results
- Integrating with other Python tools

---

**ripit: Because life's too short for regex syntax.**
