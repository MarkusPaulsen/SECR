# <editor-fold desc="Import typing">
from functools import reduce
from typing import *
# </editor-fold>
# <editor-fold desc="Import RxPY">
from rx import from_list
from rx.operators import to_list, flat_map, filter, distinct, map
# </editor-fold>

# <editor-fold desc="Import own classes">
from Productive.Model.Document import Document
from Productive.Model.Sentence import Sentence
# </editor-fold>


# noinspection PyMethodMayBeStatic
class ViewLayer:

    # <editor-fold desc="Public interface">
    def print_document(self, document: Document):
        sentences: List[Sentence] = document.get_sentences()
        self._print_document_summary(sentences=sentences)
        (
            from_list(document.get_sentences())
            .pipe(filter(lambda sentence: sentence.get_relevant()))
            .subscribe(lambda relevant_sentence: self._print_sentence_summary(sentence=relevant_sentence))
        )
    # </editor-fold>

    # <editor-fold desc="Print methods">
    def _print_document_summary(self, sentences: List[Sentence]):
        relevant_sentences: List[Sentence] = (
            from_list(sentences)
            .pipe(filter(lambda sentence: sentence.get_relevant()))
            .pipe(to_list())
            .run()
        )
        print("Document summary:")
        print("")
        nr_relevant_sentences: int = len(relevant_sentences)
        print("Number of relevant sentences: " + str(nr_relevant_sentences))
        first_class_effects: str = (
            from_list(relevant_sentences)
            .pipe(filter(lambda sentence: sentence.get_first_class_effects() != []))
            .pipe(map(lambda sentence: sentence.get_first_class_effects()))
            .pipe(flat_map(lambda sentence: from_list(sentence)))
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        first_class_effect_text: str = str(reduce(
            lambda accumulator, effect: accumulator + ", " + effect, first_class_effects
        )) if first_class_effects != [] else "None"
        print("First class effects: " + first_class_effect_text)
        second_class_effects: str = (
            from_list(relevant_sentences)
            .pipe(filter(lambda sentence: sentence.get_second_class_effects() != []))
            .pipe(map(lambda sentence: sentence.get_second_class_effects()))
            .pipe(flat_map(lambda sentence: from_list(sentence)))
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        second_class_effect_text: str = str(reduce(
            lambda accumulator, effect: accumulator + ", " + effect, second_class_effects
        )) if second_class_effects != [] else "None"
        print("Second class effects: " + second_class_effect_text)
        third_class_effects: str = (
            from_list(relevant_sentences)
            .pipe(filter(lambda sentence: sentence.get_third_class_effects() != []))
            .pipe(map(lambda sentence: sentence.get_third_class_effects()))
            .pipe(flat_map(lambda sentence: from_list(sentence)))
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        third_class_effect_text: str = str(reduce(
            lambda accumulator, effect: accumulator + ", " + effect, third_class_effects
        )) if third_class_effects != [] else "None"
        print("Third class effects: " + third_class_effect_text)
        devices: str = (
            from_list(relevant_sentences)
            .pipe(filter(lambda sentence: sentence.get_devices() != []))
            .pipe(map(lambda sentence: sentence.get_devices()))
            .pipe(flat_map(lambda sentence: from_list(sentence)))
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        devices_text: str = str(reduce(
            lambda accumulator, device: accumulator + ", " + device, devices
        )) if devices != [] else "None"
        print("Devices: " + devices_text)
        print("")
        print("")
        print("")

    def _reduce_fix(self, accumulator, annotated_word):
        if type(accumulator) == tuple:
            return str(accumulator[0]) + "(" + str(accumulator[1]) + ")"\
                   + ", " + str(annotated_word[0]) + "(" + str(annotated_word[1]) + ")"
        else:
            return accumulator + ", " + str(annotated_word[0]) + "(" + str(annotated_word[1]) + ")"

    def _print_sentence_summary(self, sentence: Sentence):
        print("Relevant sentence: " + sentence.get_sentence())
        print("")
        annotated_sentence_text: str = str(reduce(
            lambda accumulator, annotated_word: self._reduce_fix(accumulator, annotated_word),
            sentence.get_term_annotated_words()
        )) if sentence.get_term_annotated_words() != [] else "None"
        print("Annotated sentence: " + annotated_sentence_text)

        first_class_effects: str = (
            from_list(sentence.get_first_class_effects())
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        first_class_effect_text: str = str(reduce(
            lambda accumulator, effect: accumulator + ", " + effect, first_class_effects
        )) if first_class_effects != [] else "None"
        print("First class effects: " + first_class_effect_text)
        second_class_effects: str = (
            from_list(sentence.get_second_class_effects())
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        second_class_effect_text: str = str(reduce(
            lambda accumulator, effect: accumulator + ", " + effect, second_class_effects
        )) if second_class_effects != [] else "None"
        print("Second class effects: " + second_class_effect_text)
        third_class_effects: str = (
            from_list(sentence.get_third_class_effects())
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        third_class_effect_text: str = str(reduce(
            lambda accumulator, effect: accumulator + ", " + effect, third_class_effects
        )) if third_class_effects != [] else "None"
        print("Third class effects: " + third_class_effect_text)
        devices: str = (
            from_list(sentence.get_devices())
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        devices_text: str = str(reduce(
            lambda accumulator, effect: accumulator + ", " + effect, devices
        )) if devices != [] else "None"
        print("Devices: " + devices_text)
        print("")
        print("")
        print("")
    # </editor-fold>
