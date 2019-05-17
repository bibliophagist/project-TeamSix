from enum import Enum, auto


class RequestType(Enum):
    FIND_SIMILAR_PAPER = auto()
    GET_RANDOM_PAPER = auto()
    DELETE_PAPER = auto()
    ADD_PAPER = auto()
    UPDATE_PAPER = auto()
    GET_PAPER = auto()
    SHOW_HISTORY = auto()
    CLEAN_HISTORY = auto()
