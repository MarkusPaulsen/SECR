from sqlite3 import *
from typing import *
# <editor-fold desc="Import RX">
from rx import from_list
from rx.operators import map, to_list
# </editor-fold>

from Productive.Model.Page import Page


class Document:

    def __init__(self, document_name: str):
        self._data_base: Connection = connect('../../models/Model/DB.db')
        self._cursor: Cursor = self._data_base.cursor()
        self._document_name: str = document_name
        self._pages: List[Page] = self._setup_pages()

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
