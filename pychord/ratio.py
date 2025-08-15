from fractions import Fraction
from typing import Union

from pychord.const import *


class Ratio:
    ratio: Union[float, Fraction]

    def __init__(self, ratio: Union[float, Fraction]):
        self.ratio = ratio

    def __repr__(self):
        return f"[Ratio {self.ratio}]"

    def __str__(self):
        return self.__repr__()

    def __neg__(self) -> "Ratio":
        """
        Inversion of ratio e.g. up an octave becomes down an octave
        """
        return Ratio(1.0 / self.ratio)

    def __add__(self, other: "Ratio"):
        assert isinstance(other, Ratio)
        return Ratio(self.ratio * other.ratio)

    def __sub__(self, other: "Ratio"):
        assert isinstance(other, Ratio)
        return Ratio(self.ratio / other.ratio)

    def __mul__(self, other: Union[int, float, Fraction]) -> "Ratio":
        assert isinstance(other, (int, float, Fraction))
        return Ratio(self.ratio**other)

    def __eq__(self, other: "Ratio"):
        return isinstance(other, Ratio) and self.ratio == other.ratio

    def __ne__(self, other: "Ratio"):
        return not isinstance(other, Ratio) or self.ratio != other.ratio

    def __ge__(self, other: "Ratio") -> bool:
        assert isinstance(other, Ratio)
        return self.ratio >= other.ratio

    def __gt__(self, other: "Ratio") -> bool:
        assert isinstance(other, Ratio)
        return self.ratio > other.ratio

    def __le__(self, other: "Ratio") -> bool:
        assert isinstance(other, Ratio)
        return self.ratio <= other.ratio

    def __lt__(self, other: "Ratio") -> bool:
        assert isinstance(other, Ratio)
        return self.ratio < other.ratio

    def compliment(self) -> "Ratio":
        """
        Compliment of this ratio, when added to the original ratio will equal an octave
        """
        return -(self - OCTAVE)


SEMITONE = Ratio(2 ** (1 / 12))
OCTAVE = Ratio(Fraction(2, 1))
