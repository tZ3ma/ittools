"""A colletion of iterable utilites.

Used to grow on the fly. Aims to provide general purpose abstract
functionalities.

.. autosummary::
   :nosignatures:

   depth
   nestify
   itrify
   is_empty
   Stringcrementor
   enum_to_2dix
   Index2D
   zip_split
   group
"""

import collections
import logging
import math
from itertools import zip_longest

from pandas import Series

logger = logging.getLogger(__name__)


def depth(arg, exclude=None):  # noqa: C901
    r"""Powerfull function to determine depth of iterable.

    Credit goes to:
    https://stackoverflow.com/a/35698158

    Parameters
    ----------
    arg : ~collections.abc.Iterable
        Iterable of which nested depth is to be determined

    exclude : ~collections.abc.Iterable, default=None
        Iterable of iterable types that should be ignored.
        If None, str are excluded.

    Returns
    -------
    int
        Depth of :paramref:`depth.arg`

    Example
    -------
    >>> depth([[2, 2], [2, [3, 3]], 1])
    3

    Using exclude to ignore tuples:

    >>> depth([[2, 2], [2, (3, 3)], 1], exclude=(tuple,))
    2
    """
    # complexity > 12; tolerable here
    if exclude is None:
        exclude = (str,)

    if isinstance(arg, tuple(exclude)):
        return 0

    try:
        if next(iter(arg)) is arg:  # avoid infinite loops
            return 1
    except TypeError:
        return 0

    try:  # pragma: no cover
        # coverage is excluded here, cause this part definetly gets
        # executed and tested. I might be overlooking something,
        # or pytest has coverage issues with rersive functions
        depths_in = map(lambda x: depth(x, exclude), arg.values())
    except AttributeError:
        try:
            print("there")
            depths_in = map(lambda x: depth(x, exclude), arg)

        except TypeError:  # pragma: no cover
            # print("Could not provoke this Error!")
            return 0

    try:
        depth_in = max(depths_in)
    except ValueError:
        depth_in = 0

    return 1 + depth_in


def nestify(obj, target_depth, container=list):
    """Return a nested container of obj of target depth.

    Parameters
    ----------
    obj
        obj which is to be put in a container

    target_depth : ~numbers.Number
        Keep nesting object until nesting depth >= target_depth

    container : ~typing.Container
        Container (list, tuple, ...)  the :paramref:`nestify.obj` is nested
        with.

    Returns
    -------
    ~typing.Container
        Nested container object with the depth of
        :paramref:`nestify.target_depth`

    Examples
    --------
    Standard use case:

    >>> nestify([1, 2, 3], 3)
    [[[1, 2, 3]]]


    Specifying the container to nest with:

    >>> nestify([1, 2, 3], 3, tuple)
    (([1, 2, 3],),)


    Not all containers work with all objects especially when working with sets,
    since sets itself are not hashable they can not be nested.

    >>> nestify([1, 2, 3], 3, set)
    Traceback (most recent call last):
      File "/usr/lib/python3.6/doctest.py", line 1330, in __run
        compileflags, 1), test.globs)
      File "<doctest ittools.nestify[2]>", line 1, in <module>
        nestify([1, 2, 3], 3, set)
      File "/home/tze/Code/ittools/ittools.py", line 118, in nestify
        obj = container([obj])
    TypeError: unhashable type: 'list'


    Frozensets however can be nested:

    >>> nestify(frozenset([1, 2, 2]), 3, frozenset)
    frozenset({frozenset({frozenset({1, 2})})})

    """
    while (
        depth(
            obj,
            exclude=(
                str,
                Series,
            ),
        )
        < target_depth
    ):
        obj = container([obj])
    return obj


def itrify(obj, container=list):
    """Turn object into an iterable container if not already.

    Strings will be itrified without splitting!

    Only objects that are of type ``str`` or **not** of
    :class:`collections.abc.Sequence` will be itrified.

    Parameters
    ----------
    obj
        Anything not a :class:`~collections.abc.Sequence` (except for str) will
        be containered as iterable.

    container : ~typing.Container, default=list
        Interable container designed to house :paramref:`itrify.obj`.


    Returns
    -------
    ~collections.abc.Container
        containered :paramref:`~itrify.obj`. ( i.e. ``list(obj)``)

    Examples
    --------
    Pretty much the same as ``list(('String',))``:

    >>> itrify('String')
    ['String']


    A list is already iterable so this is futile:

    >>> itrify([1, 2, 3], tuple)
    [1, 2, 3]


    Strings although iterable will be itrified as whole:

    >>> itrify('String', tuple)
    ('String',)


    The :paramref:`itrify.container` of course, can be any callable
    container type:

    >>> itrify('String', set)
    {'String'}


    Pandas is awesome they support out of the box data type transformation:

    >>> import pandas as pd
    >>> itrify(pd.Series([1,2,3]), set)
    {1, 2, 3}

    """
    if isinstance(obj, str):
        return container([obj])
    if not isinstance(obj, collections.abc.Sequence):
        return container(obj)
    return obj


