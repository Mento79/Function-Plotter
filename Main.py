from functools import partial
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

        # hide the add button to add new one after the added function
        self.button_add[index - 1].setVisible(False)

        # create the new function boxes
        self.function_text_box_creation(index)
        self.start_and_end_box_creation(index, 68)
        self.remove_and_add_button_creation(index)

        # initialize the layouts
        button_add_layout = QVBoxLayout()
        new_function_layout = QHBoxLayout()
        function_box_layout = QVBoxLayout()
        function_text_box_layout = QHBoxLayout()
        start_and_end_layout = QHBoxLayout()

        # layout function text box and add it to the function box layout
        function_text_box_layout.addWidget(self.color_label[index])
        function_text_box_layout.addWidget(self.input_function[index])
        function_box_layout.addLayout(function_text_box_layout)

        # layout start and end text boxes and add it to the function box layout
        start_and_end_layout.addWidget(self.input_start[index])
        start_and_end_layout.addWidget(self.input_end[index])
        start_and_end_layout.setSpacing(10)
        function_box_layout.addLayout(start_and_end_layout)

        # here we use a new layout to add a remove button beside the text boxes
        new_function_layout.addLayout(function_box_layout)
        new_function_layout.addWidget(self.button_remove[index])

        # here we use a new layout too to the add button under the previous new layout
        button_add_layout.addLayout(new_function_layout)
        button_add_layout.addWidget(self.button_add[index])

        # hide the add button after we have 8 functions
        if len(self.input_function) == 8:
            self.button_add[index].setVisible(False)

        # add the new function to the main functions layout and add spacing
        # between the current function and the next one to be created
        self.function_layout.addLayout(button_add_layout)
        self.spacing.append(QSpacerItem(20, 20))
        self.function_layout.addItem(self.spacing[index])

    def remove_function(self, index):
        # remove the text boxes and the buttons of the removed function
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

        self.function_layout.removeItem(self.spacing[index])
        self.spacing.pop(index)

        # update the index of the rest functions
        for i in range(index, len(self.button_remove)):
            self.button_remove[i].clicked.disconnect()
            self.button_remove[i].clicked.connect(partial(self.remove_function, i))

        # update the color of the rest functions
        for i in range(index, len(self.color_label)):
            self.color_label[i].setText(f"<font color='{self.colors[i]}'>⬤</font>")

        # update the place of the add button
        if index == len(self.input_function):
            self.button_add[index - 1].setVisible(True)
        # visualize the add button if we have less than 8 functions
        if len(self.input_function) < 8:
            self.button_add[-1].setVisible(True)

    # this function is used to plot a new ploot every time the draw button is clicked
    def update_plot(self):

        # first we clear the previous axes and draw new one
        if self.plot:
            self.axes.cla()
            self.plot_axes()

        # we loop on every function added to draw it
        for i in range(len(self.input_function)):

            # we read the data from the text boxes of each function
            function = self.input_function[i].text()
            start = self.input_start[i].text()
            end = self.input_end[i].text()

            # first we validate the data we get from the text boxes
            if not self.validate(start, end, function, i, True):
                # if there are error clear the screen
                self.canvas.draw()
                return

            # second we calculate the y to all the points to be drawn
            x, y = self.points_maker(int(start), int(end), function, i)
            if not x:
                # if there are error clear the screen
                self.canvas.draw()
                return

            # if it is not the first function to be plotted append it to the previous ones
            if self.plot:
                self.plot.append(self.axes.plot(x, y, color=self.colors[i]))
            # else just plot it
            else:
                self.plot = self.axes.plot(x, y, color=self.colors[i])
        self.canvas.draw()

    def plot_axes(self):
        xmin, xmax, ymin, ymax = -100, 100, -100, 100

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

        # Draw major and minor grid lines
        self.axes.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)

        # Draw arrows
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

        # we calculate the y of each unit between start and end
        # the difference between every two succesive units are 0.1
        # we round the result to first three digits
        for i in np.arange(start, end + step, step):
            x_res.append(round(i, 3))
            temp = evaluate(self, i, function, index)
            if temp != None:
                y_res.append(round(temp, 3))
            else:
                return None, None
        return x_res, y_res

    # we use this function to display the error message as a new window on the screen
    def alert(self, message):
        self.dlg = QMessageBox(self)
        self.dlg.setWindowTitle("Can't Draw")
        self.dlg.setStyleSheet("QLabel{min-width: 300px;}")
        self.dlg.setText(message)
        self.dlg.exec_()

    def validate(self, start, end, function, index, alertbool):
        # check if the function matches the regex
        if not validate_function(function):
            if alertbool:
                self.alert(
                    f"function {index + 1} should be consists of numbers and x's \nand between each two only one of these +,-,*,/,^")
            return False
        # check if the start is empty
        if start == "":
            if alertbool:
                self.alert(f"Please Enter start point for function {index + 1}")
            return False
        # check if the end is empty
        if end == "":
            if alertbool:
                self.alert(f"Please Enter start point for function {index + 1}")
            return False
        # check if the start is a number
        if not validate_limits(start):
            if alertbool:
                self.alert(f"Start point of function {index + 1} should be a number")
            return False
        # check if the end is a number
        if not validate_limits(end):
            if alertbool:
                self.alert(f"End point of function {index + 1} should be a number")
            return False
        # check if start is more the end
        if float(start) > float(end):
            if alertbool:
                self.alert(f"Start point should be less than or equal \nthe end point for function {index + 1}")
            return False
        return True


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()
    app.exec_()
