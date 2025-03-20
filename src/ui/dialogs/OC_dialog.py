from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, 
                             QTextEdit, QMessageBox)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from ...utils.serial_manager import SerialManager
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SerialMonitorThread(QThread):
    data_received = pyqtSignal(bytes)

    def __init__(self, serial_manager):
        super().__init__()
        self.serial_manager = serial_manager

    def run(self):
        self.serial_manager.start_monitoring()

    def stop(self):
        self.serial_manager.stop_monitoring()

class OperationsCenterDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.serial_manager = SerialManager()
        self.monitor_thread = None
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
        self.refresh_ports()
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

    def refresh_ports(self):
        """사용 가능한 포트 목록 새로고침"""
        current_port = self.port_combo.currentText()
        self.port_combo.clear()
        self.port_combo.addItems(self.serial_manager.get_available_ports())
        
        # 이전 선택 포트가 여전히 존재하면 다시 선택
        if current_port in self.port_combo.items():
            self.port_combo.setCurrentText(current_port)

    def toggle_connection(self):
        """시리얼 포트 연결/해제 토글"""
        if not self.serial_manager.is_connected:
            port = self.port_combo.currentText()
            if not port:
                QMessageBox.warning(self, '경고', '포트를 선택해주세요.')
                return

            if self.serial_manager.connect(port):
                self.connect_btn.setText('연결 해제')
                self.start_btn.setEnabled(True)
                self.log_text.append(f'포트 {port}에 연결되었습니다.')
                
                # 데이터 모니터링 시작
                self.monitor_thread = SerialMonitorThread(self.serial_manager)
                self.monitor_thread.data_received.connect(self.handle_received_data)
                self.monitor_thread.start()
            else:
                QMessageBox.critical(self, '오류', '포트 연결에 실패했습니다.')
        else:
            self.serial_manager.disconnect()
            if self.monitor_thread:
                self.monitor_thread.stop()
                self.monitor_thread.wait()
                self.monitor_thread = None
            
            self.connect_btn.setText('연결')
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)
            self.log_text.append('포트 연결이 해제되었습니다.')

    def handle_received_data(self, data: bytes):
        """수신된 데이터 처리"""
        try:
            # 데이터를 문자열로 변환하여 로그에 표시
            text = data.decode('utf-8')
            self.log_text.append(text)
        except UnicodeDecodeError:
            # UTF-8 디코딩 실패 시 16진수로 표시
            hex_data = ' '.join([f'{b:02X}' for b in data])
            self.log_text.append(f'[HEX] {hex_data}')

    def start_operation(self):
        """작업 시작"""
        # TODO: 실제 작업 시작 로직 구현
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.log_text.append('작업이 시작되었습니다.')

    def stop_operation(self):
        """작업 정지"""
        # TODO: 실제 작업 정지 로직 구현
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.log_text.append('작업이 정지되었습니다.')

    def closeEvent(self, event):
        """다이얼로그 종료 시 정리"""
        if self.serial_manager.is_connected:
            self.serial_manager.disconnect()
        if self.monitor_thread:
            self.monitor_thread.stop()
            self.monitor_thread.wait()
        event.accept() 