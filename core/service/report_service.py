import os
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from core.config.app_config import email


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

    def send_to_email(self, report_detail):
        report_path = self.get_report_file(report_detail)
        report = report_detail.report
        user = report.user
        context = ssl.create_default_context()

        msg = MIMEMultipart()
        msg['Subject'] = 'G42 Bike Fitting Report'
        msg['From'] = email['addr']
        msg['To'] = user.email

        pdf = MIMEApplication(open(report_path, 'rb').read())
        pdf.add_header('Content-Disposition', 'attachment', filename="{}.pdf".format(report.name))
        msg.attach(pdf)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(email['addr'], email['password'])
            server.sendmail(email['addr'], user.email, msg.as_string())  # 发送邮件

    def _get_report_file_name(self, report_detail):
        report = report_detail.report
        report_name = "%s.pdf" % report.name
        file_path = os.path.join("static/pdf/", report_name)
        return os.path.abspath(file_path)
