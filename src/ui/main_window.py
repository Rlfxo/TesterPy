from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from .dialogs.OC_dialog import OperationsCenterDialog
from .dialogs.QC_dialog import QualityCenterDialog
from .dialogs.settings_dialog import SettingsDialog
import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('EVAR Tool')
        self.setWindowIcon(QIcon(resource_path('img/icon.png')))
        
        # 메인 위젯과 레이아웃 설정
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout()
        main_widget.setLayout(layout)

        # 로고 이미지
        logo_label = QLabel()
        logo_pixmap = QPixmap(resource_path('img/title.png'))
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)

        # 버튼 생성
        self.create_buttons(layout)

        # 윈도우 크기 및 위치 설정
        self.setGeometry(100, 100, 800, 600)

    def create_buttons(self, layout):
        # Operations Center 버튼
        oc_btn = QPushButton('Operations Center', self)
        oc_btn.clicked.connect(self.open_operations_center)
        layout.addWidget(oc_btn)

        # Quality Center 버튼
        qc_btn = QPushButton('Quality Center', self)
        qc_btn.clicked.connect(self.open_quality_center)
        layout.addWidget(qc_btn)

        # 프로그램 설정 버튼
        settings_btn = QPushButton('프로그램 설정', self)
        settings_btn.clicked.connect(self.open_settings)
        layout.addWidget(settings_btn)

        # 종료 버튼
        exit_btn = QPushButton('프로그램 종료', self)
        exit_btn.clicked.connect(self.close)
        layout.addWidget(exit_btn)

    def open_operations_center(self):
        dialog = OperationsCenterDialog()
        dialog.exec_()

    def open_quality_center(self):
        dialog = QualityCenterDialog()
        dialog.exec_()

    def open_settings(self):
        dialog = SettingsDialog()
        dialog.exec_() 