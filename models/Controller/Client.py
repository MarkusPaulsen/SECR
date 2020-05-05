from models.Controller.APTReportsFileReader import APTReportFileReader
from models.Controller.AnnotationFileReader import AnnotationFileReader
from models.Controller.DBInjecter import DBInjecter

afr: AnnotationFileReader = AnnotationFileReader()
arr: APTReportFileReader = APTReportFileReader()
dbi: DBInjecter = DBInjecter()
dbi.set_annotation_store(afr.get_annotation_store())
dbi.set_apt_report_store(arr.get_apt_report_store())
dbi.db_inject()
