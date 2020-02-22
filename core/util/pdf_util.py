import collections
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from core.util.report_img_util import get_img_path


class PdfUtil(object):
    HEIGHT, WIDTH = A4
    SIDE_MARGIN = 10 * mm
    MIDDLE_MARGIN = 5 * mm
    FULL_CONTENT_LENGTH = WIDTH - 2 * SIDE_MARGIN
    HALF_CONTENT_LENGTH = (WIDTH - 2 * SIDE_MARGIN - MIDDLE_MARGIN) / 2
    RIGHT_CONTENT_MARGIN = (WIDTH + MIDDLE_MARGIN) / 2

    ICON_SIZE = (32.625 * mm, 22.5 * mm)

    MEASUREMENT = {
        "left": {
            'margin': SIDE_MARGIN,
            'center_left': (HALF_CONTENT_LENGTH - ICON_SIZE[0]) / 4 + SIDE_MARGIN + ICON_SIZE[0],
            'center_right': 3 * (HALF_CONTENT_LENGTH - ICON_SIZE[0]) / 4 + SIDE_MARGIN + ICON_SIZE[0],
        },
        "right": {
            'margin': RIGHT_CONTENT_MARGIN,
            'center_left': (HALF_CONTENT_LENGTH - ICON_SIZE[0]) / 4 + RIGHT_CONTENT_MARGIN + ICON_SIZE[0],
            'center_right': 3 * (HALF_CONTENT_LENGTH - ICON_SIZE[0]) / 4 + RIGHT_CONTENT_MARGIN + ICON_SIZE[0],
        }
    }

    def __init__(self, report_detail):
        self.report_detail = report_detail
        self.report = report_detail.report
        self.user = self.report.user
        self.canvas = None

    def generate_report(self):
        file_path = self.__get_report_file_name()
        report_name = os.path.basename(file_path)
        self.canvas = canvas.Canvas(file_path, pagesize=(self.WIDTH, self.HEIGHT))
        self.canvas.setTitle(report_name)
        self.canvas.setAuthor('G42 Bike Fitting')
        self.__process_page1()
        self.__process_page2()
        self.__process_page3()
        self.__process_page4()
        self.__process_page5()
        self.__process_page6()
        self.__process_page7()

        self.canvas.save()
        return file_path

    def __process_page1(self):
        # header personal bike report
        self.__draw_header()
        # logo
        img_margin = (self.WIDTH - 230 * mm) / 2
        self.canvas.drawImage('static/img/logo.png', img_margin, self.__get_height(80), 230 * mm, 48 * mm)
        # user name and time
        self.__set_fill_color(102, 177, 255)
        self.canvas.setFont('Helvetica', 18)
        self.canvas.drawCentredString(self.WIDTH / 2, self.__get_height(135), self.user.name)
        self.__set_fill_color(156, 65, 87)
        self.canvas.setFont('Helvetica', 14)
        format_time = self.report.create_time.strftime('%Y-%m-%d %H:%M:%S')
        self.canvas.drawCentredString(self.WIDTH / 2, self.__get_height(150), format_time)
        self.canvas.showPage()

    def __process_page2(self):
        # header and title
        self.__draw_header()
        self.__draw_title('Personal Information')
        # left rider info
        self.__draw_cell_title(self.SIDE_MARGIN, self.__get_height(60), self.HALF_CONTENT_LENGTH, 'RIDER')

        rider_info = collections.OrderedDict()
        rider_info['Name:'] = self.user.name
        rider_info['Age:'] = str(self.user.age)
        rider_info['Gender:'] = 'Male' if self.user.gender == 1 else 'Female'
        rider_info['Phone:'] = self.user.phone
        rider_info['Email:'] = self.user.email
        self.__draw_cell_content(rider_info, self.SIDE_MARGIN, self.__get_height(70))

        # right bike info
        self.__draw_cell_title(self.RIGHT_CONTENT_MARGIN, self.__get_height(60), self.HALF_CONTENT_LENGTH, 'BIKE')

        bike_info = collections.OrderedDict()
        bike_info['Model:'] = self.report_detail.model
        bike_info['Size:'] = self.report_detail.size
        bike_info['Year:'] = str(self.report_detail.year)
        bike_info['Type:'] = self.report_detail.type
        self.__draw_cell_content(bike_info, self.RIGHT_CONTENT_MARGIN, self.__get_height(70))
        # footer
        self.__draw_footer(1)
        self.canvas.showPage()

    def __process_page3(self):
        self.__draw_header()
        self.__draw_title('Fit Report')
        self.__draw_cell_title(self.SIDE_MARGIN, self.__get_height(40), self.FULL_CONTENT_LENGTH, 'FIT ANGLES')
        self.__draw_footer(2)

        # measurement
        start_height = 43
        angles = self.report_detail.angles
        self.__draw_measurement('left', self.__get_height(start_height), angles['Ankle_Angle_Min'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Ankle_Angle_Max'], 'deg')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), angles['Ankle_Angle_Range'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Ankle_Angle_Bottom'], 'deg')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), angles['Ankle_Angle_Rear'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Ankle_Angle_Top'], 'deg')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), angles['Ankle_Angle_Forward'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Knee_Angle_Max'], 'deg')
        self.canvas.showPage()

    def __process_page4(self):
        self.__draw_header()
        self.__draw_footer(3)

        start_height = 15
        angles = self.report_detail.angles
        self.__draw_measurement('left', self.__get_height(start_height), angles['Knee_Angle_Min'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Knee_Angle_Range'], 'deg')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), angles['Hip_Angle_Min'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Hip_Angle_Max'], 'deg')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), angles['Back_From_Level'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Back_From_Level_Average'], 'deg')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), angles['Hip_Shoulder_Wrist'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Hip_Shoulder_Wrist_Average'], 'deg')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), angles['Hip_Shoulder_Elbow'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Hip_Shoulder_Elbow_Average'], 'deg')
        self.canvas.showPage()

    def __process_page5(self):
        self.__draw_header()
        self.__draw_footer(3)

        start_height = 15
        angles = self.report_detail.angles
        self.__draw_measurement('left', self.__get_height(start_height), angles['Elbow_Angle'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Elbow_Angle_Average'], 'deg')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), angles['Forearm_From_Level'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Forearm_From_Level_Average'], 'deg')

        start_height += 55
        self.__draw_cell_title(self.SIDE_MARGIN, self.__get_height(start_height), self.FULL_CONTENT_LENGTH,
                               'FIT ALIGNMENT')

        start_height += 5
        distance = self.report_detail.distances
        self.__draw_measurement('left', self.__get_height(start_height), distance['Knee_to_Foot_Forward'], 'mm')
        self.__draw_measurement('right', self.__get_height(start_height), distance['Knee_to_Foot_Lateral'], 'mm')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), distance['Hip_to_Foot_Lateral'], 'mm')
        self.__draw_measurement('right', self.__get_height(start_height), distance['Shoulder_to_Wrist_Lateral'], 'mm')
        self.canvas.showPage()

    def __process_page6(self):
        self.__draw_header()
        self.__draw_footer(4)

        start_height = 15
        angles = self.report_detail.angles
        distance = self.report_detail.distances
        self.__draw_measurement('left', self.__get_height(start_height), angles['Foot_From_Level'], 'deg')
        self.__draw_measurement('right', self.__get_height(start_height), angles['Foot_From_Level_Average'], 'deg')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), distance['Knee_Lateral_Travel'], 'mm')
        self.__draw_measurement('right', self.__get_height(start_height), distance['Hip_Vertical_Travel'], 'mm')

        start_height += 12 * mm
        self.__draw_measurement('left', self.__get_height(start_height), distance['Hip_Lateral_Travel'], 'mm')
        self.canvas.showPage()

    def __process_page7(self):
        self.__draw_header()
        self.__draw_footer(5)

        cur_height = 20
        self.__draw_cell_title(self.SIDE_MARGIN, self.__get_height(cur_height), self.FULL_CONTENT_LENGTH, 'MARKER PATH')
        note1 = "Note: Maker paths viewed from the front will be on the opposite side of the report. The paths representing the right side of the body will be shown"
        note2 = "on the left and vice versa. Green is downstroke and red is upstroke."
        cur_height += 6

        self.__set_fill_color(0, 0, 0)
        self.canvas.setFont('Helvetica', 12)
        self.canvas.drawString(self.SIDE_MARGIN + 2 * mm, self.__get_height(cur_height), note1)
        cur_height += 6
        self.canvas.drawString(self.SIDE_MARGIN + 2 * mm, self.__get_height(cur_height), note2)

        cur_height += 10
        self.canvas.drawString(self.SIDE_MARGIN, self.__get_height(cur_height), 'Front View of Knee Path')

        self.__set_stroke_color(200, 200, 200)
        self.canvas.setLineWidth(1)
        cur_height += 2
        self.canvas.line(self.SIDE_MARGIN, self.__get_height(cur_height),
                         self.SIDE_MARGIN + self.FULL_CONTENT_LENGTH, self.__get_height(cur_height))
        icon_img = "static/img/marker_path.png"
        knee_path_img = get_img_path(self.report_detail.knee_path_img)
        knee_path_size = (36 * mm, 64 * mm)

        icon_height = cur_height + (self.ICON_SIZE[1] / mm + 2)
        self.canvas.drawImage(icon_img, self.MEASUREMENT['left']['margin'], self.__get_height(icon_height),
                              self.ICON_SIZE[0],
                              self.ICON_SIZE[1])
        cur_height += knee_path_size[1] / mm + 2
        self.canvas.drawImage(knee_path_img, (self.WIDTH - knee_path_size[0]) / 2, self.__get_height(cur_height),
                              *knee_path_size)

        cur_height += 2
        self.__set_stroke_color(200, 200, 200)
        self.canvas.line(self.SIDE_MARGIN, self.__get_height(cur_height),
                         self.SIDE_MARGIN + self.FULL_CONTENT_LENGTH, self.__get_height(cur_height))

        self.canvas.showPage()

    def __draw_title(self, text):
        self.__set_fill_color(102, 177, 255)
        self.canvas.setFont('Helvetica-Bold', 20)
        self.canvas.drawCentredString(self.WIDTH / 2, self.__get_height(25), text)

    def __draw_cell_title(self, x, y, length, text):
        self.__set_fill_color(185, 219, 255)
        self.__set_stroke_color(185, 219, 255)
        self.canvas.rect(x, y, length, 6 * mm, fill=1)

        self.__set_fill_color(0, 0, 0)
        self.canvas.setFont('Helvetica-Bold', 12)
        self.canvas.drawString(x + 2 * mm, y + 1 * mm, text)

    def __draw_cell_content(self, content_dict, x, y):
        line_height = 8 * mm
        cur_height = y
        margin = x + 2 * mm
        for key, val in content_dict.items():
            self.__set_fill_color(0, 0, 0)
            self.canvas.setFont('Helvetica-Bold', 16)
            self.canvas.drawString(margin, cur_height, key)
            cur_height -= line_height
            self.canvas.setFont('Helvetica', 16)
            self.canvas.drawString(margin, cur_height, val)
            cur_height -= line_height

    def __get_height(self, h):
        return self.HEIGHT - h * mm

    def __get_mirror_x(self, x):
        return self.WIDTH - x * mm

    def __set_fill_color(self, r, g, b):
        self.canvas.setFillColorRGB(r / 255, g / 255, b / 255)

    def __set_stroke_color(self, r, g, b):
        self.canvas.setStrokeColorRGB(r / 255, g / 255, b / 255)

    def __get_report_file_name(self):
        report = self.report_detail.report
        report_name = "%s.pdf" % report.name
        file_path = os.path.join("static/report/pdf/", report_name)
        return os.path.abspath(file_path)

    def __draw_header(self):
        self.__set_fill_color(130, 130, 130)
        self.canvas.setFont('Helvetica', 10)
        self.canvas.drawString(self.SIDE_MARGIN, self.__get_height(6), 'Personal Bike Fitting Report')
        self.canvas.setLineWidth(1)
        self.__set_stroke_color(102, 177, 255)
        self.canvas.line(self.SIDE_MARGIN, self.__get_height(8), self.WIDTH - self.SIDE_MARGIN,
                         self.__get_height(8))

    def __draw_footer(self, page_num):
        self.__set_fill_color(167, 167, 167)
        self.canvas.setFont('Helvetica', 10)
        self.canvas.drawCentredString(self.WIDTH / 2, 3 * mm, str(page_num))

        footer_img_w = 28.75 * mm
        footer_img_h = 6 * mm
        img_margin = self.WIDTH - self.SIDE_MARGIN - footer_img_w
        self.canvas.drawImage('static/img/logo.png', img_margin, 2 * mm, footer_img_w, footer_img_h)

    def __draw_measurement(self, side, y, measure_dict, unit):
        cur_height = y
        line_height = 6 * mm

        self.canvas.setFont('Helvetica', 12)
        cur_height -= line_height
        self.__set_fill_color(0, 0, 0)
        self.canvas.drawString(self.MEASUREMENT[side]['margin'], cur_height, measure_dict['display_name'])
        self.__set_fill_color(153, 60, 83)
        self.canvas.drawCentredString(self.MEASUREMENT[side]['center_left'], cur_height, 'Left')
        self.__set_fill_color(28, 44, 191)
        self.canvas.drawCentredString(self.MEASUREMENT[side]['center_right'], cur_height, 'Right')

        self.__set_stroke_color(200, 200, 200)
        self.canvas.setLineWidth(1)
        cur_height -= 2 * mm
        self.canvas.line(self.MEASUREMENT[side]['margin'], cur_height,
                         self.MEASUREMENT[side]['margin'] + self.HALF_CONTENT_LENGTH, cur_height)
        img_path = "static/img/%s" % (measure_dict["img"])
        self.canvas.drawImage(img_path, self.MEASUREMENT[side]['margin'], cur_height - self.ICON_SIZE[1] - 2 * mm,
                              self.ICON_SIZE[0],
                              self.ICON_SIZE[1])

        self.__set_fill_color(0, 0, 0)
        cur_height -= line_height
        self.canvas.drawCentredString(self.MEASUREMENT[side]['center_left'], cur_height,
                                      self.__get_measure_str('Max Less', measure_dict["left_less_than_range"], unit))
        self.canvas.drawCentredString(self.MEASUREMENT[side]['center_right'], cur_height,
                                      self.__get_measure_str('Max Less', measure_dict["right_less_than_range"], unit))
        cur_height -= line_height
        self.canvas.drawCentredString(self.MEASUREMENT[side]['center_left'], cur_height,
                                      self.__get_measure_str('Current', measure_dict["left"], unit))
        self.canvas.drawCentredString(self.MEASUREMENT[side]['center_right'], cur_height,
                                      self.__get_measure_str('Current', measure_dict["right"], unit))
        cur_height -= line_height
        self.canvas.drawCentredString(self.MEASUREMENT[side]['center_left'], cur_height,
                                      self.__get_measure_str('Max More', measure_dict["left_more_than_range"], unit))
        self.canvas.drawCentredString(self.MEASUREMENT[side]['center_right'], cur_height,
                                      self.__get_measure_str('Max More', measure_dict["right_more_than_range"], unit))
        cur_height -= line_height
        self.canvas.drawCentredString(self.MEASUREMENT[side]['center_right'], cur_height,
                                      self.__get_range_str(measure_dict['good_range'], unit))
        cur_height -= 2 * mm
        self.__set_stroke_color(200, 200, 200)
        self.canvas.line(self.MEASUREMENT[side]['margin'], cur_height,
                         self.MEASUREMENT[side]['margin'] + self.HALF_CONTENT_LENGTH, cur_height)

    @staticmethod
    def __get_measure_str(key, val, unit):
        if val is None:
            val = '--'
            unit = ''
        elif unit == 'deg':
            unit = chr(176)
        else:
            unit = 'mm'
        return "%s: %s%s" % (key, val, unit)

    @staticmethod
    def __get_range_str(range_tuple, unit):
        if range_tuple is None or range_tuple[0] is None or range_tuple[1] is None:
            return "Range: -- to --"
        else:
            unit = chr(176) if unit == 'deg' else 'mm'
            return "Range: %s%s to %s%s" % (range_tuple[0], unit, range_tuple[1], unit)
