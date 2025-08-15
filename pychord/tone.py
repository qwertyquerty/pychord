from pychord.ratio import Ratio


class Tone:
    frequency: float

    def __init__(self, frequency):
        self.frequency = frequency

    def __repr__(self) -> str:
        return f"[Tone ({self.frequency})]"

    def __str__(self) -> str:
        return self.__repr__()

    def __add__(self, other: "Ratio") -> "Tone":
        assert isinstance(other, Ratio)
        return self.transposed(other)

    def __sub__(self, other: "Ratio") -> "Tone":
        assert isinstance(other, Ratio)
        return self.transposed(-other)

    def __eq__(self, other: "Tone"):
        return isinstance(other, Tone) and self.frequency == other.frequency

    def __ne__(self, other: "Tone"):
        return not isinstance(other, Tone) or self.frequency != other.frequency

    def __ge__(self, other: "Tone") -> bool:
        assert isinstance(other, Tone)
        return self.frequency >= other.frequency

    def __gt__(self, other: "Tone") -> bool:
        assert isinstance(other, Tone)
        return self.frequency > other.frequency

    def __le__(self, other: "Tone") -> bool:
        assert isinstance(other, Tone)
        return self.frequency <= other.frequency

    def __lt__(self, other: "Tone") -> bool:
        assert isinstance(other, Tone)
        return self.frequency < other.frequency

    def transposed(self, interval: "Ratio") -> "Tone":
        assert isinstance(interval, Ratio)
        return Tone(self.frequency * interval.ratio)
