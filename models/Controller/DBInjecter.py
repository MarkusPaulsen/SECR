# <editor-fold desc="Import Typing">
from functools import reduce
from typing import *
# </editor-fold>
# <editor-fold desc="Import RX">
from rx import from_list
from rx.operators import map, filter, to_list
# </editor-fold>
import sqlite3

from models.Model.Annotation import Annotation


# noinspection PyMethodMayBeStatic
class DBInjecter:

    # <editor-fold desc="Constructor">
    def __init__(self):
        self._data_base = self._setup_data_base()
        self._cursor = self._setup_cursor()
        self._annotation_store: List[Annotation] = self._setup_annotation_store()

    # </editor-fold>

    # <editor-fold desc="Public interface">
    def set_annotation_store(self, annotation_store: List[Annotation]):
        self._annotation_store = annotation_store

    # </editor-fold>

    # <editor-fold desc="Setup methods">
    def _setup_data_base(self):
        return sqlite3.connect('../Model/DB.db')

    def _setup_cursor(self):
        return self._data_base.cursor()

    def _setup_annotation_store(self):
        return []

    # </editor-fold>

    # <editor-fold desc="DB inject method">
    def db_inject(self):
        attribute_label_list = (
            from_list(self._annotation_store)
            .pipe(filter(
                lambda annotation: annotation.get_annotation_data()[0] == "A"
            ))
            .pipe(map(
                lambda annotation: (
                    annotation.get_annotation_file_name(),
                    annotation.get_annotation_data().split("\t")
                )
            ))
            .pipe(map(
                lambda annotation_data: (
                    annotation_data[0],
                    annotation_data[0] + "_" + annotation_data[1][0],
                    annotation_data[1][1].split(" ")
                )
            ))
            .pipe(map(
                lambda annotation_data: (
                    annotation_data[1],
                    annotation_data[2][0],
                    annotation_data[0] + "_" + annotation_data[2][1],
                    annotation_data[2][2]
                )
            ))
            .pipe(to_list())
            .run()
        )
        self._cursor.executemany("INSERT INTO AttributeLabel VALUES(?, ?, ?, ?)", attribute_label_list)
        relation_label_list = (
            from_list(self._annotation_store)
            .pipe(filter(
                lambda annotation: annotation.get_annotation_data()[0] == "R"
            ))
            .pipe(map(
                lambda annotation: (
                    annotation.get_annotation_file_name(),
                    annotation.get_annotation_data().split("\t")
                )
            ))
            .pipe(map(
                lambda annotation_data: (
                    annotation_data[0],
                    annotation_data[0] + "_" + annotation_data[1][0],
                    annotation_data[1][1].split(" ")
                )
            ))
            .pipe(map(
                lambda annotation_data: (
                    annotation_data[1],
                    annotation_data[2][0],
                    annotation_data[0] + "_" + annotation_data[2][1].split(":")[1],
                    annotation_data[0] + "_" + annotation_data[2][2].split(":")[1]
                )
            ))
            .pipe(to_list())
            .run()
        )
        self._cursor.executemany("INSERT INTO RelationLabel VALUES(?, ?, ?, ?)", relation_label_list)
        term_label_list = (
            from_list(self._annotation_store)
            .pipe(filter(
                lambda annotation: annotation.get_annotation_data()[0] == "T"
            ))
            .pipe(map(
                lambda annotation: (
                    annotation.get_annotation_file_name(),
                    annotation.get_annotation_data().split("\t")
                )
            ))
            .pipe(map(
                lambda annotation_data: (
                    annotation_data[0] + "_" + annotation_data[1][0],
                    annotation_data[1][1].split(" "),
                    annotation_data[1][2]
                )
            ))
            .pipe(map(
                lambda annotation_data: (
                    annotation_data[0],
                    annotation_data[1][0],
                    reduce(lambda accumulator, number: accumulator + ";" + number, annotation_data[1][1:], "")[1:],
                    annotation_data[2]
                )
            ))
            .pipe(to_list())
            .run()

        )
        self._cursor.executemany("INSERT INTO TermLabel VALUES(?, ?, ?, ?)", term_label_list)
        self._data_base.commit()

    # </editor-fold>