def is_empty(lst):
    """Check if list ist empty.

    ``True`` if :paramref:`~is_empty.lst` is an empty :class:`~typing.List`. ``False``
    otherwise. Works based on ``bool([]) == True``.

    Parameters
    ----------
    lst: list
        List to be checked for emptiness.

    Returns
    -------
    bool
        ``True`` if :paramref:`~is_empty.lst` is an empty :class:`~typing.List`. ``False``
        otherwise.

    Examples
    --------
    >>> is_empty([])
    True

    >>> is_empty([[], [1,2,3]])
    False

    >>> is_empty([[[[]]]])
    True

    Tuple is not a list (u dont say):

    >>> is_empty(([], []))
    False
    """
    # is lst a list ?
    if isinstance(lst, list):
        # ... yes! check if all elements are empty
        return all(map(is_empty, lst))
    # ...  no! Not a list
    return False


class Stringcrementor:
    """
    Iterator of String + incremented Integer = Stringcrementor.

    Returns string + integer of which the integer is incremented
    by one each time next() is called on the Stringcrementor object.

    Parameters
    ----------
    string: str
        String/tag/label of what you want to be incremented i.e "Category".
        Default: ``Stringcrementor``
    start: ~numbers.Number
        Starting number which is to be incremented. Default: 0

    Returns
    -------
    str
        string + integer of which the integer is incremented.

    Example
    -------
    >>> strementor = Stringcrementor('The Answer is: ')

    >>> for i in range(42):
    ...     pass # just kidding

    >>> for i in range(3):
    ...     print(next(strementor))
    The Answer is: 0
    The Answer is: 1
    The Answer is: 2
    """

    def __init__(self, string="Stringcrementor ", start=0):
        self.value = start
        self.string = string

    def __iter__(self):
        """Retun instance of self, when iterated."""
        return self

    def __next__(self):
        """Increase the integer value by one when nexted on."""
        next_value = self.value
        self.value += 1
        return self.string + str(next_value)


def enum_to_2dix(number, shape):
    """Map a 1d range to a 2d index.

    Parameters
    ----------
    number : int
        Number to be mapped to a 2D index. Usually used with in some form of
        iteration.

    shape : tuple
        2 dimensional tuple defining an arrays 2d shape as in ``(rows, columns)``.

    Returns
    -------
    tuple
        the 1d enumerate numberition mapped to a (row, column) 2d tuple

    Note
    ----
    Only the number of columns is actually used. Since this is designed to
    be used with 2D-Matrices however, it is left as 2D-shape for convenience.

    This implies however, that you can actually use infinite
    :paramref:`~enum_to_2dix.number` arguments altough your
    :paramref:`~enum_to_2dix.shape` might imply only 3 rows.

    Examples
    --------
    Mapping ``range(6)`` to a 3,2 dimenstion array:

    >>> for i in range(6):
    ...     print(i, '->', enum_to_2dix(i, (3,2)))
    0 -> (0, 0)
    1 -> (0, 1)
    2 -> (1, 0)
    3 -> (1, 1)
    4 -> (2, 0)
    5 -> (2, 1)

    Mapping ``range(12)`` to a 3,4 dimenstion array:

    >>> for i in range(12):
    ...     print(i, '->', enum_to_2dix(i, (3,4)))
    0 -> (0, 0)
    1 -> (0, 1)
    2 -> (0, 2)
    3 -> (0, 3)
    4 -> (1, 0)
    5 -> (1, 1)
    6 -> (1, 2)
    7 -> (1, 3)
    8 -> (2, 0)
    9 -> (2, 1)
    10 -> (2, 2)
    11 -> (2, 3)
    """
    column = shape[1]
    return (math.floor(number / column), number % column)


