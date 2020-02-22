import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

from core.config.app_config import email
from core.util.pdf_util import PdfUtil


class ReportService(object):
    def __init__(self):
        pass

    def get_report_file(self, report_detail):
        pdf_util = PdfUtil(report_detail)
        return pdf_util.generate_report()

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
