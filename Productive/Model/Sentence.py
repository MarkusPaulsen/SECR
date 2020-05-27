# <editor-fold desc="Import typing">
from typing import *
# </editor-fold>


class Sentence:

    # <editor-fold desc="Constructor">
    def __init__(self, document_name: str, page_number: int, sentence: str):
        self._document_name: str = document_name
        self._page_number: int = page_number
        self._sentence: str = sentence
        self._relevant: bool = True
        self._words: List[str] = []
        self._term_annotated_words: List[Tuple[str, str]] = []
        self._first_class_effects: List[str] = []
        self._second_class_effects: List[str] = []
        self._third_class_effects: List[str] = []
        self._devices: List[str] = []
    # </editor-fold>

    # <editor-fold desc="Public interface">
    def get_sentence(self) -> str:
        return self._sentence

    def get_relevant(self) -> bool:
        return self._relevant

    def get_words(self) -> List[str]:
        return self._words

    def get_term_annotated_words(self) -> List[Tuple[str, str]]:
        return self._term_annotated_words

    def get_first_class_effects(self) -> List[str]:
        return self._first_class_effects

    def get_second_class_effects(self) -> List[str]:
        return self._second_class_effects

    def get_third_class_effects(self) -> List[str]:
        return self._third_class_effects

    def get_devices(self) -> List[str]:
        return self._devices

    def set_relevant(self, relevant: bool):
        self._relevant = relevant

    def set_words(self, words: List[str]):
        self._words = words

    def set_term_annotated_words(self, term_annotated_words: List[str]):
        self._term_annotated_words = term_annotated_words

    def set_first_class_effects(self, first_class_effects: List[str]):
        self._first_class_effects = first_class_effects

    def set_second_class_effects(self, second_class_effects: List[str]):
        self._second_class_effects = second_class_effects

    def set_third_class_effects(self, third_class_effects: List[str]):
        self._third_class_effects = third_class_effects

    def set_devices(self, devices: List[str]):
        self._devices = devices
    # </editor-fold>