class Index2D:
    """Construct a callable object that maps a number to a 2d index.

    Parameters
    ----------
    shape : 2-tuple
        tuple defining an array's 2d shape as in ``(rows, columns)``

    Returns
    -------
    tuple
        the 1d enumerate position mapped to a (row, column) 2d tuple

    Examples
    --------
    >>> idx2d = Index2D((3, 2))
    >>> for i in range(6):
    ...     print(i, '->', idx2d(i))
    ...
    0 -> (0, 0)
    1 -> (0, 1)
    2 -> (1, 0)
    3 -> (1, 1)
    4 -> (2, 0)
    5 -> (2, 1)
    """

    @property
    def shape(self):
        """Tuple representing the shape of the Index2D object."""
        return self._shape

    def __init__(self, shape):
        self._shape = shape

    def __call__(self, number):
        """Make the :class:`~ittools.Index2D` objects callable.

        Parameters
        ----------
        number : ~numbers.Number
            The 1 d index/number to be mapped to a 2d index.

        Returns
        -------
        tuple
            the 1d enumerate position mapped to a (row, column) 2d tuple

        """
        return enum_to_2dix(number, self.shape)


def zip_split(sequence, chunks):
    r"""Split sequence into chunks returning a zipped-like order of elements.

    The last :math:`n` chunks will be one item short of the rest, if the
    number of items in :paramref:`~zip_split.sequence` is not an integer
    multiple of :paramref:`~zip_split.chunks`. With :math:`n` beeing:

    :math:`n = \text{len}\left(\text{sequence}\right)-
    \left[\text{len}\left(\text{sequence}\right) \% \text{chunks}\right]`.

    Note
    ----
    Credit to https://www.garyrobinson.net/2008/04/splitting-a-pyt.html
    (Garry Robinson)

    Parameters
    ----------
    sequence: ~collections.abc.Sequence
        The sequence to split into chunks.
    chunks: int
        The number of splitted sequences created.

    Yields
    ------
    :class:`~collections.abc.Generator`
        A generator object yielding the chunks of items in zip like order.

    Examples
    --------
    Simple demonstration:

    >>> import ittools
    >>> hi10 = 10 * ['hi']
    >>> print(list(ittools.zip_split(hi10, 3)))
    [['hi', 'hi', 'hi', 'hi'], ['hi', 'hi', 'hi'], ['hi', 'hi', 'hi']]

    Use case for turning a (supposedly) long iterable into a
    :class:`pandas.DataFrame` of 3 rows:

    >>> import ittools
    >>> import pandas as pd
    >>> print(pd.DataFrame(list(ittools.zip_split(hi10, 3))).to_string(
    ...     index=False, header=False))
    hi hi hi   hi
    hi hi hi None
    hi hi hi None
    """
    for i in range(chunks):
        yield sequence[i::chunks]


def group(iterable, chunks, fillvalue=None):
    """Split iterable into chunks.

    If the number of items in :paramref:`~group.iterable` is not an integer
    multiple of :paramref:`~group.chunks`, the
    last chunk is filled using :paramref:`~group.fillvalue`.

    Parameters
    ----------
    iterable: ~collections.abc.Iterable
        The iterable to split into groups.

    chunks: int
        The number of groups created

    fillvalue: ~numbers.Number, None, default = None
        The last chunk is filled with this in case the number of items in
        :paramref:`~group.iterable` is not an integer multiple of
        :paramref:`~group.chunks`

    Returns
    -------
    :class:`~collections.abc.Generator`
        A generator object yielding the groups.

    Note
    ----
    Credit to https://stackoverflow.com/a/434411
    (Boris)

    Examples
    --------
    Simple example:

    >>> import ittools
    >>> print(list(ittools.group(range(10), chunks=3)))
    [(0, 1, 2, 3), (4, 5, 6, 7), (8, 9, None, None)]

    Use case for turning a(supposedly) long iterable into a
    :class:`pandas.DataFrame` of 3 columns:

    >>> import ittools
    >>> import pandas as pd
    >>> print(pd.DataFrame(list(zip(*ittools.group(range(10), 3)))).to_string(
    ...     index=False, header=False))
    0 4 8.0
    1 5 9.0
    2 6 NaN
    3 7 NaN
    """
    length = math.ceil(len(iterable) / chunks)
    args = [iter(iterable)] * length
    return zip_longest(*args, fillvalue=fillvalue)
