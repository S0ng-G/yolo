# MainLogic.py
import os, cv2, traceback
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QApplication
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from ultralytics import YOLO
from GUI import Ui_MainWindow
import PyQt5

dirname = os.path.dirname(PyQt5.__file__)
qt_dir = os.path.join(dirname, 'Qt5', 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = qt_dir


class LogicMixin(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.model = None
        self.filePath = None
        self.file_path = None
        self.is_detecting = False

    # 与GUI中的UI连接
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)

        # 信号连接
        self.loadModelBtn.clicked.connect(self.load_model)
        self.fileBtn.clicked.connect(self.select_file)
        self.detectBtn.clicked.connect(self.run_detection)

    def load_model(self):
        try:
            model_name = self.modelCombo.currentText() + ".pt"
            self.model = YOLO(model_name)
            self.statusbar.showMessage(f"模型加载成功: {model_name}")
            self.fileBtn.setEnabled(True)
        except Exception as e:
            self.statusbar.showMessage(f"错误: {str(e)}")
            self.model = None
            self.detectBtn.setEnabled(False)

    def select_file(self):
        try:
            options = QFileDialog.Options()
            input_type = self.inputCombo.currentText()

            if input_type == "图片":
                file, _ = QFileDialog.getOpenFileName(None, "选择图片", "",
                                                      "图片文件 (*.jpg *.jpeg *.png *.bmp);;所有文件 (*)",
                                                      options=options)
                if file and os.path.exists(file):
                    frame = cv2.imread(file)
                    if frame is not None:
                        self.file_path = file
                        self.display_image(frame)
                        self.statusbar.showMessage(f"已加载图片: {os.path.basename(file)}")
                        self.detectBtn.setEnabled(True)
                    else:
                        QMessageBox.critical(None, "错误", "无法读取图片文件！")

            elif input_type == "视频":
                file, _ = QFileDialog.getOpenFileName(None, "选择视频", "",
                                                      "视频文件 (*.mp4 *.avi *.mov *.mkv);;所有文件 (*)",
                                                      options=options)
                if file:
                    self.filePath = file
                    self.statusbar.showMessage(f"已加载视频: {os.path.basename(file)}")
                    self.detectBtn.setEnabled(True)
                    cap = cv2.VideoCapture(file)
                    ret, frame = cap.read()
                    cap.release()
                    if ret and frame is not None:
                        self.display_image(frame)
                    else:
                        QMessageBox.critical(None, "错误", "无法读取视频第一帧！")

            elif input_type == "摄像头":
                self.detectBtn.setEnabled(True)

        except Exception as e:
            QMessageBox.critical(None, "文件选择失败", str(e))
            print(traceback.format_exc())

    def display_image(self, cv_img):
        try:
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.videoLabel.setPixmap(QPixmap.fromImage(qt_image).scaled(
                self.videoLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        except Exception as e:
            self.statusbar.showMessage(f"显示错误: {str(e)}")

    def run_detection(self):
        try:
            if self.model is None:
                QMessageBox.warning(None, "模型未加载", "请先加载模型！")
                return


            conf_threshold = self.confSlider.value() / 100.0
            input_type = self.inputCombo.currentText()

            if input_type == "摄像头":
                self.statusbar.showMessage("打开摄像头中...")
                cap = cv2.VideoCapture(0)  # 默认第一个摄像头
                if not cap.isOpened():
                    QMessageBox.critical(None, "错误", "无法打开摄像头！")
                    return

                self.statusbar.showMessage("摄像头检测进行中... 按 Ctrl+C 或关闭窗口以终止")
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    conf_threshold = self.confSlider.value() / 100.0
                    results = self.model(frame, conf=conf_threshold)[0]
                    result_frame = results.plot()
                    self.display_image(result_frame)

                    # 等待 1ms，处理 GUI 事件，防止卡死
                    QApplication.processEvents()

                cap.release()
                self.statusbar.showMessage("摄像头检测结束")

            elif input_type == "图片":
                if not self.file_path:
                    QMessageBox.warning(None, "未选择文件", "请选择图片文件！")
                    return

                results = self.model(self.file_path, conf=conf_threshold)[0]
                result_img = results.plot()
                self.display_image(result_img)
                self.statusbar.showMessage("图片检测完成")

            elif input_type == "视频":
                if not self.filePath:
                    QMessageBox.warning(None, "未选择视频", "请选择视频文件！")
                    return

                cap = cv2.VideoCapture(self.filePath)
                if not cap.isOpened():
                    QMessageBox.critical(None, "错误", "无法打开视频文件！")
                    return

                self.statusbar.showMessage("开始处理视频...")
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break

                    results = self.model(frame, conf=conf_threshold)[0]
                    result_frame = results.plot()
                    self.display_image(result_frame)
                    cv2.waitKey(1)

                cap.release()
                self.statusbar.showMessage("视频检测完成")

        except Exception as e:
            QMessageBox.critical(None, "检测失败", str(e))

