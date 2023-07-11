import matplotlib
import numpy as np
import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar

step=0.1

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        loader = QUiLoader()
        self.setWindowTitle('Set Matplotlib Chart Value with QLineEdit Widget')
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QHBoxLayout()
        vlayout = QVBoxLayout()
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

        self.draw = QPushButton()
        self.draw.setText("Draw")
        self.draw.clicked.connect(self.update_chart)

        vlayout.addWidget(self.input_function)

        hLayout =QHBoxLayout()
        hLayout.addWidget(self.input_start)
        hLayout.addWidget(self.input_end)
        hLayout.setContentsMargins(100,0,100,0)
        hLayout.setSpacing(30)

        vlayout.addLayout(hLayout)
        vlayout.addWidget(self.draw)
        layout.addLayout(vlayout)

        self.canvas = FigureCanvas(plt.Figure(figsize=(15, 6)))
        toolbar = NavigationToolbar(self.canvas, self)

        vlayout2 = QVBoxLayout()
        vlayout2.addWidget(toolbar)
        vlayout2.addWidget(self.canvas)

        layout.addLayout(vlayout2)

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

    def update_chart(self):
        value = self.input_function.text()
        start = int(self.input_start.text())
        end = int(self.input_end.text())
        x,y = self.graphCalc(start,end)

        if self.plot:
            del self.plot[0]
        self.plot = self.axes.plot(x, y, color='g')
        print(self.plot)
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
        function = self.input_function.text().replace("^", "**")
        return eval(function)

    def graphCalc(self,start,end):
        x_res=[]
        y_res=[]
        for i in np.arange(start,end+step,step):
            x_res.append(i)
            y_res.append(self.evaluate(i))
        return x_res,y_res

if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')

    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

