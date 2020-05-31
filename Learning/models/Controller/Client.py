from Learning.models.Controller.AnnotationFileReader import AnnotationFileReader
from Learning.models.Controller.TokenFileReader import TokenFileReader
from Learning.models.Controller.APTReportsFileReader import APTReportFileReader
from Learning.models.Controller.DBInjecter import DBInjecter


class Client:

    # <editor-fold desc="Constructor">
    def __init__(self):
        self._traintfr: TokenFileReader = TokenFileReader(
            base_folder="../../data/MalwareTextDB-2.0/data/train/tokenized"
        )
        self._devtfr: TokenFileReader = TokenFileReader(
            base_folder="../../data/MalwareTextDB-2.0/data/dev/tokenized"
        )
        self._testtfr: TokenFileReader = TokenFileReader(
            base_folder="../../data/MalwareTextDB-2.0/data/test_1/tokenized"
        )
        self._trainafr: AnnotationFileReader = AnnotationFileReader(
            base_folder="../../data/MalwareTextDB-2.0/data/train/annotations"
        )
        self._devafr: AnnotationFileReader = AnnotationFileReader(
            base_folder="../../data/MalwareTextDB-2.0/data/dev/annotations"
        )
        self._testafr: AnnotationFileReader = AnnotationFileReader(
            base_folder="../../data/MalwareTextDB-2.0/data/test_1/annotations"
        )
        self._arr: APTReportFileReader = APTReportFileReader(
            base_folder="../../data/APTReports"
        )
        self._dbi: DBInjecter = DBInjecter()
        self._prepare_injection()

    # </editor-fold>

    # <editor-fold desc="Prepare injection method">
    def _prepare_injection(self):
        self._dbi.set_train_token_store(self._traintfr.get_token_store())
        self._dbi.set_dev_token_store(self._devtfr.get_token_store())
        self._dbi.set_test_token_store(self._testtfr.get_token_store())
        self._dbi.set_train_annotation_store(self._trainafr.get_annotation_store())
        self._dbi.set_dev_annotation_store(self._devafr.get_annotation_store())
        self._dbi.set_test_annotation_store(self._testafr.get_annotation_store())
        self._dbi.set_apt_report_store(self._arr.get_apt_report_store())
        self._dbi.db_inject()
    # </editor-fold>


if __name__ == "__main__":
    Client()
