# <editor-fold desc="Import Typing">
from functools import reduce
from sqlite3 import Cursor, Connection
from typing import *
# </editor-fold>
# <editor-fold desc="Import RX">
from rx import from_list
from rx.operators import map, filter, to_list
# </editor-fold>
import sqlite3

from Learning.models.Model.APTReport import APTReport
from Learning.models.Model.Annotation import Annotation


# noinspection PyMethodMayBeStatic
from Learning.models.Model.Token import Token


# noinspection PyMethodMayBeStatic
class DBInjecter:

    # <editor-fold desc="Constructor">
    def __init__(self):
        self._data_base: Connection = self._setup_data_base()
        self._cursor: Cursor = self._setup_cursor()

        self._train_annotation_store: List[Annotation] = self._setup_annotation_store()
        self._dev_annotation_store: List[Annotation] = self._setup_annotation_store()
        self._test_annotation_store: List[Annotation] = self._setup_annotation_store()

        self._train_token_store: List[Token] = self._setup_token_store()
        self._dev_token_store: List[Token] = self._setup_token_store()
        self._test_token_store: List[Token] = self._setup_token_store()

        self._apt_report_store: List[APTReport] = self._setup_apt_report_store()

    # </editor-fold>

    # <editor-fold desc="Public interface">
    def set_train_annotation_store(self, train_annotation_store: List[Annotation]):
        self._train_annotation_store = train_annotation_store

    def set_dev_annotation_store(self, dev_annotation_store: List[Annotation]):
        self._dev_annotation_store = dev_annotation_store

    def set_test_annotation_store(self, test_annotation_store: List[Annotation]):
        self._test_annotation_store = test_annotation_store

    def set_train_token_store(self, train_token_store: List[Token]):
        self._train_token_store = train_token_store

    def set_dev_token_store(self, dev_token_store: List[Token]):
        self._dev_token_store = dev_token_store

    def set_test_token_store(self, test_token_store: List[Token]):
        self._test_token_store = test_token_store

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

    def _setup_token_store(self) -> List[Token]:
        return []

    def _setup_apt_report_store(self) -> List[APTReport]:
        return []

    # </editor-fold>

    # <editor-fold desc="DB inject method">
    def db_inject_attribute_label_list(self, source: List[Annotation], table: str):
        self._cursor.execute("DELETE FROM " + table)
        self._data_base.commit()
        attribute_label_list = (
            from_list(source)
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
                    annotation_data[0] + "_" + annotation_data[1][0],
                    annotation_data[0],
                    annotation_data[1][0],
                    annotation_data[1][1].split(" ")
                )
            ))
            .pipe(map(
                lambda annotation_data: (
                    annotation_data[0],
                    annotation_data[1],
                    annotation_data[2],
                    annotation_data[3][0],
                    annotation_data[0].split("_")[0] + "_" + annotation_data[3][1],
                    annotation_data[3][2]
                )
            ))
            .pipe(to_list())
            .run()
        )
        self._cursor.executemany("INSERT INTO " + table + " VALUES(?, ?, ?, ?, ?, ?)", attribute_label_list)
        self._data_base.commit()

    def db_inject_relation_label_list(self, source: List[Annotation], table: str):
        self._cursor.execute("DELETE FROM " + table)
        self._data_base.commit()
        relation_label_list = (
            from_list(source)
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
                    annotation_data[0] + "_" + annotation_data[1][0],
                    annotation_data[0],
                    annotation_data[1][0],
                    annotation_data[1][1].split(" ")
                )
            ))
            .pipe(map(
                lambda annotation_data: (
                    annotation_data[0],
                    annotation_data[1],
                    annotation_data[2],
                    annotation_data[3][0],
                    annotation_data[0].split("_")[0] + "_" + annotation_data[3][1].split(":")[1],
                    annotation_data[0].split("_")[0] + "_" + annotation_data[3][2].split(":")[1]
                )
            ))
            .pipe(to_list())
            .run()
        )
        self._cursor.executemany("INSERT INTO " + table + " VALUES(?, ?, ?, ?, ?, ?)", relation_label_list)
        self._data_base.commit()

    def db_inject_term_label_list(self, source: List[Annotation], table: str):
        self._cursor.execute("DELETE FROM " + table)
        self._data_base.commit()
        term_label_list = (
            from_list(source)
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
                    annotation_data[0],
                    annotation_data[1][0],
                    annotation_data[1][1].split(" "),
                    annotation_data[1][2]
                )
            ))
            .pipe(map(
                lambda annotation_data: (
                    annotation_data[0],
                    annotation_data[1],
                    annotation_data[2],
                    annotation_data[3][0],
                    reduce(
                        lambda accumulator, number:
                        accumulator + ";" + number, annotation_data[3][1:], ""
                    )[1:],
                    annotation_data[4]
                )
            ))
            .pipe(to_list())
            .run()

        )
        self._cursor.executemany("INSERT INTO " + table + " VALUES(?, ?, ?, ?, ?, ?)", term_label_list)
        self._data_base.commit()

    def db_inject_token_list(self, source: List[Token], table: str):
        self._cursor.execute("DELETE FROM " + table)
        self._data_base.commit()
        token_list = (
            from_list(source)
            .pipe(map(
                lambda token: (
                    token.get_token_file_name() + "_" + str(token.get_line_number()),
                    token.get_token_file_name(),
                    token.get_line_number(),
                    token.get_word(),
                    token.get_token_set()
                )
            ))
            .pipe(to_list())
            .run()

        )
        self._cursor.executemany("INSERT INTO " + table + " VALUES(?, ?, ?, ?, ?)", token_list)
        self._data_base.commit()

    def db_inject_atp_report_list(self):
        self._cursor.execute("DELETE FROM APTReport")
        self._data_base.commit()
        apt_report_list = (
            from_list(self._apt_report_store)
            .pipe(map(
                lambda apt_report: (
                    apt_report.get_apt_report_index(),
                    apt_report.get_apt_report_file_name(),
                    apt_report.get_apt_report_page_number(),
                    apt_report.get_apt_report_data()
                )
            ))
            .pipe(to_list())
            .run()

        )
        self._cursor.executemany("INSERT INTO APTReport VALUES(?, ?, ?, ?)", apt_report_list)
        self._data_base.commit()

    def db_inject(self):
        # self.db_inject_term_label_list(source=self._train_annotation_store, table="Train_TermLabel")
        # self.db_inject_relation_label_list(source=self._train_annotation_store, table="Train_RelationLabel")
        # self.db_inject_attribute_label_list(source=self._train_annotation_store, table="Train_AttributeLabel")
        # self.db_inject_term_label_list(source=self._dev_annotation_store, table="Dev_TermLabel")
        # self.db_inject_relation_label_list(source=self._dev_annotation_store, table="Dev_RelationLabel")
        # self.db_inject_attribute_label_list(source=self._dev_annotation_store, table="Dev_AttributeLabel")
        # self.db_inject_term_label_list(source=self._test_annotation_store, table="Test_TermLabel")
        # self.db_inject_relation_label_list(source=self._test_annotation_store, table="Test_RelationLabel")
        # self.db_inject_attribute_label_list(source=self._test_annotation_store, table="Test_AttributeLabel")
        # self.db_inject_token_list(source=self._train_token_store, table="Train_Token")
        # self.db_inject_token_list(source=self._dev_token_store, table="Dev_Token")
        # self.db_inject_token_list(source=self._test_token_store, table="Test_Token")
        self.db_inject_atp_report_list()

    # </editor-fold>
