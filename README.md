# ripshit and Reg(ex)icide: Escaping Escaping Hell

## Why This Exists

**ripgrep is awesome.** Blazing fast, smart defaults, respects .gitignore - it's everything grep should have been. Built in Rust, it's a perfect example of how modern tools can be orders of magnitude better than their predecessors.

**But I can never remember regex syntax.** And I absolutely loathe escaping things. 

**Globbing is too weak.** `*.py` finds files, but can't find patterns inside them.

**ripshit is my solution:** Take ripgrep's power, add pattern syntax I can actually remember and type quickly. 

### The Core Idea: Aliasing for Regex

ripshit is fundamentally an **aliasing system for regex patterns** - creating shortcuts for the patterns I use constantly:

```bash
# Regex patterns (I can never remember these)
\w+                →  <name>
.*                 →  <>
[a-zA-Z]+          →  <word>
\d+                →  <number>
[a-zA-Z0-9_-]+     →  <filename>
```

**Just like shell aliases** (`ll` for `ls -la`), ripshit creates short, memorable names for common patterns. Plus, `<>` are way easier to type than escaping parentheses and backslashes.

**ripgrep gave us the speed. ripshit gives us syntax that doesn't make me want to scream.**

### The Problem (Real Example)

Find Python functions in a codebase:

```bash
# Usage: find all function definitions with regex
rg "def\s+\w+\s*\([^)]*\)\s*:"

# Usage: find all function definitions with ripshit
ripshit 'def <name>(<>):'
```

**5 seconds vs 2 minutes.** And the ripshit pattern is actually memorable next week.

### What It Does

Converts intuitive patterns into regex so ripgrep can search code:

```bash
# Usage: find all function definitions
ripshit 'def <name>(<>):'

# Usage: find context managers
ripshit 'with <> as <name>:'

# Usage: find specific filenames in imports
ripshit 'import <filename>'
```

**All ripgrep flags work** - add `-B 3 -A 5`, `-n`, `--max-depth 2`, whatever is needed.

## Installation

```bash
# 1. Install ripgrep (required)
brew install ripgrep  # macOS
apt install ripgrep   # Ubuntu/Debian

# 2. Save this script as ~/bin/ripshit
chmod +x ~/bin/ripshit
```
### The Complete Script (17 lines)

```bash
#!/bin/bash

pattern="$1"
shift

# Convert ripshit patterns to regex
pattern="${pattern//<>/.*}"
pattern="${pattern//<name>/\\w+}"
pattern="${pattern//<word>/[a-zA-Z]+}"
pattern="${pattern//<number>/\\d+}"
pattern="${pattern//<filename>/[a-zA-Z0-9_-]+}"

# Escape literal parentheses
pattern="${pattern//(/\\(}"
pattern="${pattern//)/\\)}"

# Call ripgrep
rg "$pattern" "$@"
```

# Recommended:
```bash
alias rip='ripshit' # in ~/.bashrc
```

## Pattern Syntax

Five simple patterns:

- `<>` - matches anything
- `<name>` - matches identifiers (alphanumeric + underscore)
- `<word>` - matches alphabetic only
- `<number>` - matches digits
- `<filename>` - matches filenames (alphanumeric + underscore + hyphen)

**Everything else is literal.** Whitespace, punctuation, keywords - just type what is visible.

### Basic Searches
```bash
# Usage: find class definitions
rip 'class <name>:'

# Usage: find imports
rip 'import <>'

# Usage: find loops
rip 'for <name> in <>:'

# Usage: find conditionals
rip 'if <> and <>:'
```

### With ripgrep Flags

```bash
# Usage: show context (3 lines before, 5 after)
rip 'def <name>(<>):' -B 3 -A 5

# Usage: show line numbers
rip 'class <name>:' -n

# Usage: limit search depth (like the old "look" script)
rip 'import <filename>' --max-depth 2

# Usage: count matches
rip 'def <name>():' -c

# Usage: show only filenames
rip 'TODO' -l
```

### Targeting File Types

```bash
# Usage: search Python files only
rip 'def <name>(<>):' --type py

# Usage: search Jupyter notebooks
rip 'import <>' --type jupyter

# Usage: search MATLAB files
rip 'function <name>' --type matlab

# Usage: search multiple types
rip 'class <name>' --type py --type js
```

### Real-World Examples

```bash
# Usage: find all function definitions with parameters
rip 'def <name>(<>):'

# Usage: find empty functions (no parameters)
rip 'def <name>():'

# Usage: find context managers with specific pattern
rip 'with open(<filename>) as <name>:'

# Usage: find exception handlers
rip 'except <> as <name>:'

# Usage: find config sections in INI files
rip '[<name>]'

# Usage: find YAML keys
rip '<name>: <>'

# Usage: find assignments to numbers
rip '<name> = <number>'
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

# Usage: find lambda functions
rip 'lambda <>:'

# Usage: find decorators
rip '@<name>'

# Usage: find string formatting (f-strings)
rip 'f"<>"'

# Usage: find old-style format strings
rip '".format(<>)'

# Usage: find assertions
rip 'assert <>'

# Usage: find yield statements
rip 'yield <>'

# Usage: find context managers (any pattern)
rip 'with <> as <>:'

# Usage: find try-except blocks
rip 'try:' -A 5

# Usage: find class methods with self
rip 'def <name>(self, <>):'

# Usage: find list slicing
rip '[<>:<>]'

# Usage: find unpacking assignments
rip '<>, <> = <>'
```

## Side-by-Side: ripshit vs Regex

