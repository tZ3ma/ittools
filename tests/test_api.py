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
class EndlessIterator:
    """Mock an endless iterator."""

    def __iter__(self):
        """Retun instance of self, when iterated."""
        return self

    def __next__(self):
        """Increase the integer value by one when nexted on."""
        return self


@pytest.mark.parametrize(
    ("arg", "exclude", "expected_result"),
    [
        ([[2, 2], [2, [3, 3]], 1], (str,), 3),
        ([[2, 2], [2, [1, (3, 3)]], 1], (tuple,), 3),
        ("hallo", None, 0),  # default  exclude test
        # ([2, 2], None,  1),  # test infinite loop
        (list, None, 0),  # test infinite type error
        (EndlessIterator(), None, 1),  # test infinite
        ([[[[[]]]]], None, 4),  # test max() value error
    ],
)
def test_depth(arg, exclude, expected_result):
    """Test correct ittools.depth functionaility."""
    assert ittools.depth(arg, exclude) == expected_result


# -------------- ittools.nestify ------------------
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


# -------------- ittools.itrify ------------------
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


# -------------- ittools.is_empty ------------------
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


# -------------- ittools.Stringcrementor ------------------
def test_stringcrmentor_next():
    """Test correct ittools.Stringcrementor __next__ functionaility."""
    strementor = ittools.Stringcrementor("Number")
    strementor_results = []
    expected_result = [
        "Number0",
        "Number1",
        "Number2",
    ]
    for _i in range(3):
        strementor_results.append(next(strementor))

    assert strementor_results == expected_result


def test_stringcrmentor_iter():
    """Test correct ittools.Stringcrementor __iter__ functionaility."""
    assert isinstance(
        iter(ittools.Stringcrementor()),
        ittools.Stringcrementor,
    )


# -------------- ittools.enum_to_2dix ------------------
@pytest.mark.parametrize(
    ("number", "shape", "expected_result"),
    [
        (0, (3, 2), (0, 0)),
        (1, (3, 2), (0, 1)),
        (2, (3, 2), (1, 0)),
        (3, (3, 2), (1, 1)),
        (4, (3, 2), (2, 0)),
        (5, (3, 2), (2, 1)),
        # change gears to rows dont matter
        (0, (1, 6), (0, 0)),
        (1, (1, 6), (0, 1)),
        (2, (1, 6), (0, 2)),
        (3, (1, 6), (0, 3)),
        (4, (1, 6), (0, 4)),
        (5, (1, 6), (0, 5)),
        (6, (1, 6), (1, 0)),
        (7, (1, 6), (1, 1)),
        # change gears to nonsensically use negatives
        (0, (2, 2), (0, 0)),
        (-1, (2, 2), (-1, 1)),
        (-2, (2, 2), (-1, 0)),
    ],
)
def test_enum_to_2dix(number, shape, expected_result):
    """Test correct ittools.enum_to_2dix functionaility."""
    assert ittools.enum_to_2dix(number, shape) == expected_result


# -------------- ittools.Index2D ------------------
@pytest.mark.parametrize(
    ("number", "shape", "expected_result"),
    [
        (0, (3, 2), (0, 0)),
        (1, (3, 2), (0, 1)),
        (2, (3, 2), (1, 0)),
        (3, (3, 2), (1, 1)),
        (5, (3, 2), (2, 1)),
        # change gears to rows dont matter
        (0, (1, 6), (0, 0)),
        (1, (1, 6), (0, 1)),
        (2, (1, 6), (0, 2)),
        (3, (1, 6), (0, 3)),
        (4, (1, 6), (0, 4)),
        (5, (1, 6), (0, 5)),
        (7, (1, 6), (1, 1)),
        # change gears to nonsensically use negatives
        (0, (2, 2), (0, 0)),
        (-2, (2, 2), (-1, 0)),
    ],
)
def test_index2d(number, shape, expected_result):
    """Test correct ittools.Index2D functionaility."""
    idx2d = ittools.Index2D(shape)
    assert idx2d(number) == expected_result


# -------------- ittools.zip_split ------------------
def test_zip_split():
    """Test correct ittools.zip_split functionaility."""
    result = [["hi", "hi", "hi", "hi"], ["hi", "hi", "hi"], ["hi", "hi", "hi"]]
    assert list(ittools.zip_split(10 * ["hi"], 3)) == result


# -------------- ittools.group ------------------
def test_group():
    """Test correct ittools.group functionaility."""
    result = [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, None, None)]
    assert list(ittools.group(range(10), chunks=3)) == result
