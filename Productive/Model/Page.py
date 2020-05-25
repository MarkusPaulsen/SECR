from sqlite3 import *
from typing import *
# <editor-fold desc="Import RX">
from rx import from_list
from rx.operators import map, to_list, flat_map
# </editor-fold>
from nltk.tokenize import sent_tokenize
from Productive.Model.Sentence import Sentence


class Page:

    def __init__(self, document_name: str, page_number: int):
        self._data_base: Connection = connect('../../models/Model/DB.db')
        self._cursor: Cursor = self._data_base.cursor()
        self._document_name: str = document_name
        self._page_number: int = page_number
        self._sentences: List[Sentence] = self._setup_sentences()

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