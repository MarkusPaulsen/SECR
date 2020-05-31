class Annotation:

    # <editor-fold desc="Constructor">
    def __init__(self, annotation_file_name: str, annotation_data: str):
        self._annotation_file_name: str = annotation_file_name
        self._annotation_data: str = annotation_data

    # </editor-fold>

    # <editor-fold desc="Public interface">
    def get_annotation_file_name(self) -> str:
        return self._annotation_file_name

    def get_annotation_data(self) -> str:
        return self._annotation_data

    # </editor-fold>
