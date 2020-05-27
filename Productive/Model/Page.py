# <editor-fold desc="Import typing">
from typing import *
# </editor-fold>
# <editor-fold desc="Import RxPY">
from rx import from_list
from rx.operators import to_list, map, flat_map
# </editor-fold>
# <editor-fold desc="Import SQLite">
from sqlite3 import *
# </editor-fold>
# <editor-fold desc="Import other classes">
from nltk.tokenize import sent_tokenize
# </editor-fold>

# <editor-fold desc="Import own classes">
from Productive.Model.Sentence import Sentence
# </editor-fold>


# noinspection SqlNoDataSourceInspection,SqlResolve
class Page:

    # <editor-fold desc="Constructor">
    def __init__(self, document_name: str, page_number: int):
        self._document_name: str = document_name
        self._page_number: int = page_number
        self._data_base: Connection = self._setup_data_base()
        self._cursor: Cursor = self._setup_cursor()
        self._sentences: List[Sentence] = self._setup_sentences()
    # </editor-fold>

    # <editor-fold desc="Public interface">
    def get_sentences(self) -> List[Sentence]:
        return self._sentences
    # </editor-fold>

    # <editor-fold desc="Setup methods">
    def _setup_data_base(self) -> Connection:
        return connect('../../Learning/models/Model/DB.db')

    def _setup_cursor(self) -> Cursor:
        return self._data_base.cursor()

    def _setup_sentences(self) -> List[Sentence]:
        query = (
            'SELECT FileContent FROM APTReport WHERE FileName="' +
            self._document_name +
            '" AND FilePageNumber=' +
            str(self._page_number) +
            ' ORDER BY FileContent;'
        )
        entry_list = list(self._cursor.execute(query))
        sentences = (
            from_list(entry_list)
            .pipe(map(lambda entry: entry[0]))
            .pipe(flat_map(lambda document: sent_tokenize(document)))
            .pipe(map((
                lambda sentence:
                Sentence(document_name=self._document_name, page_number=self._page_number, sentence=sentence))
            ))
            .pipe(to_list())
            .run()
        )
        return sentences
    # </editor-fold>
