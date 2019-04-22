from enum import Enum, auto


class RequestType(Enum):
    FIND_SIMILAR_PAPER = auto()
    GET_RANDOM_PAPER = auto()
    DELETE_PAPER = auto()
    ADD_PAPER = auto()
