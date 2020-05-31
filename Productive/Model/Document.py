# <editor-fold desc="Import typing">
from typing import *
# </editor-fold>
# <editor-fold desc="Import RxPY">
from rx import from_list
from rx.operators import to_list, map, flat_map, filter
# </editor-fold>
# <editor-fold desc="Import SQLite">
from sqlite3 import *
# </editor-fold>

# <editor-fold desc="Import own classes">
from Productive.Model.Page import Page
from Productive.Model.Sentence import Sentence
# </editor-fold>


# noinspection SqlNoDataSourceInspection,SqlResolve
class Document:

    # <editor-fold desc="Constructor">
    def __init__(self, document_name: str):
        self._document_name: str = document_name
        self._data_base: Connection = self._setup_data_base()
        self._cursor: Cursor = self._setup_cursor()
        self._pages: List[Page] = self._setup_pages()
    # </editor-fold>

    # <editor-fold desc="Public interface">
    def get_sentences(self) -> List[Sentence]:
        sentences: List[Sentence] = (
            from_list(self._pages)
            .pipe(flat_map(lambda page: from_list(page.get_sentences())))
            .pipe(to_list())
            .run()
        )
        return sentences
    # </editor-fold>

    # <editor-fold desc="Setup methods">
    def _setup_data_base(self) -> Connection:
        return connect('../../Learning/models/Model/DB.db')

    def _setup_cursor(self) -> Cursor:
        return self._data_base.cursor()

    def _setup_pages(self) -> List[Page]:
        query = (
            ' SELECT FilePageNumber FROM APTReport WHERE FileName="' +
            self._document_name +
            '" ORDER BY FilePageNumber; '
        )
        entry_list = list(self._cursor.execute(query))
        pages = (
            from_list(entry_list)
            .pipe(map(lambda entry: entry[0]))
            .pipe(map((lambda page_number: Page(document_name=self._document_name, page_number=page_number))))
            .pipe(to_list())
            .run()
        )
        return pages
    # </editor-fold>
