from PyQt5 import QtWidgets, uic, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout,QMessageBox 
import sys
from Stopwatch import *
import numpy as np
from threading import Thread
import scipy

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("GUI.ui", self)
        self.GraphWidget1 = PlotWidget()
        self.GraphWidget1.setXRange(0,1)
        # self.GraphWidget1.getPlotItem().hideAxis('bottom')
        # self.GraphWidget1.getPlotItem().hideAxis('left')
        self.transition = pg.InfiniteLine(pen='white')
        layout1=QVBoxLayout()
        layout1.addWidget(self.GraphWidget1)
        self.ui.widget_11.setLayout(layout1)
        self.ui.full_menu.setVisible(False)
        self.ui.Monitor.clicked.connect(self.MonitoringMode)
        self.ui.Monitor2.clicked.connect(self.MonitoringMode)
        self.ui.Statistics.clicked.connect(self.StatisticsMode)
        self.ui.Statistics2.clicked.connect(self.StatisticsMode)
        self.ui.pushButton_9.clicked.connect(self.UpdateSidebar)
        self.ui.actionLoad.triggered.connect(self.LoadData)
        self.ui.clear.clicked.connect(self.Pause)
        self.ui.Statistics.setHidden(True)
        self.ui.Statistics2.setHidden(True)

        self.time = 0
        self.pos = 0 
        self.cycles = 0
        self.values = []
        self.peakcounter = 1
        self.paused = False


    def UpdateSidebar(self):
        if self.ui.pushButton_9.isChecked() == True:
            self.ui.Monitor2.setHidden(True)
            self.ui.Statistics2.setHidden(True)
            self.ui.exit2.setHidden(True)
        else:
            self.ui.Monitor2.setHidden(False)
            # self.ui.Statistics2.setHidden(False)
            self.ui.exit2.setHidden(False)

    def StatisticsMode(self):
        self.ui.stackedWidget.setCurrentIndex(1)
        self.ui.stackedWidget_2.setCurrentIndex(1)

    def MonitoringMode(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.stackedWidget_2.setCurrentIndex(0)

    def Pause(self):
        if self.paused == False:
            self.paused = True
        else:
            self.paused = False

    def LoadData(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName()
        except:
            pass
        else:
            path = filename[0]
            with open(path, 'rb') as file:
                # Read binary data
                binary_data = file.read()
                
                # Convert binary data to a 1D array of integers
                values2= np.frombuffer(binary_data, dtype=np.int32)
                data1=values2.copy()
                self.ECGvalues=data1[:9000]
                
                #fs is already known in medical signals
                fs = 500.0  # Sample rate in Hz
                
                # Calculate time values
                self.ECGtimes = np.arange(0, len(self.ECGvalues) / fs, 1 / fs)
            self.GraphWidget1.setYRange(min(self.ECGvalues),max(self.ECGvalues))
            self.GraphWidget1.clear()
            self.ECGdataline = self.GraphWidget1.plot(name='ECG',pen='g')
            self.ECGdataline.clear()
            self.values = []
            self.times = []
            self.time = 0
            self.pos = 0
            self.peakcounter = 1
            self.GraphWidget1.addItem(self.transition)
            self.peaks = scipy.signal.find_peaks(self.ECGvalues,height=4e+06)[0]
            self.Visualize()

    def Visualize(self):
        self.timer1 = QtCore.QTimer()
        self.timer1.setInterval(int(50))
        self.timer1.timeout.connect(
            self.Visualize
        )  # Connect to a single update method
        self.timer1.start()
        if self.paused == False:
            self.time += 10
            self.pos += 10
            self.times = self.ECGtimes[:self.time]
            if len(self.values) < 500:
                self.values = self.ECGvalues[:self.pos]
            else:
                self.values[self.time-10:self.time] = self.ECGvalues[self.pos-10:self.pos]
                self.times = self.ECGtimes[:500]
            self.transition.setValue(self.time/500)
            if self.peakcounter < len(self.peaks)-1 and self.pos > self.peaks[self.peakcounter]:
                self.peakcounter += 1
                time = (self.peaks[self.peakcounter] - self.peaks[self.peakcounter - 1]) * 0.002
                BPM = 60/time
                self.ui.label_2.setText(str(int(BPM)))
                if BPM < 60 or BPM > 90:
                    self.ui.label_2.setStyleSheet("color: red;") 
                elif BPM < 65 or BPM > 80:
                    self.ui.label_2.setStyleSheet("color: yellow;")
                elif BPM >= 65 and BPM <= 80:
                    self.ui.label_2.setStyleSheet("color: green;")
            if self.time == 500:
                self.time = 0
                self.cycles += 1
            # if self.time%500 ==0:
            #     self.time = 0
            #     self.cycles += 1

            self.ECGdataline.setData(self.times,self.values)
            if self.pos >= 9000:
                self.timer1.stop()