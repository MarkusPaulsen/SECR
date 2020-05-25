from models.Controller.APTReportsFileReader import APTReportFileReader
from models.Controller.AnnotationFileReader import AnnotationFileReader
from models.Controller.DBInjecter import DBInjecter
from models.Controller.TokenFileReader import TokenFileReader

# trainafr: AnnotationFileReader = AnnotationFileReader(base_folder="../../data/MalwareTextDB-2.0/data/train/annotations")
# devafr: AnnotationFileReader = AnnotationFileReader(base_folder="../../data/MalwareTextDB-2.0/data/dev/annotations")
# testafr: AnnotationFileReader = AnnotationFileReader(base_folder="../../data/MalwareTextDB-2.0/data/test_1/annotations")
# traintfr: TokenFileReader = TokenFileReader(base_folder="../../data/MalwareTextDB-2.0/data/train/tokenized")
# devtfr: TokenFileReader = TokenFileReader(base_folder="../../data/MalwareTextDB-2.0/data/dev/tokenized")
# testtfr: TokenFileReader = TokenFileReader(base_folder="../../data/MalwareTextDB-2.0/data/test_1/tokenized")
arr: APTReportFileReader = APTReportFileReader(base_folder="../../data/APTReports")
dbi: DBInjecter = DBInjecter()
# dbi.set_train_annotation_store(trainafr.get_annotation_store())
# dbi.set_dev_annotation_store(devafr.get_annotation_store())
# dbi.set_test_annotation_store(testafr.get_annotation_store())
# dbi.set_train_token_store(traintfr.get_token_store())
# dbi.set_dev_token_store(devtfr.get_token_store())
# dbi.set_test_token_store(testtfr.get_token_store())
dbi.set_apt_report_store(arr.get_apt_report_store())
dbi.db_inject()
