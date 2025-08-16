from typing import Union

from pychord.const import *
from pychord.interval import Interval, OCTAVE
from pychord.note import Note


class Chord:
    """
    Describes a collection of `Note`s in 12TET
    """

    def __init__(self, chord: Union[set[Note], str], root: Note = None):
        """
        `chord` can either be a set of `Note`s or a string definition
        `root` is the root `Note` of the set of `Note`s; only required for passing in a set
        """
