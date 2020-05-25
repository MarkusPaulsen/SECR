class Token:

    # <editor-fold desc="Constructor">
    def __init__(self, token_file_name: str, line_number: int,  word: str, token_set: str):
        self._token_file_name: str = token_file_name
        self._line_number: int = line_number
        self._word: str = word
        self._token_set: str = token_set

    # </editor-fold>

    # <editor-fold desc="Public interface">
    def get_token_file_name(self) -> str:
        return self._token_file_name

    def get_line_number(self) -> int:
        return self._line_number

    def get_word(self) -> str:
        return self._word

    def get_token_set(self) -> str:
        return self._token_set

    # </editor-fold>
