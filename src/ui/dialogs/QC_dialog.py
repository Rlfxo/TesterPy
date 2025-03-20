from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, 
                             QTextEdit, QMessageBox, QTableWidget,
                             QTableWidgetItem, QHeaderView)
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

class QualityCenterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quality Center')
        self.setWindowIcon(QIcon(resource_path('img/icon.png')))
        self.setGeometry(100, 100, 1000, 800)

        # 메인 레이아웃
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 상단 컨트롤 영역
        control_layout = QHBoxLayout()
        
        # 테스트 항목 선택 콤보박스
        self.test_combo = QComboBox()
        self.test_combo.addItems(['전체 테스트', '전기적 특성', '기계적 특성', '환경 테스트'])
        control_layout.addWidget(QLabel('테스트 항목:'))
        control_layout.addWidget(self.test_combo)

        # 시작 버튼
        self.start_btn = QPushButton('테스트 시작')
        self.start_btn.clicked.connect(self.start_test)
        control_layout.addWidget(self.start_btn)

        # 결과 저장 버튼
        save_btn = QPushButton('결과 저장')
        save_btn.clicked.connect(self.save_results)
        control_layout.addWidget(save_btn)

        layout.addLayout(control_layout)

        # 테스트 결과 테이블
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(['테스트 항목', '측정값', '기준값', '단위', '결과'])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.result_table)

        # 로그 영역
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)

        # 하단 버튼 영역
        button_layout = QHBoxLayout()
        
        # 리포트 생성 버튼
        report_btn = QPushButton('리포트 생성')
        report_btn.clicked.connect(self.generate_report)
        button_layout.addWidget(report_btn)

        # 닫기 버튼
        close_btn = QPushButton('닫기')
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def start_test(self):
        # TODO: 실제 테스트 시작 로직 구현
        self.log_text.append('테스트가 시작되었습니다.')
        self.start_btn.setEnabled(False)

    def save_results(self):
        # TODO: 실제 결과 저장 로직 구현
        self.log_text.append('테스트 결과가 저장되었습니다.')

    def generate_report(self):
        # TODO: 실제 리포트 생성 로직 구현
        self.log_text.append('테스트 리포트가 생성되었습니다.') 