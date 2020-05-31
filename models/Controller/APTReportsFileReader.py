# <editor-fold desc="Import Typing">
import multiprocessing
import re
from typing import *
# </editor-fold>
# <editor-fold desc="Import RX">
from PyPDF2 import PdfFileReader
from rx import from_list
from rx.operators import map, filter, to_list, flat_map, observe_on
# </editor-fold>
# <editor-fold desc="Import Other Libraries">
import os
import PyPDF2
# </editor-fold>

# <editor-fold desc=" Import Own Classes">
from rx.scheduler import ThreadPoolScheduler

from models.Model.APTReport import APTReport
# </editor-fold>


# noinspection PyMethodMayBeStatic
class APTReportFileReader:

    # <editor-fold desc="Constructor">
    def __init__(self):
        self._apt_report_store: List[APTReport] = self._setup_apt_report_store()

    # </editor-fold>

    # <editor-fold desc="Public interface">
    def get_apt_report_store(self) -> List[APTReport]:
        return self._apt_report_store

    # </editor-fold>

    # <editor-fold desc="Setup methods">
    def _setup_apt_report_store(self) -> List[APTReport]:

        def _get_file_names(path) -> List[str]:
            output: List[str] = []
            for root, dirs, files in os.walk(path):
                for file in files:
                    output = output + [os.path.join(root, file)]
            return output

        def y(apt_report_file, page_number, apt_report_file_name):
            print(apt_report_file_name + "_Page_" + str(page_number))
            return apt_report_file.getPage(page_number).extractText()

        def _get_apt_report_list(apt_report_file_name: str) -> List[Tuple[str, str]]:
            try:
                apt_report_file: PdfFileReader = PyPDF2.PdfFileReader(apt_report_file_name)
                if not apt_report_file.isEncrypted:
                    file_name_apt_report_list: List[Tuple[str, str]] = (
                        from_list(range(0, len(apt_report_file.pages)))
                        .pipe(map(
                            lambda page_number:
                            (
                                re.sub("\.\./\.\./data/APTReports/", "", apt_report_file_name)
                                + "_Page_"
                                + str(page_number),
                                y(apt_report_file, page_number, apt_report_file_name)
                            )
                        ), observe_on(pool_scheduler))
                        .pipe(to_list())
                        .run()
                    )
                    return file_name_apt_report_list
                else:
                    print("Encrypted!")
                    return []
            except Exception as e:
                print(e)
                print(type(e))
                print(e.args)
                return []

        optimal_thread_count = multiprocessing.cpu_count() + 1
        pool_scheduler = ThreadPoolScheduler(optimal_thread_count)
        apt_report_store: List[APTReport] = (
            from_list(
                [".pdf"]
            )
            .pipe(flat_map(
                lambda extension:
                from_list(
                    _get_file_names("../../data/APTReports")
                )
                .pipe(filter(
                    lambda apt_report_file_name: apt_report_file_name.endswith(extension)
                ))
            ))
            .pipe(flat_map(
                lambda apt_report_file_name: from_list(_get_apt_report_list(apt_report_file_name=apt_report_file_name))
            ))
            .pipe(map(
                lambda file_name_apt_report_tuple: APTReport(
                    apt_report_file_name=file_name_apt_report_tuple[0],
                    apt_report_data=file_name_apt_report_tuple[1]
                )
            ))
            .pipe(to_list())
            .run()
        )
        return apt_report_store
    # </editor-fold>
