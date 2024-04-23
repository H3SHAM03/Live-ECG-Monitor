from MyWindow import *

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('Live ECG Monitor')
    window.setWindowIcon(QtGui.QIcon('assets\\icon.png'))
    window.show()
    sys.exit(app.exec_())