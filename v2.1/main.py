# main.py
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow
from MainLogic import LogicMixin

class MainWindow(QMainWindow, LogicMixin):
    def __init__(self):
        super(MainWindow, self).__init__()
    
    def resizeEvent(self, event):
        if hasattr(self, 'last_frame') and self.last_frame is not None:
            self.display_image(self.last_frame)
        event.accept()

    def closeEvent(self, event):
        self.stop_flag = True
        try:
            if hasattr(self, 'cap') and self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass
        event.accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
