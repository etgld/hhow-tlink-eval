import logging
from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from lseval.correctness_matrix import Correctness, CorrectnessMatrix
from lseval.datatypes import DocTimeRel, Entity, Relation

logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
    datefmt="%m/%d/%Y %H:%M:%S",
    level=logging.INFO,
)


class TLINK(StrEnum):
    BEFORE = "BEFORE"
    CONTAINS = "CONTAINS"
    CONTAINS_1 = "CONTAINS-1"
    OVERLAP = "OVERLAP"
    BEGINS_ON = "BEGINS-ON"
    ENDS_ON = "ENDS-ON"


class TIMEX3(StrEnum):
    DATE = "DATE"
    TIME = "TIME"
    DURATION = "DURATION"
    QUANTIFIER = "QUANTIFIER"
    PREPOSTEXP = "PREPOSTEXP"
    SET = "SET"
    INSTANT = "INSTANT"


@dataclass(eq=True, frozen=True)
class Event(Entity):
    def __post_init__(self) -> None:
        pass


@dataclass(eq=True, frozen=True)
class TimeExpression(Entity):
    def __post_init__(self) -> None:
        pass


class EventType(StrEnum):
    Event = "EVENT"
    TimeExpression = "TIMEX3"
    NA = "N/A"

    @classmethod
    def _missing_(cls, value):
        return EventType.NA


@dataclass(eq=True, frozen=True)
class TemporalRelation(Relation):
    def __post_init__(self):
        if (
            not (isinstance(self.arg1, Event) and isinstance(self.arg2, TimeExpression))
            or not (
                isinstance(self.arg2, Event) and isinstance(self.arg1, TimeExpression)
            )
            or len(self.label) != 1
            or not all(map(TemporalRelation.validate_tlink_label, self.label))
        ):
            raise ValueError(f"TLINK problems {self}")

    @staticmethod
    def validate_tlink_label(label: Any) -> bool:
        return label in TLINK


@dataclass
class AnnotatedFileScores:
    file_id: int
    event_correctness_matrix: CorrectnessMatrix[Event]
    time_expression_correctness_matrix: CorrectnessMatrix[TimeExpression]
    temporal_relation_correctness_matrix: CorrectnessMatrix[TemporalRelation]
    dtr_correctness_matrices: Mapping[DocTimeRel, CorrectnessMatrix[Entity]] = field(
        default_factory=dict
    )
    cui_correctness_totals: Mapping[str, Mapping[Correctness, int]] = field(
        default_factory=dict
    )


@dataclass
class AnnotatedCorpusScores:
    event_correctness_matrix: CorrectnessMatrix[Event]
    time_expression_correctness_matrix: CorrectnessMatrix[TimeExpression]
    temporal_relation_correctness_matrix: CorrectnessMatrix[TemporalRelation]
    dtr_correctness_matrices: Mapping[DocTimeRel, CorrectnessMatrix[Entity]] = field(
        default_factory=dict
    )
    cui_correctness_totals: Mapping[str, Mapping[Correctness, int]] = field(
        default_factory=dict
    )
