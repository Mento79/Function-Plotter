import matplotlib
import numpy as np
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
import re

step=0.1
def validateFunction(inp):
    pattern = r'^(-?[0-9x]+[\+\-\*/\^])*-?[0-9x]+$' # Regular expression pattern
    if re.match(pattern, inp):
        return True
    else:
        return False
def validateLimits(inp):
    pattern = r'^(-?[1-9][0-9]*|0)$' # Regular expression pattern
    if re.match(pattern, inp):
        return True
    else:
        return False


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.setWindowTitle('Set Matplotlib Chart Value with QLineEdit Widget')
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QHBoxLayout()
        vLayout = QVBoxLayout()
        # layout.setContentsMargins(20,0,20,0)
        self.setLayout(layout)
        self.input_function = QLineEdit()
        self.input_function.setPlaceholderText("Function")

        self.input_start = QLineEdit()
        self.input_start.setFixedWidth(80)
        self.input_start.setPlaceholderText("Start")

        self.input_end = QLineEdit()
        self.input_end.setFixedWidth(80)
        self.input_end.setPlaceholderText("End")

        self.button_draw = QPushButton()
        self.button_draw.setText("Draw")
        self.button_draw.setFixedHeight(80)
        font = QtGui.QFont()
        font.setPointSize(30)
        self.button_draw.setFont(font)


        self.button_draw.clicked.connect(self.updatePlot)

        textVLayout = QVBoxLayout()
        textVLayout.addWidget(self.input_function)

        hLayout =QHBoxLayout()
        hLayout.addWidget(self.input_start)
        hLayout.addWidget(self.input_end)
        hLayout.setSpacing(15)

        textVLayout.addLayout(hLayout)
        vLayout.addLayout(textVLayout)
        vLayout.addSpacing(1000)
        vLayout.setContentsMargins(0,0,5,0)

        vLayout.addWidget(self.button_draw)
        layout.addLayout(vLayout)

        self.canvas = FigureCanvas(plt.Figure(figsize=(15, 7)))
        self.canvas.resize(1700,self.height())
        print(self.canvas.get_width_height())
        toolbar = NavigationToolbar(self.canvas, self)

        vLayout2 = QVBoxLayout()
        vLayout2.addWidget(toolbar)
        vLayout2.addWidget(self.canvas)

        layout.addLayout(vLayout2)

        self.insert_ax()

        # self.window=loader.load("app_v1.ui", self)
        # self.window.MplWidget = MatplotlibWidget(self.window.MplWidget)
        # self.window.MplWidget.setGeometry(QtCore.QRect(0, 0, self.window.MplWidget.width(),
        #                                     self.window.MplWidget.height()))  # Set the size and position of the widget
        # self.window.button_draw.clicked.connect(self.window.MplWidget.plotGraph)
        # self.window.show()

    def insert_ax(self):
        font = {
            'weight': 'normal',
            'size': 16
        }
        matplotlib.rc('font', **font)

        self.axes = self.canvas.figure.subplots()
        self.axes.set_ylim([0, 100])
        self.axes.set_xlim([0, 1])
        self.plotAxes()
        self.plot = None

    def updatePlot(self):
        function = self.input_function.text()
        start = self.input_start.text()
        end = self.input_end.text()
        if self.plot:
            self.axes.cla()
            self.plotAxes()
        if not self.validate(function,start,end):
            return
        x,y = self.graphCalc(int(start),int(end))
        if not x:
            return
        self.plot = self.axes.plot(x, y, color='g')

        self.canvas.draw()

    def plotAxes(self):
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
    def evaluate(self,x):
        try:
            function = self.input_function.text().replace("^", "**")
            return eval(function)
        except ZeroDivisionError :
            self.alert("Please don't divide by zero")
            return None
        except Exception as e:
            self.alert(e)
            return None


    def graphCalc(self,start,end):
        x_res=[]
        y_res=[]
        for i in np.arange(start,end+step,step):
            x_res.append(i)
            temp=self.evaluate(i)
            if temp:
                y_res.append(temp)
            else:
                return None,None
        return x_res,y_res

    def alert(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Can't Draw")
        dlg.setStyleSheet("QLabel{min-width: 300px;}");
        dlg.setText(message)
        button = dlg.exec_()
    def validate(self,function,start,end):
        if not validateFunction(function):
            self.alert("function should be consists of numbers and x's \nand between each two only one of these +,-,*,/,^")
            return False
        if start=="":
            self.alert("Please Enter start point")
            return False
        if end=="":
            self.alert("Please Enter start point")
            return False
        if not validateLimits(start):
            self.alert("Start point should be number")
            return False
        if not validateLimits(end):
            self.alert("End point should be number")
            return False
        if float(start)>float(end):
            self.alert("Start point should be less than or equal \nthe end point")
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

