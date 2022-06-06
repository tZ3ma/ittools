# src/ittools/__init__.py
# flake8: noqa
"""ittools - A colletion of iterable utilites."""
from importlib.metadata import version

from .core import (
    Index2D,
    Stringcrementor,
    depth,
    enum_to_2dix,
    group,
    is_empty,
    itrify,
    nestify,
    zip_split,
)

__version__ = version(__name__)
