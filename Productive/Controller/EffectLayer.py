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
class EffectLayer:

    def __init__(self):
        self._data_base: Connection = connect('../../models/Model/DB.db')
        self._cursor: Cursor = self._data_base.cursor()

    def _find_effects(self, term_subject: str, term_action: str, term_object: str)\
            -> Tuple[List[str], List[str], List[str]]:
        spo_query = '''SELECT Train_AttributeLabel.Effect as Result
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
        AND TermA.Text="''' + term_subject + '''"
        AND TermB.Text="''' + term_action + '''"
        AND TermC.Text="''' + term_object + '''"
        ORDER BY TermB.Text, TermA.Text;'''
        spo_entry_list = list(self._cursor.execute(spo_query))
        spo_table_content = (
            from_list(spo_entry_list)
            .pipe(map(lambda element: element[0]))
            .pipe(to_list())
            .run()
        )
        po_query = '''SELECT Train_AttributeLabel.Effect as Result
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
        AND TermB.Text="''' + term_action + '''"
        AND TermC.Text="''' + term_object + '''"
        ORDER BY TermB.Text, TermA.Text;'''
        po_entry_list = list(self._cursor.execute(po_query))
        po_table_content = (
            from_list(po_entry_list)
            .pipe(map(lambda element: element[0]))
            .pipe(to_list())
            .run()
        )
        o_query = '''SELECT Train_AttributeLabel.Effect as Result
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
        AND TermC.Text="''' + term_object + '''"
        ORDER BY TermB.Text, TermA.Text;'''
        o_entry_list = list(self._cursor.execute(o_query))
        o_table_content = (
            from_list(o_entry_list)
            .pipe(map(lambda element: element[0]))
            .pipe(to_list())
            .run()
        )
        return spo_table_content, po_table_content, o_table_content

    def _apply_effect_sentence(self, sentence: Sentence):
        term_subjects = (
            from_list(sentence.get_term_annotated_words())
            .pipe(filter(lambda term_annotated_word: term_annotated_word[1] == "Subject"))
            .pipe(map(lambda term_annotated_word: term_annotated_word[0]))
            .pipe(to_list())
            .run()
        )
        term_actions = (
            from_list(sentence.get_term_annotated_words())
            .pipe(filter(lambda term_annotated_word: term_annotated_word[1] == "Action"))
            .pipe(map(lambda term_annotated_word: term_annotated_word[0]))
            .pipe(to_list())
            .run()
        )
        term_objects = (
            from_list(sentence.get_term_annotated_words())
            .pipe(filter(lambda term_annotated_word: term_annotated_word[1] == "Object"))
            .pipe(map(lambda term_annotated_word: term_annotated_word[0]))
            .pipe(to_list())
            .run()
        )
        for term_object in term_objects:
            for term_subject in term_subjects:
                for term_action in term_actions:
                    effects = self._find_effects(term_subject, term_action, term_object)
                    sentence.set_first_class_effects(sentence.get_first_class_effects() + effects[0])
                    sentence.set_second_class_effects(sentence.get_second_class_effects() + effects[1])
                    sentence.set_third_class_effects(sentence.get_third_class_effects() + effects[2])

    def apply_effect(self, document: Document):
        (
            from_list(document.get_sentences())
            .subscribe(lambda sentence: self._apply_effect_sentence(sentence=sentence))
        )
