from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QGridLayout, QTabWidget,
                             QCalendarWidget, QMessageBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QIcon
from ...utils.test_manager import TestManager
from ...utils.visualization_manager import VisualizationManager
import os
import sys
import webbrowser
from datetime import datetime, timedelta

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TestHistoryDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.test_manager = TestManager()
        self.visualization_manager = VisualizationManager()
        self.initUI()
        self.load_history()

    def initUI(self):
        self.setWindowTitle('테스트 이력')
        self.setWindowIcon(QIcon(resource_path('img/icon.png')))
        self.setGeometry(100, 100, 1000, 800)

        # 메인 레이아웃
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 필터 영역
        filter_layout = QHBoxLayout()
        
        # 테스트 유형 필터
        filter_layout.addWidget(QLabel('테스트 유형:'))
        self.type_combo = QComboBox()
        self.type_combo.addItems(['전체', '전압', '전류', '온도', '저항'])
        self.type_combo.currentTextChanged.connect(self.load_history)
        filter_layout.addWidget(self.type_combo)
        
        # 기간 필터
        filter_layout.addWidget(QLabel('기간:'))
        self.period_combo = QComboBox()
        self.period_combo.addItems(['오늘', '1주일', '1개월', '3개월', '전체'])
        self.period_combo.currentTextChanged.connect(self.load_history)
        filter_layout.addWidget(self.period_combo)
        
        layout.addLayout(filter_layout)

        # 테스트 이력 테이블
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels(['날짜', '테스트 항목', '측정값', '기준값', '오차', '결과'])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.itemSelectionChanged.connect(self.on_selection_changed)
        layout.addWidget(self.history_table)

        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        
        self.view_detail_btn = QPushButton('상세 보기')
        self.view_detail_btn.clicked.connect(self.view_detail)
        self.view_detail_btn.setEnabled(False)
        button_layout.addWidget(self.view_detail_btn)
        
        self.view_graph_btn = QPushButton('그래프 보기')
        self.view_graph_btn.clicked.connect(self.view_graph)
        self.view_graph_btn.setEnabled(False)
        button_layout.addWidget(self.view_graph_btn)
        
        self.delete_btn = QPushButton('삭제')
        self.delete_btn.clicked.connect(self.delete_test)
        self.delete_btn.setEnabled(False)
        button_layout.addWidget(self.delete_btn)
        
        self.close_btn = QPushButton('닫기')
        self.close_btn.clicked.connect(self.close)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)

    def load_history(self):
        """테스트 이력 로드"""
        # 필터 조건 설정
        test_type = self.type_combo.currentText()
        if test_type == '전체':
            test_type = None
            
        period = self.period_combo.currentText()
        if period == '오늘':
            start_date = datetime.now().date()
        elif period == '1주일':
            start_date = datetime.now().date() - timedelta(days=7)
        elif period == '1개월':
            start_date = datetime.now().date() - timedelta(days=30)
        elif period == '3개월':
            start_date = datetime.now().date() - timedelta(days=90)
        else:  # 전체
            start_date = None

        # 테스트 이력 조회
        history = self.test_manager.get_test_history(test_type=test_type, start_date=start_date)
        
        # 테이블 업데이트
        self.history_table.setRowCount(len(history))
        for i, test in enumerate(history):
            self.history_table.setItem(i, 0, QTableWidgetItem(test['timestamp']))
            self.history_table.setItem(i, 1, QTableWidgetItem(test['test_item']))
            self.history_table.setItem(i, 2, QTableWidgetItem(f"{test['measured_value']:.2f}"))
            self.history_table.setItem(i, 3, QTableWidgetItem(f"{test['reference_value']:.2f}"))
            self.history_table.setItem(i, 4, QTableWidgetItem(f"{test['error']:.2f}%"))
            self.history_table.setItem(i, 5, QTableWidgetItem(test['result']))

    def on_selection_changed(self):
        """테이블 선택 변경 시 처리"""
        selected = len(self.history_table.selectedItems()) > 0
        self.view_detail_btn.setEnabled(selected)
        self.view_graph_btn.setEnabled(selected)
        self.delete_btn.setEnabled(selected)

    def view_detail(self):
        """선택한 테스트의 상세 정보 표시"""
        row = self.history_table.currentRow()
        if row < 0:
            return
            
        test_id = self.history_table.item(row, 0).text()
        test_data = self.test_manager.get_test_detail(test_id)
        
        from .test_detail_dialog import TestDetailDialog
        dialog = TestDetailDialog(test_data)
        dialog.exec_()

    def view_graph(self):
        """선택한 테스트의 그래프 표시"""
        row = self.history_table.currentRow()
        if row < 0:
            return
            
        test_id = self.history_table.item(row, 0).text()
        test_data = self.test_manager.get_test_detail(test_id)
        
        filepath = self.visualization_manager.create_test_result_graph(test_data)
        webbrowser.open('file://' + os.path.abspath(filepath))

    def delete_test(self):
        """선택한 테스트 삭제"""
        row = self.history_table.currentRow()
        if row < 0:
            return
            
        test_id = self.history_table.item(row, 0).text()
        
        reply = QMessageBox.question(
            self,
            '테스트 삭제',
            '선택한 테스트를 삭제하시겠습니까?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.test_manager.delete_test(test_id)
            self.load_history() 