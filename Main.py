import matplotlib
import numpy as np

matplotlib.use('QtAgg')
# matplotlib.rcParams['backend.qt4']='PySide'

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MatplotlibWidget(FigureCanvas):

    def __init__(self, parent=None, xlabel='x', ylabel='y', title='Title'):
        super(MatplotlibWidget, self).__init__(Figure())

        self.setParent(parent)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.axes = self.figure.add_subplot(111)

        self.axes.set_xlabel(xlabel)
        self.axes.set_ylabel(ylabel)
        self.axes.set_title(title)


import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtUiTools import QUiLoader

loader = QUiLoader()
app = QtWidgets.QApplication(sys.argv)
window = loader.load("app_v1.ui", None)
# window.MplWidget = MatplotlibWidget()
mpl_widget = MatplotlibWidget(window.MplWidget)
mpl_widget.setGeometry(QtCore.QRect(0, 0, window.MplWidget.width(), window.MplWidget.height()))  # Set the size and position of the widget
window.show()


def plotDataPoints(self, x, y):
    self.axes.clear()

    self.axes.plot(x, y)

    xmin, xmax, ymin, ymax = -5, 5, -5, 5
    ticks_frequency = 1

    # Set identical scales for both axes
    self.axes.set(xlim=(xmin-1, xmax+1), ylim=(ymin-1, ymax+1), aspect='equal')

    # Set bottom and left spines as x and y axes of coordinate system
    self.axes.spines['bottom'].set_position('zero')
    self.axes.spines['left'].set_position('zero')

    # Remove top and right spines
    self.axes.spines['top'].set_visible(False)
    self.axes.spines['right'].set_visible(False)

    # Create 'x' and 'y' labels placed at the end of the axes
    self.axes.set_xlabel('x', size=14, labelpad=-24, x=1.03)
    self.axes.set_ylabel('y', size=14, labelpad=-21, y=1.02, rotation=0)

    # Create custom major ticks to determine position of tick labels
    x_ticks = np.arange(xmin, xmax + 1, 1)
    y_ticks = np.arange(ymin, ymax + 1, 1)
    self.axes.set_xticks(x_ticks[x_ticks != 0])
    self.axes.set_yticks(y_ticks[y_ticks != 0])

    # Draw major and minor grid lines
    self.axes.grid(which='both', color='grey', linewidth=1, linestyle='-', alpha=0.2)

    # Draw arrows
    # arrow_fmt = dict(markersize=4, color='black', clip_on=False)
    # self.axes.plot((1), (0), marker='>', transform=self.axes.get_yaxis_transform(), **arrow_fmt)
    # self.axes.plot((-1), (0), marker='<', transform=self.axes.get_yaxis_transform(), **arrow_fmt)
    # self.axes.plot((0), (1), marker='^', transform=self.axes.get_xaxis_transform(), **arrow_fmt)
    # self.axes.plot((0), (-1), marker='v', transform=self.axes.get_xaxis_transform(), **arrow_fmt)

    arrow_fmt = dict(markersize=4, color='black', clip_on=False)
    self.axes.annotate("", xy=(xmax+1, 0), xytext=(xmax+0.9, 0), arrowprops=dict(arrowstyle="->", linewidth=1.5), va='center',
                ha='right')
    self.axes.annotate("", xy=(xmin-1, 0), xytext=(xmin-0.9, 0), arrowprops=dict(arrowstyle="->", linewidth=1.5), va='center',
                ha='right')
    self.axes.annotate("", xy=(0, ymax+1), xytext=(0, ymax+0.9), arrowprops=dict(arrowstyle="->", linewidth=1.5), va='center',
                ha='right')
    self.axes.annotate("", xy=(0, ymin-1), xytext=(0, ymin-0.9), arrowprops=dict(arrowstyle="->", linewidth=1.5), va='center',
                ha='right')

    self.canvas.draw()


plotDataPoints(mpl_widget, [1, 2, 3], [1, 2, 3])

window.show()
app.exec_()
