from typing import Union

from pychord.const import *
from pychord.interval import Interval, OCTAVE
from pychord.note import Note

class Chord():
    """
    Describes a collection of `Note`s in 12TET
    """
    def __init__(self, notes: set[Note] ): 
        