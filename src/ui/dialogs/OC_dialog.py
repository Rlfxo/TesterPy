from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QComboBox, 
                             QTextEdit, QMessageBox)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QIcon
from ...utils.serial_manager import SerialManager
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
        self.serial_manager = SerialManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('운영 센터')
        self.setWindowIcon(QIcon(resource_path('img/icon.png')))
        self.setGeometry(100, 100, 800, 600)

        # 메인 레이아웃
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 포트 선택 영역
        port_layout = QHBoxLayout()
        
        port_layout.addWidget(QLabel('포트:'))
        self.port_combo = QComboBox()
        self.refresh_ports()
        port_layout.addWidget(self.port_combo)
        
        self.refresh_btn = QPushButton('새로고침')
        self.refresh_btn.clicked.connect(self.refresh_ports)
        port_layout.addWidget(self.refresh_btn)
        
        self.connect_btn = QPushButton('연결')
        self.connect_btn.clicked.connect(self.toggle_connection)
        port_layout.addWidget(self.connect_btn)
        
        layout.addLayout(port_layout)

        # 데이터 표시 영역
        self.data_text = QTextEdit()
        self.data_text.setReadOnly(True)
        layout.addWidget(self.data_text)

        # 하단 버튼 영역
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton('시작')
        self.start_btn.clicked.connect(self.start_operation)
        self.start_btn.setEnabled(False)
        button_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton('정지')
        self.stop_btn.clicked.connect(self.stop_operation)
        self.stop_btn.setEnabled(False)
        button_layout.addWidget(self.stop_btn)
        
        close_btn = QPushButton('닫기')
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)

    def refresh_ports(self):
        """사용 가능한 포트 목록 갱신"""
        self.port_combo.clear()
        ports = self.serial_manager.get_available_ports()
        self.port_combo.addItems(ports)
        
        if ports:
            self.connect_btn.setEnabled(True)
        else:
            self.connect_btn.setEnabled(False)
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(False)

    def toggle_connection(self):
        """연결/해제 토글"""
        if not self.serial_manager.is_port_open():
            port = self.port_combo.currentText()
            if not port:
                QMessageBox.warning(self, '경고', '포트를 선택하세요.')
                return
                
            try:
                self.serial_manager.connect(port)
                self.connect_btn.setText('해제')
                self.start_btn.setEnabled(True)
                self.port_combo.setEnabled(False)
                self.refresh_btn.setEnabled(False)
                self.serial_manager.set_callback(self.on_data_received)
            except Exception as e:
                QMessageBox.critical(self, '오류', f'연결 실패: {str(e)}')
                return
        else:
            try:
                self.serial_manager.disconnect()
                self.connect_btn.setText('연결')
                self.start_btn.setEnabled(False)
                self.stop_btn.setEnabled(False)
                self.port_combo.setEnabled(True)
                self.refresh_btn.setEnabled(True)
            except Exception as e:
                QMessageBox.critical(self, '오류', f'해제 실패: {str(e)}')
                return

    def start_operation(self):
        """작업 시작"""
        try:
            self.serial_manager.start_monitoring()
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.data_text.append('작업이 시작되었습니다.')
        except Exception as e:
            QMessageBox.critical(self, '오류', f'작업 시작 실패: {str(e)}')

    def stop_operation(self):
        """작업 정지"""
        try:
            self.serial_manager.stop_monitoring()
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.data_text.append('작업이 정지되었습니다.')
        except Exception as e:
            QMessageBox.critical(self, '오류', f'작업 정지 실패: {str(e)}')

    def on_data_received(self, data):
        """데이터 수신 시 호출되는 콜백"""
        self.data_text.append(data)

    def closeEvent(self, event):
        """다이얼로그 종료 시 처리"""
        if self.serial_manager.is_port_open():
            try:
                self.serial_manager.disconnect()
            except:
                pass
        event.accept() 