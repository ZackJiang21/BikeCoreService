import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


class ReportService(object):
    def __init__(self):
        pass

    def get_report_file(self, report_detail):
        file_path = self._get_report_file_name(report_detail)
        c = canvas.Canvas(file_path, pagesize=A4)
        c.drawString(100, 100, "Hello World")
        c.showPage()
        c.save()
        return file_path

    def _get_report_file_name(self, report_detail):
        report = report_detail.report
        report_name = "%s.pdf" % report.name
        file_path = os.path.join("static/pdf/", report_name)
        return os.path.abspath(file_path)
