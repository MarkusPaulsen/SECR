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
class DeviceLayer:

    # <editor-fold desc="Constructor">
    def __init__(self):
        self._data_base: Connection = self._setup_data_base()
        self._cursor: Cursor = self._setup_cursor()
        self._query: str = self._setup_query()
        self._entry_list: List[Tuple[str]] = self._setup_entry_list()
    # </editor-fold>

    # <editor-fold desc="Public interface">
    def apply_device(self, document: Document):
        (
            from_list(document.get_sentences())
            .pipe(filter(lambda sentence: sentence.get_term_annotated_words() != []))
            .subscribe(lambda sentence: self._apply_device_sentence(sentence=sentence))
        )
    # </editor-fold>

    # <editor-fold desc="Lookup methods">
    def _find_devices(self, term_object: str) -> List[str]:
        table_content: List[str] = (
            from_list(self._entry_list)
            .pipe(map(lambda element: element[0]))
            .pipe(filter(lambda hard_software: hard_software == term_object))
            .pipe(distinct())
            .pipe(to_list())
            .run()
        )
        return table_content

    def _apply_device_sentence(self, sentence: Sentence):
        term_objects: List[str] = (
            from_list(sentence.get_term_annotated_words())
            .pipe(filter(lambda term_annotated_word: term_annotated_word[1] == "Object"))
            .pipe(map(lambda term_annotated_word: term_annotated_word[0]))
            .pipe(to_list())
            .run()
        )
        for term_object in term_objects:
            devices = self._find_devices(term_object)
            sentence.set_devices(list(set(sentence.get_devices() + devices)))
    # </editor-fold>

    # <editor-fold desc="Setup methods">
    def _setup_data_base(self) -> Connection:
        return connect('../../Learning/models/Model/DB.db')

    def _setup_cursor(self) -> Cursor:
        return self._data_base.cursor()

    def _setup_query(self) -> str:
        return '''SELECT Train_TermLabel.Text
                FROM Train_AttributeLabel, Train_RelationLabel, Train_TermLabel
                WHERE Train_AttributeLabel.Type="StrategicObjectives"
                AND Train_RelationLabel.Type="ActionObj"
                AND Train_AttributeLabel.Source = Train_RelationLabel.Source
                AND Train_RelationLabel.Destination=Train_TermLabel.Key
                ORDER BY Train_TermLabel.Text;'''

    def _setup_entry_list(self) -> List[Tuple[str]]:
        return list(self._cursor.execute(self._query))
    # </editor-fold>
