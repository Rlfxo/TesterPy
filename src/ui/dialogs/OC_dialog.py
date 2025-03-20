from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, 
                             QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class OperationsCenterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Operations Center')
        self.setWindowIcon(QIcon(resource_path('img/icon.png')))
        self.setGeometry(100, 100, 800, 600)

        # 메인 레이아웃
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 상단 컨트롤 영역
        control_layout = QHBoxLayout()
        
        # 포트 선택 콤보박스
        self.port_combo = QComboBox()
        self.port_combo.addItems(['COM1', 'COM2', 'COM3', 'COM4'])
        control_layout.addWidget(QLabel('포트:'))
        control_layout.addWidget(self.port_combo)

        # 연결 버튼
        self.connect_btn = QPushButton('연결')
        self.connect_btn.clicked.connect(self.toggle_connection)
        control_layout.addWidget(self.connect_btn)

        # 새로고침 버튼
        refresh_btn = QPushButton('새로고침')
        refresh_btn.clicked.connect(self.refresh_ports)
        control_layout.addWidget(refresh_btn)

        layout.addLayout(control_layout)

        # 로그 영역
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        # 하단 버튼 영역
        button_layout = QHBoxLayout()
        
        # 시작 버튼
        self.start_btn = QPushButton('시작')
        self.start_btn.clicked.connect(self.start_operation)
        self.start_btn.setEnabled(False)
        button_layout.addWidget(self.start_btn)

        # 정지 버튼
        self.stop_btn = QPushButton('정지')
        self.stop_btn.clicked.connect(self.stop_operation)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)

        # 닫기 버튼
        close_btn = QPushButton('닫기')
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def toggle_connection(self):
        if self.connect_btn.text() == '연결':
            # TODO: 실제 연결 로직 구현
            self.connect_btn.setText('연결 해제')
            self.start_btn.setEnabled(True)
            self.log_text.append('장비가 연결되었습니다.')
        else:
            # TODO: 실제 연결 해제 로직 구현
            self.connect_btn.setText('연결')
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            self.log_text.append('장비 연결이 해제되었습니다.')

    def refresh_ports(self):
        # TODO: 실제 포트 목록 새로고침 로직 구현
        self.log_text.append('포트 목록을 새로고침했습니다.')

    def start_operation(self):
        # TODO: 실제 시작 로직 구현
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_text.append('작업이 시작되었습니다.')

    def stop_operation(self):
        # TODO: 실제 정지 로직 구현
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.log_text.append('작업이 정지되었습니다.') 