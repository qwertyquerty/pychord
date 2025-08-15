from fractions import Fraction
from typing import Union

from pychord.const import *
from pychord.ratio import Ratio, SEMITONE, OCTAVE


class Interval(Ratio):
    semitones: int
    quality: str
    quantity: int

    def __init__(self, interval: Union[int, str]):
        assert isinstance(interval, (int, str))

        if isinstance(interval, int):
            self.semitones = interval

            abs_semitones = abs(self.semitones)

            self.quality = INTERVAL_VALUE_TO_COMPONENTS[abs_semitones % SEMITONES_PER_OCTAVE][0]

            self.quantity = INTERVAL_VALUE_TO_COMPONENTS[abs_semitones % SEMITONES_PER_OCTAVE][1] + (
                7 * (abs_semitones // SEMITONES_PER_OCTAVE)
            )

        elif isinstance(interval, str):
            m = INTERVAL_NAME_RE.match(interval)

            assert m is not None, f"Invalid 12TET interval name: '{interval}'!"

            self.quality = m.group(1)
            self.quantity = int(m.group(2))
            octave = 0
            offset_quantity = self.quantity

            if offset_quantity > 7:
                octave = (self.quantity - 1) // 7
                offset_quantity = self.quantity % 7

            offset_name = f"{self.quality}{offset_quantity}"

            assert offset_name in INTERVAL_NAME_TO_VALUE, f"Invalid 12TET interval name: '{offset_name}'!"

            self.semitones = octave * SEMITONES_PER_OCTAVE + INTERVAL_NAME_TO_VALUE[offset_name]

        interval = (SEMITONE * (abs(self.semitones) % SEMITONES_PER_OCTAVE)) + (
            OCTAVE * (abs(self.semitones) // SEMITONES_PER_OCTAVE)
        )
        super().__init__((interval if self.semitones >= 0 else -interval).ratio)

    def __repr__(self) -> str:
        return f"[Interval {self.name()} ({self.ratio})]"

    def __str__(self) -> str:
        return self.__repr__()

    def __add__(self, other: Union["Interval", Ratio]) -> Union["Interval", Ratio]:
        assert isinstance(other, (Interval, Ratio))

        if isinstance(other, Interval):
            return Interval(self.semitones + other.semitones)
        elif isinstance(other, Ratio):
            return Ratio(self.ratio) + other

    def __sub__(self, other: Union["Interval", Ratio]) -> Union["Interval", Ratio]:
        assert isinstance(other, (Interval, Ratio))

        if isinstance(other, Interval):
            return Interval(self.semitones - other.semitones)
        elif isinstance(other, Ratio):
            return Ratio(self.ratio) - other

    def __mul__(self, other: Union[int, float, Fraction]) -> Union["Interval", Ratio]:
        assert isinstance(other, (int, float, Fraction))

        if isinstance(other, int):
            return Interval(self.semitones * other)
        else:
            return Ratio(self.ratio) * other

    def __neg__(self) -> "Ratio":
        """
        Inversion of interval e.g. up an octave becomes down an octave
        """
        return Interval(-self.semitones)

    def compliment(self) -> "Interval":
        """
        Compliment of this interval, when added to the original interval will equal an octave
        """
        return -(self - Interval(SEMITONES_PER_OCTAVE))

    def name(self) -> "str":
        return f"{'-' if self.semitones < 0 else ''}{self.quality}{self.quantity}"
