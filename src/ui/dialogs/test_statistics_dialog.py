from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, 
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QGroupBox, QGridLayout, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from ...utils.test_manager import TestManager
from ...utils.visualization_manager import VisualizationManager
import os
import sys
import webbrowser

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TestStatisticsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.test_manager = TestManager()
        self.visualization_manager = VisualizationManager()
        self.initUI()
        self.load_statistics()

    def initUI(self):
        self.setWindowTitle('테스트 통계')
        self.setWindowIcon(QIcon(resource_path('img/icon.png')))
        self.setGeometry(100, 100, 1000, 800)

        # 메인 레이아웃
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 기간 선택
        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel('기간:'))
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(['1일', '1주일', '1개월'])
        self.period_combo.currentTextChanged.connect(self.load_statistics)
        period_layout.addWidget(self.period_combo)
        
        layout.addLayout(period_layout)

        # 탭 위젯 생성
        tab_widget = QTabWidget()
        layout.addWidget(tab_widget)

        # 요약 탭
        summary_tab = QWidget()
        summary_layout = QVBoxLayout()
        summary_tab.setLayout(summary_layout)

        # 요약 정보 그룹
        summary_group = QGroupBox('요약 정보')
        summary_grid = QGridLayout()
        
        # 전체 테스트 수
        summary_grid.addWidget(QLabel('전체 테스트:'), 0, 0)
        self.total_tests_label = QLabel()
        summary_grid.addWidget(self.total_tests_label, 0, 1)
        
        # 통과 테스트 수
        summary_grid.addWidget(QLabel('통과 테스트:'), 1, 0)
        self.passed_tests_label = QLabel()
        summary_grid.addWidget(self.passed_tests_label, 1, 1)
        
        # 실패 테스트 수
        summary_grid.addWidget(QLabel('실패 테스트:'), 2, 0)
        self.failed_tests_label = QLabel()
        summary_grid.addWidget(self.failed_tests_label, 2, 1)
        
        # 평균 통과율
        summary_grid.addWidget(QLabel('평균 통과율:'), 3, 0)
        self.pass_rate_label = QLabel()
        summary_grid.addWidget(self.pass_rate_label, 3, 1)
        
        summary_group.setLayout(summary_grid)
        summary_layout.addWidget(summary_group)

        # 테스트 유형별 통계 테이블
        type_group = QGroupBox('테스트 유형별 통계')
        type_layout = QVBoxLayout()
        
        self.type_table = QTableWidget()
        self.type_table.setColumnCount(5)
        self.type_table.setHorizontalHeaderLabels(['테스트 유형', '테스트 수', '통과', '실패', '통과율'])
        self.type_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        type_layout.addWidget(self.type_table)
        
        type_group.setLayout(type_layout)
        summary_layout.addWidget(type_group)

        # 그래프 버튼
        graph_btn_layout = QHBoxLayout()
        
        self.summary_graph_btn = QPushButton('요약 그래프 보기')
        self.summary_graph_btn.clicked.connect(self.show_summary_graph)
        graph_btn_layout.addWidget(self.summary_graph_btn)
        
        self.distribution_graph_btn = QPushButton('분포 그래프 보기')
        self.distribution_graph_btn.clicked.connect(self.show_distribution_graph)
        graph_btn_layout.addWidget(self.distribution_graph_btn)
        
        summary_layout.addLayout(graph_btn_layout)

        # 일별 통계 탭
        daily_tab = QWidget()
        daily_layout = QVBoxLayout()
        daily_tab.setLayout(daily_layout)

        # 일별 통계 테이블
        daily_group = QGroupBox('일별 통계')
        daily_table_layout = QVBoxLayout()
        
        self.daily_table = QTableWidget()
        self.daily_table.setColumnCount(5)
        self.daily_table.setHorizontalHeaderLabels(['날짜', '테스트 수', '통과', '실패', '통과율'])
        self.daily_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        daily_table_layout.addWidget(self.daily_table)
        
        daily_group.setLayout(daily_table_layout)
        daily_layout.addWidget(daily_group)

        # 일별 추이 그래프 버튼
        self.trend_graph_btn = QPushButton('일별 추이 그래프 보기')
        self.trend_graph_btn.clicked.connect(self.show_trend_graph)
        daily_layout.addWidget(self.trend_graph_btn)

        # 탭 추가
        tab_widget.addTab(summary_tab, '요약')
        tab_widget.addTab(daily_tab, '일별 통계')

        # 닫기 버튼
        close_btn = QPushButton('닫기')
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)

    def load_statistics(self):
        """통계 정보 로드"""
        # 기간 설정
        period_map = {
            '1일': 'day',
            '1주일': 'week',
            '1개월': 'month'
        }
        period = period_map.get(self.period_combo.currentText(), 'day')
        
        # 통계 정보 조회
        self.current_stats = self.test_manager.get_test_statistics(period)
        
        # 요약 정보 표시
        self.total_tests_label.setText(str(self.current_stats['total_tests']))
        self.passed_tests_label.setText(str(self.current_stats['total_passed']))
        self.failed_tests_label.setText(str(self.current_stats['total_failed']))
        self.pass_rate_label.setText(f"{self.current_stats['average_pass_rate']:.1f}%")
        
        # 테스트 유형별 통계 표시
        self.type_table.setRowCount(len(self.current_stats['test_types']))
        for i, (test_type, type_stats) in enumerate(self.current_stats['test_types'].items()):
            self.type_table.setItem(i, 0, QTableWidgetItem(test_type))
            self.type_table.setItem(i, 1, QTableWidgetItem(str(type_stats['count'])))
            self.type_table.setItem(i, 2, QTableWidgetItem(str(type_stats['passed'])))
            self.type_table.setItem(i, 3, QTableWidgetItem(str(type_stats['failed'])))
            self.type_table.setItem(i, 4, QTableWidgetItem(f"{type_stats['pass_rate']:.1f}%"))
        
        # 일별 통계 표시
        self.daily_table.setRowCount(len(self.current_stats['daily_stats']))
        for i, daily_stat in enumerate(self.current_stats['daily_stats']):
            date = f"{daily_stat['date'][:4]}-{daily_stat['date'][4:6]}-{daily_stat['date'][6:]}"
            self.daily_table.setItem(i, 0, QTableWidgetItem(date))
            self.daily_table.setItem(i, 1, QTableWidgetItem(str(daily_stat['total'])))
            self.daily_table.setItem(i, 2, QTableWidgetItem(str(daily_stat['passed'])))
            self.daily_table.setItem(i, 3, QTableWidgetItem(str(daily_stat['failed'])))
            self.daily_table.setItem(i, 4, QTableWidgetItem(f"{daily_stat['pass_rate']:.1f}%"))

    def show_summary_graph(self):
        """요약 그래프 표시"""
        if not hasattr(self, 'current_stats'):
            return
        
        filepath = self.visualization_manager.create_test_summary_graph(self.current_stats)
        webbrowser.open('file://' + os.path.abspath(filepath))

    def show_distribution_graph(self):
        """분포 그래프 표시"""
        if not hasattr(self, 'current_stats'):
            return
        
        filepath = self.visualization_manager.create_test_distribution_graph(self.current_stats)
        webbrowser.open('file://' + os.path.abspath(filepath))

    def show_trend_graph(self):
        """일별 추이 그래프 표시"""
        if not hasattr(self, 'current_stats'):
            return
        
        filepath = self.visualization_manager.create_daily_trend_graph(self.current_stats)
        webbrowser.open('file://' + os.path.abspath(filepath)) 