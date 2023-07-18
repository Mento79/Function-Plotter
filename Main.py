from functools import partial
import matplotlib
import numpy as np
import sys
from PySide2 import QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox, QSpacerItem, \
    QLabel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, \
    NavigationToolbar2QT as NavigationToolbar
import re

# Global variables
step = 0.1


# here we validate the function by comparing it to a regex
def validate_function(inp):
    pattern = r'^(-?[0-9x]+[\+\-\*/\^])*-?[0-9x]+$'
    if re.match(pattern, inp):
        return True
    else:
        return False


# here we validate the start and end by comparing it to a regex
def validate_limits(inp):
    pattern = r'^(-?[1-9][0-9]*|0)$'  # Regular expression pattern
    if re.match(pattern, inp):
        return True
    else:
        return False


# here we evaluate the y result of every point to be drawn
def evaluate(app, x, function, index):
    try:
        fun = function.replace("^", "**")
        return eval(fun)
    except ZeroDivisionError:
        app.alert(f"Please don't divide by zero in function {index + 1}")
        return None
    except Exception as e:
        app.alert(str(e))
        return None


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        # initialize variables
        self.button_draw = None
        loader = QUiLoader()
        self.colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'pink']
        self.input_function = []
        self.color_label = []
        self.input_start = []
        self.input_end = []
        self.button_add = []
        self.button_remove = []
        self.spacing = []
        index = 0
        
        # set window options 
        self.setWindowTitle('Set Matplotlib Chart Value with QLineEdit Widget')
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)

        # create first function boxes
        self.function_text_box_creation(index)
        self.start_and_end_box_creation(index, 80)
        self.remove_and_add_button_creation(index)
        self.draw_button_creation()

        # create the canvas and its toolbar
        self.canvas = FigureCanvas(plt.Figure(figsize=(15, 7)))
        toolbar = NavigationToolbar(self.canvas, self)

        # initialize the layouts
        app_layout = QHBoxLayout()
        side_bar_layout = QVBoxLayout()
        self.function_layout = QVBoxLayout()
        function_box_layout = QVBoxLayout()
        function_text_box_layout = QHBoxLayout()
        start_and_end_layout = QHBoxLayout()
        main_canvas_layout = QVBoxLayout()
        
        # set main app layout
        self.setLayout(app_layout)
        
        # layout function text box and add it to the function box layout
        function_text_box_layout.addWidget(self.color_label[index])
        function_text_box_layout.addWidget(self.input_function[index])
        function_box_layout.addLayout(function_text_box_layout)

        # layout start and end text boxes and add it to the function box layout
        start_and_end_layout.addWidget(self.input_start[index])
        start_and_end_layout.addWidget(self.input_end[index])
        start_and_end_layout.setSpacing(15)
        function_box_layout.addLayout(start_and_end_layout)
        
        # add button to function box layout
        function_box_layout.addWidget(self.button_add[index])
        
        # add the first function layout to the main function layout
        self.function_layout.addLayout(function_box_layout)
        self.spacing.append(QSpacerItem(20, 20))
        self.function_layout.addItem(self.spacing[index])
        
        # add the main function layout and the draw button to the sidebar layout and then add it to the app layout
        side_bar_layout.addLayout(self.function_layout)
        side_bar_layout.addStretch()
        side_bar_layout.setContentsMargins(0, 40, 5, 0)
        side_bar_layout.addWidget(self.button_draw)
        app_layout.addLayout(side_bar_layout)

        # add the canvas and its toolbar to the main canvas layout and then add it to the app layout
        main_canvas_layout.addWidget(toolbar)
        main_canvas_layout.addWidget(self.canvas)
        app_layout.addLayout(main_canvas_layout)

        # draw the main axis
        self.axes = self.canvas.figure.subplots()
        self.axes.set_ylim([0, 100])
        self.axes.set_xlim([0, 1])
        self.plot_axes()
        self.plot = None


    def function_text_box_creation(self, index):
        self.input_function.append(QLineEdit())
        self.input_function[index].setPlaceholderText("Function")

        self.color_label.append(QLabel(f"<font color='{self.colors[index]}'>⬤</font>"))
        color_font = self.color_label[index].font()
        color_font.setPointSize(15)
        self.color_label[index].setFont(color_font)

    def start_and_end_box_creation(self, index, size):
        self.input_start.append(QLineEdit())
        self.input_start[index].setFixedWidth(size)
        self.input_start[index].setPlaceholderText("Start")

        self.input_end.append(QLineEdit())
        self.input_end[index].setFixedWidth(size)
        self.input_end[index].setPlaceholderText("End")

    def remove_and_add_button_creation(self, index):
        self.button_remove.append(QPushButton())
        self.button_remove[index].setText("X")
        if index == 0:
            self.button_remove[index].setVisible(False)
        else:
            self.button_remove[index].setFixedWidth(20)
            self.button_remove[index].setFixedHeight(50)
            self.button_remove[index].clicked.connect(partial(self.remove_function, index))

        self.button_add.append(QPushButton())
        self.button_add[index].setText("Add")
        self.button_add[index].clicked.connect(self.add_function)

    def draw_button_creation(self):
        self.button_draw = QPushButton()
        self.button_draw.setText("Draw")
        self.button_draw.setFixedHeight(80)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.button_draw.setFont(font)
        self.button_draw.clicked.connect(self.update_plot)


    def add_function(self):
        index = len(self.input_function)
        button_add_layout = QVBoxLayout()
        new_function_layout = QHBoxLayout()
        function_box_layout = QVBoxLayout()

        self.button_add[index - 1].setVisible(False)

        self.function_text_box_creation(index)

        function_text_box_layout = QHBoxLayout()
        function_text_box_layout.addWidget(self.color_label[index])
        function_text_box_layout.addWidget(self.input_function[index])
        function_box_layout.addLayout(function_text_box_layout)

        self.start_and_end_box_creation(index, 68)

        start_and_end_layout = QHBoxLayout()
        start_and_end_layout.addWidget(self.input_start[index])
        start_and_end_layout.addWidget(self.input_end[index])
        start_and_end_layout.setSpacing(10)
        function_box_layout.addLayout(start_and_end_layout)

        new_function_layout.addLayout(function_box_layout)

        self.remove_and_add_button_creation(index)

        new_function_layout.addWidget(self.button_remove[index])

        button_add_layout.addLayout(new_function_layout)

        button_add_layout.addWidget(self.button_add[index])
        if len(self.input_function) == 8:
            self.button_add[index].setVisible(False)

        # self.function_layout.addSpacing(20)
        self.function_layout.addLayout(button_add_layout)
        self.spacing.append(QSpacerItem(20, 20))
        self.function_layout.addItem(self.spacing[index])

    def remove_function(self, index):
        self.input_function[index].deleteLater()
        self.input_function.pop(index)

        self.color_label[index].deleteLater()
        self.color_label.pop(index)

        self.input_start[index].deleteLater()
        self.input_start.pop(index)

        self.input_end[index].deleteLater()
        self.input_end.pop(index)

        self.button_add[index].deleteLater()
        self.button_add.pop(index)

        self.button_remove[index].deleteLater()
        self.button_remove.pop(index)

        # self.function_layout.removeItem(self.function_layout.itemAt(2*index))
        self.function_layout.removeItem(self.spacing[index])
        self.spacing.pop(index)

        # self.function_layout.itemAt(2 * index+1).deleteLater()
        # self.function_layout.itemAt(2 * index).deleteLater()
        for i in range(index, len(self.button_remove)):
            self.button_remove[i].clicked.disconnect()
            self.button_remove[i].clicked.connect(partial(self.remove_function, i))
        for i in range(index, len(self.color_label)):
            self.color_label[i].setText(f"<font color='{self.colors[i]}'>⬤</font>")
        if index == len(self.input_function):
            self.button_add[index - 1].setVisible(True)
        if len(self.input_function) < 8:
            self.button_add[-1].setVisible(True)

    def update_plot(self):

        if self.plot:
            self.axes.cla()
            self.plot_axes()
        for i in range(len(self.input_function)):
            function = self.input_function[i].text()
            start = self.input_start[i].text()
            end = self.input_end[i].text()
            if not self.validate(start, end, function, i, True):
                self.canvas.draw()
                return
            x, y = self.points_maker(int(start), int(end), function, i)
            if not x:
                self.canvas.draw()
                return
            if self.plot:
                self.plot.append(self.axes.plot(x, y, color=self.colors[i]))
            else:
                self.plot = self.axes.plot(x, y, color=self.colors[i])
        self.canvas.draw()

    def plot_axes(self):
        xmin, xmax, ymin, ymax = -100, 100, -100, 100
        ticks_frequency = 1

        # Set identical scales for both axes
        self.axes.set(xlim=(xmin - 1, xmax + 1), ylim=(ymin - 1, ymax + 1), aspect='equal')

        # Set bottom and left spines as x and y axes of coordinate system
        self.axes.spines['bottom'].set_position('zero')
        self.axes.spines['left'].set_position('zero')

        # Remove top and right spines
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)

        # Create 'x' and 'y' labels placed at the end of the axes
        self.axes.set_xlabel('x', size=14, labelpad=-24, x=1.03)
        self.axes.set_ylabel('y', size=14, labelpad=-21, y=1.02, rotation=0)

        # # Create custom major ticks to determine position of tick labels
        # x_ticks = np.arange(xmin, xmax + 1, 1)
        # y_ticks = np.arange(ymin, ymax + 1, 1)
        # self.axes.set_xticks(x_ticks[x_ticks != 0])
        # self.axes.set_yticks(y_ticks[y_ticks != 0])

        # Draw major and minor grid lines
        self.axes.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)

        # Draw arrows
        # arrow_fmt = dict(markersize=4, color='black', clip_on=False)
        # self.axes.plot((1), (0), marker='>', transform=self.axes.get_yaxis_transform(), **arrow_fmt)
        # self.axes.plot((-1), (0), marker='<', transform=self.axes.get_yaxis_transform(), **arrow_fmt)
        # self.axes.plot((0), (1), marker='^', transform=self.axes.get_xaxis_transform(), **arrow_fmt)
        # self.axes.plot((0), (-1), marker='v', transform=self.axes.get_xaxis_transform(), **arrow_fmt)

        arrow_fmt = dict(markersize=4, color='black', clip_on=False)
        self.axes.annotate("", xy=(xmax + 1, 0), xytext=(xmax + 0.9, 0),
                           arrowprops=dict(arrowstyle="->", linewidth=1.5), va='center',
                           ha='right')
        self.axes.annotate("", xy=(xmin - 1, 0), xytext=(xmin - 0.9, 0),
                           arrowprops=dict(arrowstyle="->", linewidth=1.5), va='center',
                           ha='right')
        self.axes.annotate("", xy=(0, ymax + 1), xytext=(0, ymax + 0.9),
                           arrowprops=dict(arrowstyle="->", linewidth=1.5), va='center',
                           ha='right')
        self.axes.annotate("", xy=(0, ymin - 1), xytext=(0, ymin - 0.9),
                           arrowprops=dict(arrowstyle="->", linewidth=1.5), va='center',
                           ha='right')

    def points_maker(self, start, end, function, index):
        x_res = []
        y_res = []
        for i in np.arange(start, end + step, step):
            x_res.append(round(i, 3))
            temp = evaluate(self, i, function, index)
            if temp != None:
                y_res.append(round(temp, 3))
            else:
                return None, None
        return x_res, y_res

    def alert(self, message):
        self.dlg = QMessageBox(self)
        self.dlg.setWindowTitle("Can't Draw")
        self.dlg.setStyleSheet("QLabel{min-width: 300px;}");
        self.dlg.setText(message)
        button = self.dlg.exec_()

    def validate(self, start, end, function, index, alertbool):
        if not validate_function(function):
            if alertbool:
                self.alert(
                    f"function {index + 1} should be consists of numbers and x's \nand between each two only one of these +,-,*,/,^")
            return False
        if start == "":
            if alertbool:
                self.alert(f"Please Enter start point for function {index + 1}")
            return False
        if end == "":
            if alertbool:
                self.alert(f"Please Enter start point for function {index + 1}")
            return False
        if not validate_limits(start):
            if alertbool:
                self.alert(f"Start point of function {index + 1} should be a number")
            return False
        if not validate_limits(end):
            if alertbool:
                self.alert(f"End point of function {index + 1} should be a number")
            return False
        if float(start) > float(end):
            if alertbool:
                self.alert(f"Start point should be less than or equal \nthe end point for function {index + 1}")
            return False
        return True


if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QtWidgets.QApplication(sys.argv)

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