### Function Definitions

```bash
# Usage: find function definitions with regex
rg "def\s+\w+\s*\([^)]*\)\s*:"

# Usage: find function definitions with ripshit
rip 'def <n>(<>):'
```

### Class Inheritance

```bash
# Usage: find class definitions with inheritance using regex
rg "class\s+\w+\s*\([^)]*\)\s*:"

# Usage: find class definitions with inheritance using ripshit
rip 'class <n>(<>):'
```

### Context Managers

```bash
# Usage: find context managers with regex
rg "with\s+.*\s+as\s+\w+\s*:"

# Usage: find context managers with ripshit
rip 'with <> as <name>:'
```

### Import Statements

```bash
# Usage: find import statements with regex
rg "import\s+.*\s+from\s+.*"

# Usage: find import statements with ripshit
rip 'import <> from <>'
```

**Notice a pattern?** ripshit reads like English. Regex reads like line noise.

**Note:** All examples use `<name>` for identifiers. This is the actual pattern - the script uses `<name>`, not `<n>`.

## The Gap It Fills

```
String search          →  Too literal, too many false positives
ripshit               →  ✓ Works for 90% of code searches
Full regex            →  Too complex, wastes mental energy
```

### When to Use Each

**Use ripshit when:**
- Exploring codebases quickly
- Finding common code patterns
- Results are needed NOW, not in 2 minutes
- Readable patterns matter (for scripts that will be reused)

**Use full regex when:**
- Complex lookaheads/lookbehinds required
- Truly unusual patterns
- Regex-specific features are needed

**Use plain search when:**
- Exact literal strings
- Simple word matching

## Origin Story

This started with a simple bash script called `look` for searching flat MATLAB codebases:

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

It worked for literals but failed for patterns. Adding regex meant escaping hell. ripshit bridges that gap.

## AI-Assisted Development

ripshit was built in a single conversation with Claude, demonstrating how AI changes the tooling equation:

**Before AI:**
- Custom tool = hours of dev time
- "Not worth it" for small frictions
- Risk of scope creep

**With AI:**
- Concept → working tool in <1 hour
- Rapid iteration on design
- Economically viable to solve small problems

The barrier to creating personalized tools is now low enough to optimize specific workflows without the traditional time investment.

## Philosophy

**Regex is powerful but hostile.** I need something between "grep a literal string" and "write a regex doctoral thesis."

ripshit gives me:
1. **Readable patterns** - `<n>` not `\w+`
2. **No escaping** - parentheses are just parentheses
3. **Memorable syntax** - I'll remember this next month
4. **90% of regex power** - for 10% of the cognitive load

### When NOT to Use ripshit

**ripshit is NOT always going to work.** If precision or expressiveness is needed in production-grade code, don't use it. 

**Use full regex when:**
- Exact, unambiguous matches are required
- Production code depends on it
- Complex lookaheads/lookbehinds required
- Critical search logic is being written

**But if the goal is to get stuff done faster and grumble less?** This probably might be a use case. ripshit is for exploration, quick searches, and getting answers NOW instead of debugging regex for 10 minutes.

## Limitations and Known Issues

ripshit is a practical hack, not a perfect solution. Here's what doesn't work:

### Pattern Order Matters

Because ripshit does simple string replacement, patterns are processed in a specific order:
1. Literal characters are escaped first: `(`, `)`, `[`, `]`, `{`, `}`
2. Then ripshit patterns are replaced: `<>`, `<name>`, `<word>`, `<number>`, `<filename>`

**This means:** If you literally type `<name>` and want to search for that exact string, ripshit will replace it. There's no escape mechanism for patterns.

### Regex Features Not Supported

ripshit doesn't support advanced regex features:
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

**The philosophy:** ripshit handles 80-90% of common searches. For the other 10-20%, use full regex or refine your pattern.

## Python Module (Optional)

Want to use ripshit patterns in Python scripts? The Python module provides the same pattern syntax programmatically.

### Installation

```bash
cd ~/projects/ripshit
pip install -e .
```

Or copy `ripshit.py` to your project.

### Quick Start

```python
import ripshit as rs

# Basic search - returns raw output string
output = rs.search('def <name>(<>):', '--type', 'py')
print(output)

# Get list of matching lines (non-empty only)
lines = rs.lines('class <name>:')
for line in lines:
    print(line)

# Count matches across all files
count = rs.count('import <>')
print(f"Found {count} import statements")
```

### API Reference

#### Convenience Functions

```python
# Quick one-off searches
rs.search(pattern: str, *args) -> str
rs.lines(pattern: str, *args) -> List[str]
rs.count(pattern: str, *args) -> int
```

All ripgrep arguments work: `'--type', 'py'`, `'-n'`, `'-C', '3'`, etc.

#### Ripshit Class

For reusable searches with default arguments:

```python
# Create searcher with defaults
searcher = rs.Ripshit(default_args=['--type', 'py', '-n'])

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
import ripshit as rs

# Find all function definitions and count them
funcs = rs.lines('def <name>(<>):', '--type', 'py')
print(f"Found {len(funcs)} functions")

# Search with context (3 lines before/after)
context = rs.search('class <name>:', '-C', '3')

# Find all TODO comments
todos = rs.lines('TODO', '--type', 'py')

# Count decorators in a specific directory
decorator_count = rs.count('@<name>', 'src/')

# Create project-specific searcher
py_searcher = rs.Ripshit(default_args=['--type', 'py', '--max-depth', '3'])
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

**ripshit: Because life's too short for regex syntax.**