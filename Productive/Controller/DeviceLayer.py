from sqlite3 import *
from typing import *
# <editor-fold desc="Import RX">
from rx import from_list
from rx.operators import map, filter, to_list
# </editor-fold>

from Productive.Model.Sentence import Sentence
from Productive.Model.Document import Document


# noinspection SqlNoDataSourceInspection,SqlResolve
# noinspection PyMethodMayBeStatic
class DeviceLayer:

    def __init__(self):
        self._data_base: Connection = connect('../../models/Model/DB.db')
        self._cursor: Cursor = self._data_base.cursor()

    def _find_devices(self, term_object: str) -> List[str]:
        query = '''SELECT Train_TermLabel.Text
        FROM Train_AttributeLabel, Train_RelationLabel, Train_TermLabel
        WHERE Train_AttributeLabel.Type="StrategicObjectives"
        AND Train_RelationLabel.Type="ActionObj"
        AND Train_AttributeLabel.Source = Train_RelationLabel.Source
        AND Train_RelationLabel.Destination=Train_TermLabel.Key
        AND Train_TermLabel.Text="''' + term_object + '''"
        ORDER BY Train_TermLabel.Text;'''
        entry_list = list(self._cursor.execute(query))
        table_content = (
            from_list(entry_list)
            .pipe(map(lambda element: element[0]))
            .pipe(to_list())
            .run()
        )
        return table_content

    def _apply_device_sentence(self, sentence: Sentence):
        term_objects = (
            from_list(sentence.get_term_annotated_words())
            .pipe(filter(lambda term_annotated_word: term_annotated_word[1] == "Object"))
            .pipe(map(lambda term_annotated_word: term_annotated_word[0]))
            .pipe(to_list())
            .run()
        )
        for term_object in term_objects:
            devices = self._find_devices(term_object)
            sentence.set_devices(sentence.get_devices() + devices)

    def apply_device(self, document: Document):
        (
            from_list(document.get_sentences())
            .subscribe(lambda sentence: self._apply_device_sentence(sentence=sentence))
        )
