# GUI.py
# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.controlPanel = QtWidgets.QWidget(self.centralwidget)
        self.controlPanel.setMinimumSize(QtCore.QSize(250, 0))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.controlPanel)

        self.label = QtWidgets.QLabel(self.controlPanel)
        self.verticalLayout.addWidget(self.label)

        self.modelCombo = QtWidgets.QComboBox(self.controlPanel)
        self.modelCombo.addItems(["yolov8n", "yolov8s", "yolov8m", "yolov8l", "yolov8x"])
        self.verticalLayout.addWidget(self.modelCombo)

        self.loadModelBtn = QtWidgets.QPushButton(self.controlPanel)
        self.verticalLayout.addWidget(self.loadModelBtn)
        self.verticalLayout.addItem(QtWidgets.QSpacerItem(20, 20))

        self.label_2 = QtWidgets.QLabel(self.controlPanel)
        self.verticalLayout.addWidget(self.label_2)

        self.inputCombo = QtWidgets.QComboBox(self.controlPanel)
        self.inputCombo.addItems(["摄像头", "图片", "视频"])
        self.verticalLayout.addWidget(self.inputCombo)

        self.fileBtn = QtWidgets.QPushButton(self.controlPanel)
        self.fileBtn.setEnabled(False)
        self.verticalLayout.addWidget(self.fileBtn)
        self.verticalLayout.addItem(QtWidgets.QSpacerItem(20, 20))

        self.label_3 = QtWidgets.QLabel(self.controlPanel)
        self.verticalLayout.addWidget(self.label_3)

        self.confSlider = QtWidgets.QSlider(self.controlPanel)
        self.confSlider.setOrientation(QtCore.Qt.Horizontal)
        self.confSlider.setRange(1, 99)
        self.confSlider.setValue(50)
        self.verticalLayout.addWidget(self.confSlider)

        self.confSpin = QtWidgets.QSpinBox(self.controlPanel)
        self.confSpin.setRange(1, 99)
        self.confSpin.setValue(50)
        self.verticalLayout.addWidget(self.confSpin)

        self.verticalLayout.addItem(QtWidgets.QSpacerItem(20, 20))
        self.detectBtn = QtWidgets.QPushButton(self.controlPanel)
        self.detectBtn.setEnabled(False)
        self.verticalLayout.addWidget(self.detectBtn)
        self.verticalLayout.addItem(QtWidgets.QSpacerItem(20, 40))

        self.horizontalLayout.addWidget(self.controlPanel)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)

        self.videoTab = QtWidgets.QWidget()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.videoTab)
        self.videoLabel = QtWidgets.QLabel(self.videoTab)
        self.videoLabel.setStyleSheet("background-color: black;")
        self.videoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.videoLabel)
        self.tabWidget.addTab(self.videoTab, "实时检测")

        self.metricsTab = QtWidgets.QWidget()
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.metricsTab)
        self.metricsLabel = QtWidgets.QLabel(self.metricsTab)
        self.metricsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_3.addWidget(self.metricsLabel)
        self.tabWidget.addTab(self.metricsTab, "性能指标")

        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.confSlider.valueChanged.connect(self.confSpin.setValue)
        self.confSpin.valueChanged.connect(self.confSlider.setValue)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "YOLOv8 目标检测系统"))
        self.label.setText(_translate("MainWindow", "<b>模型选择</b>"))
        self.loadModelBtn.setText(_translate("MainWindow", "加载模型"))
        self.label_2.setText(_translate("MainWindow", "<b>输入源</b>"))
        self.fileBtn.setText(_translate("MainWindow", "选择文件"))
        self.label_3.setText(_translate("MainWindow", "<b>置信度阈值 (%)</b>"))
        self.detectBtn.setText(_translate("MainWindow", "开始检测"))
        self.videoLabel.setText(_translate("MainWindow", "等待视频输入..."))
        self.metricsLabel.setText(_translate("MainWindow", "训练指标将在此显示..."))
