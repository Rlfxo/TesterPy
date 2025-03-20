from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from .dialogs.OC_dialog import OperationsCenterDialog
from .dialogs.QC_dialog import QualityCenterDialog
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
        self.setWindowTitle('SerialPy')
        self.setWindowIcon(QIcon(resource_path('img/icon.png')))
        self.setGeometry(100, 100, 400, 300)

        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 레이아웃
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # 운영 센터 버튼
        oc_btn = QPushButton('운영 센터')
        oc_btn.clicked.connect(self.show_operations_center)
        layout.addWidget(oc_btn)
        
        # 품질 관리 센터 버튼
        qc_btn = QPushButton('품질 관리 센터')
        qc_btn.clicked.connect(self.show_quality_center)
        layout.addWidget(qc_btn)

    def show_operations_center(self):
        """운영 센터 다이얼로그 표시"""
        dialog = OperationsCenterDialog()
        dialog.exec_()

    def show_quality_center(self):
        """품질 관리 센터 다이얼로그 표시"""
        dialog = QualityCenterDialog()
        dialog.exec_() 