# tests/test_api.py
"""Test module to check if the obfuscated core import is working."""
import types

import pytest
from pandas import Series

import ittools


def test_succesful_import():
    """Test for correct core import (cheesy)."""
    assert isinstance(ittools.group, types.FunctionType)


# -------------- ittools.depth ------------------
@pytest.mark.parametrize(
    ("arguments", "expected_result"),
    [
        (([[2, 2], [2, [3, 3]], 1], (str,)), 3),
        (([[2, 2], [2, [1, (3, 3)]], 1], (tuple,)), 3),
        (("hallo", (str,)), 0),
    ],
)
def test_depth(arguments, expected_result):
    """Test correct ittools.depth functionaility."""
    assert ittools.depth(*arguments) == expected_result


@pytest.mark.parametrize(
    ("arguments", "expected_result"),
    [
        (([1, 2, 3], 3), [[[1, 2, 3]]]),
        (([1, 2, 3], 3, list), [[[1, 2, 3]]]),
        (([1, 2, 3], 3, tuple), (([1, 2, 3],),)),
    ],
)
def test_nestify(arguments, expected_result):
    """Test correct ittools.nestify functionaility."""
    assert ittools.nestify(*arguments) == expected_result


def test_nestify_fail_on_unhashable():
    """Test ittools.nestify fail on unhashables."""
    try:
        ittools.nestify([1, 2, 3], 3, set)

    except TypeError as terror:
        assert "unhashable" in str(terror)


@pytest.mark.parametrize(
    ("arguments", "expected_result"),
    [
        (("String", list), ["String"]),
        (("String", set), {"String"}),
        (([1, 2, 3], tuple), [1, 2, 3]),
        ((Series([1, 2, 3]), set), {1, 2, 3}),
    ],
)
def test_itrify(arguments, expected_result):
    """Test correct ittools.itrify functionaility."""
    assert ittools.itrify(*arguments) == expected_result


def test_default_itrify():
    """Test correct default ittools.itrify functionaility."""
    assert ittools.itrify("String") == ["String"]


@pytest.mark.parametrize(
    ("argument", "expected_result"),
    [
        ([], True),
        ([[], [1, 2, 3]], False),
    ],
)
def test_is_empty(argument, expected_result):
    """Test correct ittools.is_empty functionaility."""
    assert ittools.is_empty(argument) == expected_result
