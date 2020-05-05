# <editor-fold desc="Import Typing">
import multiprocessing
from functools import reduce
from sqlite3 import Cursor, Connection
from typing import *
# </editor-fold>
# <editor-fold desc="Import RX">
from rx import from_list
from rx.operators import map, filter, to_list
# </editor-fold>
import sqlite3

from rx.scheduler import ThreadPoolScheduler

from models.Model.APTReport import APTReport
from models.Model.Annotation import Annotation


# noinspection PyMethodMayBeStatic
class DBInjecter:

    # <editor-fold desc="Constructor">
    def __init__(self):
        self._data_base: Connection = self._setup_data_base()
        self._cursor: Cursor = self._setup_cursor()
        self._annotation_store: List[Annotation] = self._setup_annotation_store()
        self._apt_report_store: List[APTReport] = self._setup_apt_report_store()

    # </editor-fold>

    # <editor-fold desc="Public interface">
    def set_annotation_store(self, annotation_store: List[Annotation]):
        self._annotation_store = annotation_store

    def set_apt_report_store(self, apt_report_store: List[APTReport]):
        self._apt_report_store = apt_report_store

    # </editor-fold>

    # <editor-fold desc="Setup methods">
    def _setup_data_base(self) -> Connection:
        return sqlite3.connect('../Model/DB.db')

    def _setup_cursor(self) -> Cursor:
        return self._data_base.cursor()

    def _setup_annotation_store(self) -> List[Annotation]:
        return []

    def _setup_apt_report_store(self) -> List[APTReport]:
        return []

    # </editor-fold>

    # <editor-fold desc="DB inject method">
    def db_inject(self):
        optimal_thread_count = multiprocessing.cpu_count() + 1
        pool_scheduler = ThreadPoolScheduler(optimal_thread_count)
        # <editor-fold desc="Delete old Data">
        self._cursor.execute("DELETE FROM AttributeLabel")
        self._cursor.execute("DELETE FROM RelationLabel")
        self._cursor.execute("DELETE FROM TermLabel")
        self._cursor.execute("DELETE FROM APTReport")
        # </editor-fold>
        self._data_base.commit()
        # <editor-fold desc="Store attribute labels">
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
        # </editor-fold>
        # <editor-fold desc="Store relation labels">
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
        # </editor-fold>
        # <editor-fold desc="Store term labels">
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
        # </editor-fold>
        self._data_base.commit()
        # <editor-fold desc="Store APT reports">
        apt_report_list = (
            from_list(self._apt_report_store)
            .pipe(map(
                lambda apt_report: (
                    apt_report.get_apt_report_file_name(),
                    apt_report.get_apt_report_data()
                )
            ))
            .pipe(to_list())
            .run()

        )
        self._cursor.executemany("INSERT INTO APTReport VALUES(?, ?)", apt_report_list)
        # </editor-fold>
        self._data_base.commit()

    # </editor-fold>
