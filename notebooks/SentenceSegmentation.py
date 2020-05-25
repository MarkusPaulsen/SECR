# <editor-fold desc="Import RX">
from rx import from_list
from rx.operators import map, filter, to_list
# </editor-fold>

from typing import *
from nltk.tokenize import sent_tokenize
import sqlite3
from sqlite3 import Cursor, Connection


# noinspection PyMethodMayBeStatic
class Document:
    def __init__(self, name: str):
        self._data_base: Connection = sqlite3.connect('../models/Model/DB.db')
        self._cursor: Cursor = self._data_base.cursor()
        self._name: str = name
        self._sentences: List[List[str]] = self.get_sentences()
        self._relevant_sentences: List[List[str]] = self.get_relevant_sentences()
        self._annotated_relevant_sentences: List[List[Tuple[str, str]]] = self.get_annotated_sentences()
        self._first_class_effects: List[str] = []
        self._second_class_effects: List[str] = []
        self._third_class_effects: List[str] = []
        self._devices: List[str] = []

    def get_sentences(self) -> List[List[str]]:
        query = 'SELECT FileContent FROM APTReport WHERE FileName="' + self._name + '" ORDER BY FilePageNumber;'
        entry_list = list(self._cursor.execute(query))
        sentences = (
            from_list(entry_list)
            .pipe(map(lambda entry: entry[0]))
            .pipe(map(lambda document: sent_tokenize(document)))
            .pipe(to_list())
            .run()
        )
        return sentences

    def classify_relevance(self, sentence: str):
        return True

    def get_relevant_sentences(self) -> List[List[str]]:
        relevant_sentences: List[List[str]] = []
        for page in self._sentences:
            relevant_sentences_page = (
                from_list(page)
                .pipe(filter(lambda sentence: self.classify_relevance(sentence)))
                .pipe(to_list())
                .run()
            )
            relevant_sentences.append(relevant_sentences_page)
        return relevant_sentences

    def classify_term(self, word: str) -> Tuple[str, str]:
        return "", ""

    def annotate_sentence(self, sentence: str) -> List[Tuple[str, str]]:
        annotated_sentence = (
            from_list(sentence.split(" "))
            .pipe(map(lambda word: self.classify_term(word)))
            .pipe(to_list())
            .run()
        )
        return annotated_sentence

    def get_annotated_sentences(self) -> List[List[Tuple[str, str]]]:
        annotated_sentences: List[List[Tuple[str, str]]] = []
        for page in self._relevant_sentences:
            relevant_sentences_page = (
                from_list(page)
                .pipe(map(lambda sentence: self.annotate_sentence(sentence)))
                .pipe(to_list())
                .run()
            )
            annotated_sentences.append(relevant_sentences_page)
        return annotated_sentences

    def find_effects(self, subject: str, predicate: str, object: str) -> Tuple[List[str], List[str], List[str]]:
        spo_query = '''SELECT Train_AttributeLabel.Effect as Result
        FROM Train_AttributeLabel, Train_RelationLabel as RelA, Train_RelationLabel as RelB, Train_TermLabel as TermA, Train_TermLabel as TermB, Train_TermLabel as TermC
        WHERE RelA.Type="SubjAction"
        AND RelB.Type="ActionObj"
        AND Train_AttributeLabel.Source = RelA.Destination
        AND Train_AttributeLabel.Source = RelB.Source
        AND RelA.Source=TermA.Key
        AND RelA.Destination=TermB.Key
        AND RelB.Destination=TermC.Key
        AND TermA.Text="''' + subject + '''"
        AND TermB.Text="''' + predicate + '''"
        AND TermC.Text="''' + object + '''"
        ORDER BY TermB.Text, TermA.Text;'''
        spo_query_entry_list = list(self._cursor.execute(spo_query))
        spo_table_content = (
            from_list(spo_query_entry_list)
            .pipe(map(lambda element: element[0]))
            .pipe(to_list())
            .run()
        )
        po_query = '''SELECT Train_AttributeLabel.Effect as Result
        FROM Train_AttributeLabel, Train_RelationLabel as RelA, Train_RelationLabel as RelB, Train_TermLabel as TermA, Train_TermLabel as TermB, Train_TermLabel as TermC
        WHERE RelA.Type="SubjAction"
        AND RelB.Type="ActionObj"
        AND Train_AttributeLabel.Source = RelA.Destination
        AND Train_AttributeLabel.Source = RelB.Source
        AND RelA.Source=TermA.Key
        AND RelA.Destination=TermB.Key
        AND RelB.Destination=TermC.Key
        AND TermB.Text="''' + predicate + '''"
        AND TermC.Text="''' + object + '''"
        ORDER BY TermB.Text, TermA.Text;'''
        po_query_entry_list = list(self._cursor.execute(po_query))
        po_table_content = (
            from_list(po_query_entry_list)
                .pipe(map(lambda element: element[0]))
                .pipe(to_list())
                .run()
        )
        o_query = '''SELECT Train_AttributeLabel.Effect as Result
        FROM Train_AttributeLabel, Train_RelationLabel as RelA, Train_RelationLabel as RelB, Train_TermLabel as TermA, Train_TermLabel as TermB, Train_TermLabel as TermC
        WHERE RelA.Type="SubjAction"
        AND RelB.Type="ActionObj"
        AND Train_AttributeLabel.Source = RelA.Destination
        AND Train_AttributeLabel.Source = RelB.Source
        AND RelA.Source=TermA.Key
        AND RelA.Destination=TermB.Key
        AND RelB.Destination=TermC.Key
        AND TermC.Text="''' + object + '''"
        ORDER BY TermB.Text, TermA.Text;'''
        o_query_entry_list = list(self._cursor.execute(o_query))
        o_table_content = (
            from_list(o_query_entry_list)
                .pipe(map(lambda element: element[0]))
                .pipe(to_list())
                .run()
        )
        return spo_table_content, po_table_content, o_table_content

    def find_devices(self, object: str):
        query = '''SELECT Train_AttributeLabel.Effect, Train_TermLabel.Text
        FROM Train_AttributeLabel, Train_RelationLabel, Train_TermLabel
        WHERE Train_AttributeLabel.Type="StrategicObjectives"
        AND Train_RelationLabel.Type="ActionObj"
        AND Train_AttributeLabel.Source = Train_RelationLabel.Source
        AND Train_RelationLabel.Destination=Train_TermLabel.Key
        ORDER BY Train_TermLabel.Text;'''
        table_content = list(self._cursor.execute(query))



a = Document(name="2019/Fireeye_rpt-apt41(08-07-2019).pdf")
