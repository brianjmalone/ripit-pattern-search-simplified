"""
ripit - Intuitive pattern search for code
"""
from .ripit import Ripit, search, _check_ripgrep

# Run check on import
_check_ripgrep()

__version__ = "0.1.0"
__all__ = ['Ripit', 'search']