from models.Controller.AnnotationFileReader import AnnotationFileReader
from models.Controller.DBInjecter import DBInjecter

afr: AnnotationFileReader = AnnotationFileReader()
dbi: DBInjecter = DBInjecter()
dbi.set_annotation_store(afr.get_annotation_store())
dbi.db_inject()
