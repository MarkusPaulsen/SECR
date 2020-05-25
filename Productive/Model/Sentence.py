from typing import *

class Sentence:
    def __init__(self, document_name: str, page_number: int, sentence: str):
        self._document_name: str = document_name
        self._page_number: int = page_number
        self._sentence: str = sentence
        self._relevant: bool = True
        self._words: List[str] = []
        self._term_annotated_words: List[Tuple[str, str]] = []
        self._effects: List[str] = []
        self._devices: List[str] = []

    def get_relevant(self) -> bool:
        return self._relevant

    def get_words(self) -> List[str]:
        return self._words

    def get_term_annotated_words(self) -> List[Tuple[str, str]]:
        return self._term_annotated_words

    def get_effects(self) -> List[str]:
        return self._effects

    def get_devices(self) -> List[str]:
        return self._devices

    def set_relevant(self, relevant: bool):
        self._relevant = relevant

    def set_words(self, words: List[str]):
        self._words = words

    def set_term_annotated_words(self, term_annotated_words: List[str]):
        self._term_annotated_words = term_annotated_words

    def set_effects(self, effects: List[str]):
        self._effects = effects

    def set_devices(self, devices: List[str]):
        self._devices = devices
