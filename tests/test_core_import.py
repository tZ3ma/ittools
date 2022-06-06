# tests/test_core_import.py
"""Test module to check if the obfuscated core import is working."""
import types

import ittools


def test_succesful_import():
    """Test for correct core import (cheesy)."""
    assert isinstance(ittools.group, types.FunctionType)
