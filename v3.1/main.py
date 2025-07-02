import os
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

from TrainMainWindow import YoloTrainerApp
from MainLogic import LogicMixin

class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Assets/UI/MainGUI.ui", self)

        self.trainButton.clicked.connect(self.open_train)
        self.detectButton.clicked.connect(self.open_detect)

        self.train_window = None
        self.detect_window = None

        self.load_history_records()

    def open_train(self):
        if self.train_window is None:
            self.train_window = YoloTrainerApp()
        self.train_window.show()

    def open_detect(self):
        if self.detect_window is None:
            self.detect_window = LogicMixin()
        self.detect_window.show()

    def load_history_records(self):
        if self.historyContainer.layout() is None:
            from PyQt5.QtWidgets import QVBoxLayout
            self.historyContainer.setLayout(QVBoxLayout())

        folder_path = "Assets/history"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        layout = self.historyContainer.layout()

        # 遍历文件夹中的文件并显示
        for filename in os.listdir(folder_path):
            filepath = os.path.join(folder_path, filename)
            if os.path.isfile(filepath):
                label = QLabel(f"{filename}")
                label.setStyleSheet("font: 11pt 'Arial'; color: white; padding: 2px;")
                layout.addWidget(label)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainController()
    window.show()
    sys.exit(app.exec_())
