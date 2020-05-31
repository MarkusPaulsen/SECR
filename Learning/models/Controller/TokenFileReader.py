# <editor-fold desc="Import Typing">
from typing import *
# </editor-fold>
# <editor-fold desc="Import RX">
from rx import from_list
from rx.operators import map, filter, to_list, flat_map, first
# </editor-fold>
# <editor-fold desc="Import Other Libraries">
import os
import re
# </editor-fold>

# <editor-fold desc=" Import Own Classes">

from Learning.models.Model.Token import Token
# </editor-fold>


# noinspection PyMethodMayBeStatic
class TokenFileReader:

    # <editor-fold desc="Constructor">
    def __init__(self, base_folder: str):
        self._base_folder: str = base_folder
        self._token_store: List[Token] = self._setup_token_store()

    # <editor-fold desc="Public interface">
    def get_token_store(self) -> List[Token]:
        return self._token_store

    # </editor-fold>

    # <editor-fold desc="Setup methods">

    def _setup_token_store(self) -> List[Token]:

        def _get_file_names(path) -> List[str]:
            output: List[str] = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    output = output + [os.path.join(root, file)]
            return output

        def _get_token_list(token_file_name: str, extension: str) -> List[Tuple[str, str]]:
            token_file = open(token_file_name, encoding="utf8")
            token_file_lines = token_file.readlines()
            index = 0
            file_name_token_list = []
            for line in token_file_lines:
                file_name_token = (
                    from_list([(line, index)])
                    .pipe(map(
                        lambda line_element:
                        (
                            re.sub(self._base_folder + "/", "", token_file_name),
                            line_element[0].strip("\n"),
                            line_element[1]
                        )
                    ))
                    .pipe(map(
                        lambda line_content:
                        (
                            re.sub(extension, "", line_content[0]),
                            line_content[2],
                            line_content[1].split(" ")[0] if line_content[1] != "" else "",
                            line_content[1].split(" ")[1] if line_content[1] != "" else ""
                        )
                    ))
                    .pipe(first())
                    .run()
                )
                file_name_token_list.append(file_name_token)
                index = index + 1
            # file_name_token_list: List[Tuple[str, str]] = (
            #     from_list(token_file_lines)
            #     .pipe(zip(
            #         from_list(range(0, len(token_file_lines)))
            #     ))
            #     .pipe(map(
            #         lambda line:
            #         (re.sub(self._base_folder + "/", "", token_file_name), line[0].strip("\n"), line[1])
            #     ))
            #     .pipe(map(
            #         lambda line_content:
            #         (
            #             re.sub(extension, "", line_content[0]),
            #             line_content[2],
            #             line_content[1].split(" ")[0] if line_content[1] != "" else "",
            #             line_content[1].split(" ")[1] if line_content[1] != "" else ""
            #         )
            #     ))
            #     .pipe(to_list())
            #     .run()
            # )
            token_file.close()
            return file_name_token_list
        token_store: List[Token] = (
            from_list(
                [".tokens"]
            )
            .pipe(flat_map(
                lambda extension:
                from_list(
                    _get_file_names(self._base_folder)
                )
                .pipe(filter(
                    lambda token_file_name: token_file_name.endswith(extension)
                ))
                .pipe(map(
                    lambda token_file_name: (token_file_name, extension)
                ))
            ))
            .pipe(flat_map(
                lambda token_file_name_data: from_list(_get_token_list(
                    token_file_name=token_file_name_data[0],
                    extension=token_file_name_data[1])
                )
            ))
            .pipe(map(
                lambda token_information_tuple: Token(
                    token_file_name=token_information_tuple[0],
                    line_number=token_information_tuple[1],
                    word=token_information_tuple[2],
                    token_set=token_information_tuple[3]
                )
            ))
            .pipe(to_list())
            .run()
        )
        return token_store
    # </editor-fold>
