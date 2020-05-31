class APTReport:

    # <editor-fold desc="Constructor">
    def __init__(self, apt_report_file_name: str, apt_report_data: str):
        self._apt_report_file_name: str = apt_report_file_name
        self._apt_report_data: str = apt_report_data

    # </editor-fold>

    # <editor-fold desc="Public interface">
    def get_apt_report_file_name(self) -> str:
        return self._apt_report_file_name

    def get_apt_report_data(self) -> str:
        return self._apt_report_data

    # </editor-fold>
