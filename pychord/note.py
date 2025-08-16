from typing import Union

from pychord.const import *
from pychord.interval import Interval
from pychord.ratio import Ratio, SEMITONE, OCTAVE
from pychord.tone import Tone


class Note(Tone):
    """
    Describes a musical note as a Tone quantized to 12TET with A4 = 440Hz, where note 0 = C0
    """

    letter: str
    octave: int
    accidental: int
    semitone: int

    def __init__(self, note: Union[int, str]):
        if not isinstance(note, (int, str)):
            raise TypeError()

        if isinstance(note, int):
            self.semitone = note
            self.octave = self.semitone // SEMITONES_PER_OCTAVE
            self.letter = NOTE_SEMITONE_TO_COMPONENTS[self.semitone % SEMITONES_PER_OCTAVE][0]
            self.accidental = NOTE_SEMITONE_TO_COMPONENTS[self.semitone % SEMITONES_PER_OCTAVE][1]

        elif isinstance(note, str):
            name = note
            m = NOTE_NAME_RE.match(name)

            if m is None:
                raise ValueError(f"Invalid note name '{name}'!")

            self.letter = m.group(1)
            self.accidental = ACCIDENTAL_NAME_TO_VALUE[m.group(2)]
            self.octave = int(m.group(3) or NOTE_DEFAULT_OCTAVE)

            c_based_note_semitone = NOTE_NAME_TO_SEMITONE[self.letter]

            self.semitone = c_based_note_semitone + self.accidental + SEMITONES_PER_OCTAVE * self.octave

        super().__init__(
            round(
                (
                    Tone(C0_FREQUENCY)
                    + Interval(self.semitone % SEMITONES_PER_OCTAVE)
                    + (OCTAVE * (self.semitone // SEMITONES_PER_OCTAVE))
                ).frequency,
                NAMED_NOTE_FREQUENCY_PRECISION,
            )
        )

    def __repr__(self) -> str:
        return f"[Note {self.name()} ({self.frequency})]"

    def __str__(self) -> str:
        return self.__repr__()

    def __add__(self, other: Union[Interval, Ratio]):
        if not isinstance(other, (Ratio, Interval)):
            return NotImplemented
        return self.transposed(other)

    def __sub__(self, other: Union[Interval, Ratio, "Note"]):
        if isinstance(other, Ratio):
            return self.transposed(-other)
        elif isinstance(other, Note):
            return Interval(self.semitone - other.semitone)
        else:
            return NotImplemented

    def name(self) -> str:
        return f"{self.letter}{ACCIDENTAL_VALUE_TO_NAME[self.accidental]}{self.octave}"

    def transposed(self, interval: Union[Ratio, Interval]) -> Union["Note", "Tone"]:
        if not isinstance(interval, (Ratio, Interval)):
            raise TypeError()

        if isinstance(interval, Interval):
            return Note(self.semitone + interval.semitones)
        else:
            return Tone(self.frequency) + interval
