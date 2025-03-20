from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QGridLayout)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from ...utils.test_manager import TestManager
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
        self.test_manager = TestManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('품질 관리 센터')
        self.setWindowIcon(QIcon(resource_path('img/icon.png')))
        self.setGeometry(100, 100, 800, 600)

        # 메인 레이아웃
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 테스트 선택
        test_layout = QHBoxLayout()
        test_layout.addWidget(QLabel('테스트 항목:'))
        
        self.test_combo = QComboBox()
        self.test_combo.addItems(['전압', '전류', '온도', '저항'])
        test_layout.addWidget(self.test_combo)
        
        layout.addLayout(test_layout)

        # 테스트 결과 테이블
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(['테스트 항목', '측정값', '기준값', '오차', '결과'])
        self.result_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.result_table)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton('테스트 시작')
        self.start_btn.clicked.connect(self.start_test)
        button_layout.addWidget(self.start_btn)
        
        self.save_btn = QPushButton('결과 저장')
        self.save_btn.clicked.connect(self.save_results)
        self.save_btn.setEnabled(False)
        button_layout.addWidget(self.save_btn)
        
        self.history_btn = QPushButton('테스트 이력')
        self.history_btn.clicked.connect(self.show_history)
        button_layout.addWidget(self.history_btn)
        
        self.close_btn = QPushButton('닫기')
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)

        # 타이머 설정
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_test)
        self.current_test_index = 0

    def start_test(self):
        """테스트 시작"""
        self.start_btn.setEnabled(False)
        self.save_btn.setEnabled(False)
        self.current_test_index = 0
        self.result_table.setRowCount(0)
        self.timer.start(1000)  # 1초마다 업데이트

    def update_test(self):
        """테스트 진행 업데이트"""
        test_items = ['전압', '전류', '온도', '저항']
        if self.current_test_index >= len(test_items):
            self.timer.stop()
            self.start_btn.setEnabled(True)
            self.save_btn.setEnabled(True)
            return

        # 테스트 결과 생성
        test_item = test_items[self.current_test_index]
        result = self.test_manager.run_test(test_item)

        # 결과 테이블에 추가
        row = self.result_table.rowCount()
        self.result_table.insertRow(row)
        self.result_table.setItem(row, 0, QTableWidgetItem(test_item))
        self.result_table.setItem(row, 1, QTableWidgetItem(f"{result['measured_value']:.2f}"))
        self.result_table.setItem(row, 2, QTableWidgetItem(f"{result['reference_value']:.2f}"))
        self.result_table.setItem(row, 3, QTableWidgetItem(f"{result['error']:.2f}%"))
        self.result_table.setItem(row, 4, QTableWidgetItem(result['result']))

        self.current_test_index += 1

    def save_results(self):
        """테스트 결과 저장"""
        results = []
        for row in range(self.result_table.rowCount()):
            result = {
                'test_item': self.result_table.item(row, 0).text(),
                'measured_value': float(self.result_table.item(row, 1).text()),
                'reference_value': float(self.result_table.item(row, 2).text()),
                'error': float(self.result_table.item(row, 3).text().replace('%', '')),
                'result': self.result_table.item(row, 4).text()
            }
            results.append(result)
        
        self.test_manager.save_test_results(results)
        self.save_btn.setEnabled(False)

    def show_history(self):
        """테스트 이력 표시"""
        from .test_history_dialog import TestHistoryDialog
        dialog = TestHistoryDialog()
        dialog.exec_()

    def closeEvent(self, event):
        """다이얼로그 종료 시 처리"""
        self.timer.stop()
        event.accept() 