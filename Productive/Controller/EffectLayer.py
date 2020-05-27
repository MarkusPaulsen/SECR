# <editor-fold desc="Import typing">
from typing import *
# </editor-fold>
# <editor-fold desc="Import RxPY">
from rx import from_list
from rx.operators import to_list, map, filter, distinct
# </editor-fold>
# <editor-fold desc="Import SQLite">
from sqlite3 import *
# </editor-fold>

# <editor-fold desc="Import own classes">
from Productive.Model.Document import Document
from Productive.Model.Sentence import Sentence
# </editor-fold>


# noinspection SqlNoDataSourceInspection,SqlResolve
# noinspection PyMethodMayBeStatic
class EffectLayer:

    # <editor-fold desc="Constructor">
    def __init__(self):
        self._data_base: Connection = self._setup_data_base()
        self._cursor: Cursor = self._setup_cursor()
        self._query: str = self._setup_query()
        self._entry_list: List[Tuple[str, str, str, str]] = self._setup_entry_list()
    # </editor-fold>

    # <editor-fold desc="Public interface">
    def apply_effect(self, document: Document):
        (
            from_list(document.get_sentences())
            .pipe(filter(lambda sentence: sentence.get_term_annotated_words() != []))
            .subscribe(lambda sentence: self._apply_effect_sentence(sentence=sentence))
        )
    # </editor-fold>

    # <editor-fold desc="Lookup methods">
    def _find_effects(self, term_subject: str, term_action: str, term_object: str)\
            -> Tuple[List[str], List[str], List[str]]:
        spo_table_content: List[str] = (
            from_list(self._entry_list)
            .pipe(filter(
                lambda element:
                term_subject == element[0] and term_action == element[1] and term_object == element[2]
            ))
            .pipe(map(lambda element: element[3]))
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        po_table_content: List[str] = (
            from_list(self._entry_list)
            .pipe(filter(
                lambda element:
                term_action == element[1] and term_object == element[2]
            ))
            .pipe(map(lambda element: element[3]))
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        o_table_content: List[str] = (
            from_list(self._entry_list)
            .pipe(filter(
                lambda element:
                term_object == element[2]
            ))
            .pipe(map(lambda element: element[3]))
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        return spo_table_content, po_table_content, o_table_content

    def _apply_effect_sentence(self, sentence: Sentence):
        term_subjects: List[str] = (
            from_list(sentence.get_term_annotated_words())
            .pipe(filter(lambda term_annotated_word: term_annotated_word[1] == "Subject"))
            .pipe(map(lambda term_annotated_word: term_annotated_word[0]))
            .pipe(to_list())
            .run()
        )
        term_actions: List[str] = (
            from_list(sentence.get_term_annotated_words())
            .pipe(filter(lambda term_annotated_word: term_annotated_word[1] == "Action"))
            .pipe(map(lambda term_annotated_word: term_annotated_word[0]))
            .pipe(to_list())
            .run()
        )
        term_objects: List[str] = (
            from_list(sentence.get_term_annotated_words())
            .pipe(filter(lambda term_annotated_word: term_annotated_word[1] == "Object"))
            .pipe(map(lambda term_annotated_word: term_annotated_word[0]))
            .pipe(to_list())
            .run()
        )
        for term_object in term_objects:
            for term_action in term_actions:
                for term_subject in term_subjects:
                    effects = self._find_effects(term_subject, term_action, term_object)
                    sentence.set_first_class_effects(list(set(sentence.get_first_class_effects() + effects[0])))
                    sentence.set_second_class_effects(list(set(sentence.get_second_class_effects() + effects[1])))
                    sentence.set_third_class_effects(list(set(sentence.get_third_class_effects() + effects[2])))
    # </editor-fold>

    # <editor-fold desc="Setup methods">
    def _setup_data_base(self) -> Connection:
        return connect('../../Learning/models/Model/DB.db')

    def _setup_cursor(self) -> Cursor:
        return self._data_base.cursor()

    def _setup_query(self) -> str:
        return '''SELECT TermA.Text as Subject,
                TermB.Text as Predicate,
                TermC.Text as Object,
                Train_AttributeLabel.Effect as Result
                FROM Train_AttributeLabel, Train_RelationLabel as RelA,
                Train_RelationLabel as RelB, Train_TermLabel as TermA,
                Train_TermLabel as TermB, Train_TermLabel as TermC
                WHERE RelA.Type="SubjAction"
                AND RelB.Type="ActionObj"
                AND Train_AttributeLabel.Source = RelA.Destination
                AND Train_AttributeLabel.Source = RelB.Source
                AND RelA.Source=TermA.Key
                AND RelA.Destination=TermB.Key
                AND RelB.Destination=TermC.Key
                ORDER BY TermB.Text, TermA.Text;'''

    def _setup_entry_list(self) -> List[Tuple[str, str, str, str]]:
        return list(self._cursor.execute(self._query))
    # </editor-fold>
