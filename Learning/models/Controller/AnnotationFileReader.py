# <editor-fold desc="Import Typing">
from typing import *
# </editor-fold>
# <editor-fold desc="Import RX">
from rx import from_list
from rx.operators import map, filter, to_list, flat_map
# </editor-fold>
# <editor-fold desc="Import Other Libraries">
import os
import re
# </editor-fold>

# <editor-fold desc=" Import Own Classes">

from Learning.models.Model.Annotation import Annotation
# </editor-fold>


# noinspection PyMethodMayBeStatic
class AnnotationFileReader:

    # <editor-fold desc="Constructor">
    def __init__(self, base_folder: str):
        self._base_folder: str = base_folder
        self._annotation_store: List[Annotation] = self._setup_annotation_store()

    # </editor-fold>

    # <editor-fold desc="Public interface">
    def get_annotation_store(self) -> List[Annotation]:
        return self._annotation_store

    # </editor-fold>

    # <editor-fold desc="Setup methods">
    def _setup_annotation_store(self) -> List[Annotation]:

        def _get_file_names(path) -> List[str]:
            output: List[str] = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    output = output + [os.path.join(root, file)]
            return output

        def _get_annotation_list(annotation_file_name: str, extension: str) -> List[Tuple[str, str]]:
            annotation_file = open(annotation_file_name, encoding="utf8")
            file_name_annotation_list: List[Tuple[str, str]] = (
                from_list(annotation_file.readlines())
                .pipe(map(
                    lambda line:
                    (re.sub(self._base_folder + "/", "", annotation_file_name), line.strip("\n"))
                ))
                .pipe(map(
                    lambda line_content:
                    (re.sub(extension, "", line_content[0]), line_content[1])
                ))
                .pipe(to_list())
                .run()
            )
            annotation_file.close()
            return file_name_annotation_list
        annotation_store: List[Annotation] = (
            from_list(
                [".ann"]
            )
            .pipe(flat_map(
                lambda extension:
                from_list(
                    _get_file_names(self._base_folder)
                )
                .pipe(filter(
                    lambda annotation_file_name: annotation_file_name.endswith(extension)
                ))
                .pipe(map(
                    lambda annotation_file_name: (annotation_file_name, extension)
                ))
            ))
            .pipe(flat_map(
                lambda annotation_file_name_data: from_list(_get_annotation_list(
                    annotation_file_name=annotation_file_name_data[0],
                    extension=annotation_file_name_data[1])
                )
            ))
            .pipe(map(
                lambda file_name_annotation_tuple: Annotation(
                    annotation_file_name=file_name_annotation_tuple[0],
                    annotation_data=file_name_annotation_tuple[1]
                )
            ))
            .pipe(to_list())
            .run()
        )
        return annotation_store
    # </editor-fold>
