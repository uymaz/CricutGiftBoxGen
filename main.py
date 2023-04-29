# This is a sample Python script.

import sys

from dataclasses import dataclass
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QDoubleValidator, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QMessageBox, \
    QFileDialog, QHBoxLayout, QFrame


class QHLine(QFrame):
    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)


@dataclass
class Line:
    x1: float
    y1: float
    x2: float
    y2: float


class TemplateGen:
    MM_TO_CRICUT = 2.8466666666666666666666666666667

    def __init__(self, length: float, width: float, height: float, margin: float, filename: str):
        self.filename = filename
        self.length = length * self.MM_TO_CRICUT
        self.width = width * self.MM_TO_CRICUT
        self.height = height * self.MM_TO_CRICUT
        self.cut_vertices = []
        self.fold_vertices = []
        self.margin = margin



    def generate_parameters(self):
        #make configurable
        self.join = self.length / 2.5
        self.e = self.width / 4.0
        self.f = self.length / 2.0
        self.a = self.width / 2.0
        self.b = (self.length - self.join) / 2.0
        self.c = self.width / 2.0
        self.d = self.b
        self.tuck = self.height / 5.0
        self.glue_tab = self.length / 5.0
        self.k = self.c + self.e - self.d

    # generate all vertices defined by the template dimensions

    def generate_cut_lines(self):
        lines = []

        # top lines
        upper_left_margin_line_top_left = Line(self.f,
                                               self.f * 2.0,
                                               self.f + self.margin,
                                               self.f * 2.0)

        upper_left_margin_line_top_right = Line(self.f + self.width - self.margin,
                                                self.f * 2.0,
                                                self.f + self.width,
                                                self.f * 2.0)

        upper_right_margin_line_top_left = Line(self.f + self.width + self.length,
                                                self.f * 2.0,
                                                self.f + self.width + self.length + self.margin,
                                                self.f * 2.0)

        upper_right_margin_line_top_right = Line(self.f + (self.width * 2.0) + self.length - self.margin,
                                                 self.f * 2.0,
                                                 self.f + (self.width * 2.0) + self.length,
                                                 self.f * 2.0)

        upper_line_top_left = Line(self.f + self.margin,
                                   self.f,
                                   self.f + self.width - self.margin,
                                   self.f)

        upper_line_top_middle = Line(self.f + self.width,
                                     self.f * 2.0,
                                     self.f + self.width + self.length,
                                     self.f * 2.0)

        upper_line_top_right = Line(self.f + self.width + self.length + self.margin,
                                    self.f,
                                    self.f + (self.width * 2.0) + self.length - self.margin,
                                    self.f)

        t_line = Line(self.f + (self.width * 2.0) + self.length,
                      (self.f * 2.0) - self.width - self.tuck,
                      self.f + (self.width * 2.0) + (self.length * 2.0),
                      (self.f * 2.0) - self.width - self.tuck)

        g_line = Line(self.f + (self.width * 2.0) + (self.length * 2.0),
                      (self.f * 2.0),
                      self.f + (self.width * 2.0) + (self.length * 2.0) + self.glue_tab,
                      (self.f * 2.0))

        # side lines
        left_line = Line(self.f,
                         self.f * 2.0,
                         self.f,
                         self.f * 2.0 + self.height)
        left_margin_line_left = Line(self.f + self.margin,
                                     self.f * 2.0,
                                     self.f + self.margin,
                                     self.f)
        right_margin_line_left = Line(self.f + self.width - self.margin,
                                      self.f * 2.0,
                                      self.f + self.width - self.margin,
                                      self.f)

        left_margin_line_right = Line(self.f + self.width + self.length + self.margin,
                                      self.f * 2.0,
                                      self.f + self.width + self.length + self.margin,
                                      self.f)

        right_margin_line_right = Line(self.f + (self.width * 2.0) + self.length - self.margin,
                                       self.f * 2.0,
                                       self.f + (self.width * 2.0) + self.length - self.margin,
                                       self.f)

        left_line_back = Line(self.f + (self.width * 2.0) + self.length,
                              self.f * 2.0,
                              self.f + (self.width * 2.0) + self.length,
                              self.f * 2.0 - self.width - self.tuck)

        right_line_back = Line(self.f + (self.width * 2.0) + (self.length * 2.0),
                               self.f * 2.0,
                               self.f + (self.width * 2.0) + (self.length * 2.0),
                               self.f * 2.0 - self.width - self.tuck)

        right_line_glue_tab = Line(self.f + (self.width * 2.0) + (self.length * 2.0) + self.glue_tab,
                                   self.f * 2.0,
                                   self.f + (self.width * 2.0) + (self.length * 2.0) + self.glue_tab,
                                   self.f * 2.0 + self.height)

        e_line_back = Line(self.f + (self.width * 2.0) + (self.length * 2.0) - self.b,
                           self.f * 2.0 + self.height + self.c,
                           self.f + (self.width * 2.0) + (self.length * 2.0) - self.b,
                           self.f * 2.0 + self.height + self.c + self.e)

        c_line_back = Line(self.f + (self.width * 2.0) + self.length + self.b,
                           self.f * 2.0 + self.height + self.c,
                           self.f + (self.width * 2.0) + self.length + self.b,
                           self.f * 2.0 + self.height + self.c + self.e)

        a_line_left = Line(self.f,
                           self.f * 2.0 + self.height,
                           self.f,
                           self.f * 3.0 + self.height)

        k_line_left = Line(self.f + self.a,
                           self.f * 2.0 + self.height + self.d,
                           self.f + self.a,
                           self.f * 3.0 + self.height)

        d_line_middle_left = Line(self.f + self.width - self.margin,
                                  self.f * 2.0 + self.height,
                                  self.f + self.width - self.margin,
                                  self.f * 2.0 + self.height + self.f)

        d_line_middle_right = Line(self.f + self.width + self.length + self.margin,
                                   self.f * 2.0 + self.height,
                                   self.f + self.width + self.length + self.margin,
                                   self.f * 2.0 + self.height + self.f)

        e_line_middle_left = Line(self.f + self.width + self.b,
                                  self.f * 3.0 + self.height - self.e,
                                  self.f + self.width + self.b,
                                  self.f * 3.0 + self.height)

        e_line_middle_right = Line(self.f + self.width + self.b + self.join,
                                   self.f * 3.0 + self.height - self.e,
                                   self.f + self.width + self.b + self.join,
                                   self.f * 3.0 + self.height)

        k_line_right = Line(self.f + self.width + self.length + self.a,
                            self.f * 2.0 + self.height + self.d,
                            self.f + self.width + self.length + self.a,
                            self.f * 3.0 + self.height)

        c_line_right = Line(self.f + (self.width * 2.0) + self.length - self.margin,
                            self.f * 2.0 + self.height,
                            self.f + (self.width * 2.0) + self.length - self.margin,
                            self.f * 3.0 + self.height)

        # diagonal lines
        diagonal_e_line_back = Line(self.f + (self.width * 2.0) + (self.length * 2.0),
                                    self.f * 2.0 + self.height,
                                    self.f + (self.width * 2.0) + (self.length * 2.0) - self.b,
                                    self.f * 2.0 + self.height + self.c)

        diagonal_c_line_back = Line(self.f + (self.width * 2.0) + self.length - self.margin,
                                    self.f * 2.0 + self.height,
                                    self.f + (self.width * 2.0) + self.length + self.b,
                                    self.f * 2.0 + self.height + self.c)

        diagonal_d_line_right = Line(self.f + self.width + self.length + self.margin,
                                     self.f * 2.0 + self.height,
                                     self.f + self.width + self.length + self.a,
                                     self.f * 2.0 + self.height + self.d)

        diagonal_d_line_left = Line(self.f + self.width - self.margin,
                                    self.f * 2.0 + self.height,
                                    self.f + self.width - self.a,
                                    self.f * 2.0 + self.height + self.d)

        # bottom lines
        bottom_a_line_left = Line(self.f,
                                  self.f * 3.0 + self.height,
                                  self.f + self.a,
                                  self.f * 3.0 + self.height)

        bottom_b_line_left = Line(self.f + self.width - self.margin,
                                  self.f * 3.0 + self.height,
                                  self.f + self.width + self.b,
                                  self.f * 3.0 + self.height)

        bottom_b_line_right = Line(self.f + self.width + self.length - self.b,
                                   self.f * 3.0 + self.height,
                                   self.f + self.width + self.length + self.margin,
                                   self.f * 3.0 + self.height)

        bottom_a_line_right = Line(self.f + self.width + self.length + self.a,
                                   self.f * 3.0 + self.height,
                                   self.f + (self.width * 2.0) + self.length - self.margin,
                                   self.f * 3.0 + self.height)

        bottom_j_line_upper = Line(self.f + self.width + self.b,
                                   self.f * 3.0 + self.height - self.e,
                                   self.f + self.width + self.length - self.b,
                                   self.f * 3.0 + self.height - self.e)

        bottom_j_line_lower = Line(self.f + (self.width * 2.0) + self.length + self.b,
                                   self.f * 2.0 + self.height + self.c + self.e,
                                   self.f + (self.width * 2.0) + self.length + self.b + self.join,
                                   self.f * 2.0 + self.height + self.c + self.e)

        bottom_g_line = Line(self.f + (self.width * 2.0) + (self.length * 2.0),
                             self.f * 2.0 + self.height,
                             self.f + (self.width * 2.0) + (self.length * 2.0) + self.glue_tab,
                             self.f * 2.0 + self.height)

        # append lines
        lines.append(upper_line_top_left)
        lines.append(upper_line_top_middle)
        lines.append(upper_line_top_right)
        lines.append(t_line)
        lines.append(upper_left_margin_line_top_left)
        lines.append(upper_left_margin_line_top_right)
        lines.append(g_line)
        lines.append(left_line)
        lines.append(left_margin_line_left)
        lines.append(right_margin_line_left)
        lines.append(left_margin_line_right)
        lines.append(right_margin_line_right)
        lines.append(upper_right_margin_line_top_left)
        lines.append(upper_right_margin_line_top_right)
        lines.append(left_line_back)
        lines.append(right_line_back)
        lines.append(e_line_middle_left)
        lines.append(e_line_middle_right)
        lines.append(diagonal_d_line_left)
        lines.append(diagonal_d_line_right)
        lines.append(right_line_glue_tab)
        lines.append(e_line_back)
        lines.append(c_line_back)
        lines.append(k_line_right)
        lines.append(c_line_right)
        lines.append(d_line_middle_left)
        lines.append(d_line_middle_right)
        lines.append(diagonal_e_line_back)
        lines.append(diagonal_c_line_back)
        lines.append(diagonal_d_line_right)
        lines.append(diagonal_d_line_left)
        lines.append(bottom_a_line_left)
        lines.append(bottom_b_line_left)
        lines.append(bottom_b_line_right)
        lines.append(bottom_a_line_right)
        lines.append(bottom_j_line_upper)
        lines.append(bottom_j_line_lower)
        lines.append(bottom_g_line)
        lines.append(a_line_left)
        lines.append(k_line_left)
        lines.append(e_line_middle_left)
        lines.append(e_line_middle_right)

        return lines

    def generate_fold_lines(self):
        lines = []

        # left rectangle
        upper_line_left = Line(self.f + self.margin,
                               self.f * 2.0,
                               self.f + self.width - self.margin,
                               self.f * 2.0)
        right_line_left = Line(self.f + self.width - self.margin,
                               self.f * 2.0,
                               self.f + self.width - self.margin,
                               self.f * 2.0 + self.height)
        lower_line_left = Line(self.f + self.width,
                               self.f * 2.0 + self.height,
                               self.f,
                               self.f * 2.0 + self.height)

        # front rectangle

        bottom_line_front = Line(self.f + self.width,
                                 self.f * 2.0 + self.height,
                                 self.f + self.width + self.length,
                                 self.f * 2.0 + self.height)

        right_line_front = Line(self.f + self.width + self.length + self.margin,
                                self.f * 2.0,
                                self.f + self.width + self.length + self.margin,
                                self.f * 2.0 + self.height)

        # right rectangle
        upper_line_right = Line(self.f + self.width + self.length + self.margin,
                                self.f * 2.0,
                                self.f + (self.width * 2.0) + self.length - self.margin,
                                self.f * 2.0)
        right_line_right = Line(self.f + (self.width * 2.0) + self.length - self.margin,
                                self.f * 2.0,
                                self.f + (self.width * 2.0) + self.length - self.margin,
                                self.f * 2.0 + self.height)
        bottom_line_right = Line(self.f + (self.width * 2.0) + self.length,
                                 self.f * 2.0 + self.height,
                                 self.f + self.width + self.length,
                                 self.f * 2.0 + self.height)

        # back rectangle
        top_line_back = Line(self.f + (self.width * 2.0) + self.length,
                             self.f * 2.0,
                             self.f + (self.width * 2.0) + (self.length * 2.0),
                             self.f * 2.0)
        bottom_line_back = Line(self.f + (self.width * 2.0) + self.length,
                                self.f * 2.0 + self.height,
                                self.f + (self.width * 2.0) + (self.length * 2.0),
                                self.f * 2.0 + self.height)
        right_line_back = Line(self.f + (self.width * 2.0) + (self.length * 2.0),
                               self.f * 2.0,
                               self.f + (self.width * 2.0) + (self.length * 2.0),
                               self.f * 2.0 + self.height)

        t_line = Line(self.f + (self.width * 2.0) + self.length,
                      (self.f * 2.0) - self.width,
                      self.f + (self.width * 2.0) + (self.length * 2.0),
                      (self.f * 2.0) - self.width)

        # append all lines to lines
        lines.append(upper_line_left)
        lines.append(right_line_left)
        lines.append(lower_line_left)
        lines.append(bottom_line_front)
        lines.append(right_line_front)
        lines.append(upper_line_right)
        lines.append(right_line_right)
        lines.append(bottom_line_right)
        lines.append(top_line_back)
        lines.append(bottom_line_back)
        lines.append(right_line_back)
        lines.append(t_line)

        return lines

    def write_header(self):
        with open(self.filename, 'w') as f:
            viewbox_x = self.f * 2.0 + self.width * 2.0 + self.length * 2.0
            viewbox_y = self.height * 3.5

            f.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
            f.write('<svg baseProfile=\'full\' viewBox="0 0 {} {}" id="templatemaker-giftbox" '.format(viewbox_x,
                                                                                                       viewbox_y))
            f.write('xmlns="http://www.w3.org/2000/svg">\n<title>Gizem\'s Template</title>')

    def write_footer(self):
        with open(self.filename, 'a') as f:
            f.write('</svg>\n')

    def write_fold(self):
        with open(self.filename, 'a') as f:
            f.write(
                '<g id="page-fold" class="fold" fill=\'none\' stroke=\'#333333\' stroke-width=\'0.75\' stroke-dasharray="4" >')

            fold_lines = self.generate_fold_lines()
            for line in fold_lines:
                f.write('<line x1="{}" y1="{}" x2="{}" y2="{}" />\n'.format(line.x1, line.y1, line.x2, line.y2))

            f.write('</g>')

    def write_cut(self):
        with open(self.filename, 'a') as f:
            f.write('<g id="page-cut" class="cut" fill=\'none\' stroke=\'#000000\' stroke-width=\'1\' >')

            cut_lines = self.generate_cut_lines()
            for line in cut_lines:
                f.write('<line x1="{}" y1="{}" x2="{}" y2="{}" />\n'.format(line.x1, line.y1, line.x2, line.y2))

            f.write('</g>')

    def write_svg(self):
        self.generate_parameters()

        self.write_header()
        self.write_fold()
        self.write_cut()
        self.write_footer()

        # show the result


