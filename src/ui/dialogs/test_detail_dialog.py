from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QTableWidget,
                             QTableWidgetItem, QHeaderView, QMessageBox,
                             QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ...utils.test_manager import TestManager
import os
import sys
import webbrowser

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TestDetailDialog(QDialog):
    def __init__(self, test_id: str):
        super().__init__()
        self.test_manager = TestManager()
        self.test_id = test_id
        self.initUI()
        self.load_test_detail()

    def initUI(self):
        self.setWindowTitle('테스트 상세 정보')
        self.setWindowIcon(QIcon(resource_path('img/icon.png')))
        self.setGeometry(100, 100, 800, 600)

        # 메인 레이아웃
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 테스트 정보 그룹
        info_group = QGroupBox('테스트 정보')
        info_layout = QGridLayout()
        
        # 테스트 유형
        info_layout.addWidget(QLabel('테스트 유형:'), 0, 0)
        self.type_label = QLabel()
        info_layout.addWidget(self.type_label, 0, 1)
        
        # 테스트 시간
        info_layout.addWidget(QLabel('테스트 시간:'), 1, 0)
        self.time_label = QLabel()
        info_layout.addWidget(self.time_label, 1, 1)
        
        # 테스트 결과
        info_layout.addWidget(QLabel('테스트 결과:'), 2, 0)
        self.result_label = QLabel()
        info_layout.addWidget(self.result_label, 2, 1)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # 테스트 결과 테이블
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(['테스트 항목', '측정값', '기준값', '단위', '결과'])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.result_table)

        # 버튼 영역
        button_layout = QHBoxLayout()
        
        # 리포트 보기 버튼
        report_btn = QPushButton('리포트 보기')
        report_btn.clicked.connect(self.view_report)
        button_layout.addWidget(report_btn)

        # 닫기 버튼
        close_btn = QPushButton('닫기')
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def load_test_detail(self):
        """테스트 상세 정보 로드"""
        # 테스트 데이터 찾기
        test_data = None
        for test in self.test_manager.get_test_history():
            if test['timestamp'] == self.test_id:
                test_data = test
                break

        if not test_data:
            QMessageBox.warning(self, '오류', '테스트 정보를 찾을 수 없습니다.')
            self.close()
            return

        # 테스트 정보 표시
        self.type_label.setText(test_data['test_type'])
        self.time_label.setText(test_data['timestamp'])
        
        # 테스트 결과 계산
        total_tests = len(test_data['results'])
        passed_tests = sum(1 for r in test_data['results'] if r['result'] == 'PASS')
        result_text = f'통과: {passed_tests}/{total_tests}'
        self.result_label.setText(result_text)

        # 결과 테이블 표시
        self.result_table.setRowCount(len(test_data['results']))
        for i, result in enumerate(test_data['results']):
            self.result_table.setItem(i, 0, QTableWidgetItem(result['test_item']))
            self.result_table.setItem(i, 1, QTableWidgetItem(f"{result['measured_value']:.2f}"))
            self.result_table.setItem(i, 2, QTableWidgetItem(f"{result['reference_value']:.2f}"))
            self.result_table.setItem(i, 3, QTableWidgetItem(result['unit']))
            self.result_table.setItem(i, 4, QTableWidgetItem(result['result']))

    def view_report(self):
        """테스트 리포트 보기"""
        report_path = self.test_manager.generate_report(self.test_id)
        if report_path:
            webbrowser.open('file://' + os.path.abspath(report_path))
        else:
            QMessageBox.warning(self, '오류', '리포트 생성에 실패했습니다.') 