class TemplateGenGUI:

    def __init__(self):
        app = QApplication(sys.argv)
        self.window = QWidget()
        self.window.setWindowTitle('Template Generator')
        self.window.setGeometry(100, 100, 280, 80)

        self.window.setWindowIcon(QIcon("ico/Giftbox.svg"))

        self.window.move(60, 15)
        self.layout = QVBoxLayout()

        # create three lineedits for length, width, height
        self.length_label = QLabel('Length in mm:')
        self.length_input = QLineEdit()
        self.length_input.setValidator(QDoubleValidator())

        self.width_label = QLabel('Width in mm:')
        self.width_input = QLineEdit()
        self.width_input.setValidator(QDoubleValidator())

        self.height_label = QLabel('Height in mm:')
        self.height_input = QLineEdit()
        self.height_input.setValidator(QDoubleValidator())

        self.margin_label = QLabel('Margin:')
        self.margin_input = QLineEdit()
        self.margin_input.setValidator(QDoubleValidator())
        self.margin_input.setPlaceholderText('Default: 5.0')

        self.btn = QPushButton('Create Template', self.window)
        self.btn.clicked.connect(self.prepare_and_run_generator)

        # filename choose
        self.file_name_label = QLabel('File name:')
        self.file_name_input = QLineEdit()
        self.file_name_input.setValidator(QRegExpValidator(QRegExp('[a-zA-Z0-9_]+')))

        # path to save in choose with qfiledialog
        self.path_label = QLabel('Path:')
        self.path_input = QLineEdit()
        self.path_input.setValidator(QRegExpValidator(QRegExp('[a-zA-Z0-9_]+')))
        self.path_btn = QPushButton('Choose path', self.window)
        self.path_btn.clicked.connect(self.choose_path)

        self.layout.addWidget(self.length_label)
        self.layout.addWidget(self.length_input)
        self.layout.addWidget(self.width_label)
        self.layout.addWidget(self.width_input)
        self.layout.addWidget(self.height_label)
        self.layout.addWidget(self.height_input)
        self.layout.addWidget(self.margin_label)
        self.layout.addWidget(self.margin_input)

        self.layout.addWidget(QHLine())

        self.layout.addWidget(self.file_name_label)
        self.layout.addWidget(self.file_name_input)

        self.layout.addWidget(self.path_label)

        self.path_layout = QHBoxLayout()

        self.path_layout.addWidget(self.path_input)
        self.path_layout.addWidget(self.path_btn)

        self.layout.addLayout(self.path_layout)

        self.layout.addWidget(self.btn)
        self.window.setLayout(self.layout)
        self.window.show()

        sys.exit(app.exec_())

    def choose_path(self):
        path = QFileDialog.getExistingDirectory(self.window, 'Choose path')
        self.path_input.setText(path)

    def prepare_and_run_generator(self):


        if self.length_input.text() == '' or self.width_input.text() == '' or self.height_input.text() == '':
            self.show_error_message('Please enter all dimensions')
            return

        if self.margin_input.text() == '':
            margin = 5.0
        else:
            margin = float(self.margin_input.text())

        length = float(self.length_input.text())
        width = float(self.width_input.text())
        height = float(self.height_input.text())

        if length <= 0 or width <= 0 or height <= 0:
            self.show_error_message('Please enter positive values')
            return

        if length > 1000 or width > 1000 or height > 1000:
            self.show_error_message('Please enter values below 1000')
            return

        self.filename = self.file_name_input.text()
        if self.filename == '':
            self.filename = 'template'

        path = self.path_input.text()
        if path == '':
            path = '.'
        else:
            path = path

        self.filename = path + '/' + self.filename + '.svg'

        generator = TemplateGen(length, width, height, margin, self.filename)
        generator.write_svg()
        self.show_success_message('Template created')

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle('Error')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_success_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle('Success')
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gui = TemplateGenGUI()

    # generate a pyqt5 gui

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
