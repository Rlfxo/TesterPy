from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, 
                             QComboBox, QGroupBox, QFormLayout,
                             QMessageBox, QFileDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ...utils.settings_manager import SettingsManager
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('프로그램 설정')
        self.setWindowIcon(QIcon(resource_path('img/icon.png')))
        self.setGeometry(100, 100, 600, 400)

        # 메인 레이아웃
        layout = QVBoxLayout()
        self.setLayout(layout)

        # 시리얼 통신 설정 그룹
        serial_group = QGroupBox('시리얼 통신 설정')
        serial_layout = QFormLayout()
        
        # 포트 설정
        self.port_combo = QComboBox()
        self.port_combo.addItems(['COM1', 'COM2', 'COM3', 'COM4'])
        serial_layout.addRow('포트:', self.port_combo)
        
        # 통신 속도
        self.baud_combo = QComboBox()
        self.baud_combo.addItems(['9600', '19200', '38400', '57600', '115200'])
        serial_layout.addRow('통신 속도:', self.baud_combo)
        
        # 데이터 비트
        self.data_bits_combo = QComboBox()
        self.data_bits_combo.addItems(['7', '8'])
        serial_layout.addRow('데이터 비트:', self.data_bits_combo)
        
        # 정지 비트
        self.stop_bits_combo = QComboBox()
        self.stop_bits_combo.addItems(['1', '1.5', '2'])
        serial_layout.addRow('정지 비트:', self.stop_bits_combo)
        
        # 패리티
        self.parity_combo = QComboBox()
        self.parity_combo.addItems(['None', 'Even', 'Odd', 'Mark', 'Space'])
        serial_layout.addRow('패리티:', self.parity_combo)
        
        serial_group.setLayout(serial_layout)
        layout.addWidget(serial_group)

        # 파일 저장 설정 그룹
        file_group = QGroupBox('파일 저장 설정')
        file_layout = QFormLayout()
        
        # 저장 경로
        path_layout = QHBoxLayout()
        self.save_path_edit = QLineEdit()
        self.save_path_edit.setReadOnly(True)
        path_layout.addWidget(self.save_path_edit)
        
        browse_btn = QPushButton('찾아보기')
        browse_btn.clicked.connect(self.browse_save_path)
        path_layout.addWidget(browse_btn)
        
        file_layout.addRow('저장 경로:', path_layout)
        
        # 파일 형식
        self.file_format_combo = QComboBox()
        self.file_format_combo.addItems(['CSV', 'Excel', 'JSON'])
        file_layout.addRow('파일 형식:', self.file_format_combo)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # 버튼 영역
        button_layout = QHBoxLayout()
        
        # 저장 버튼
        save_btn = QPushButton('저장')
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        # 취소 버튼
        cancel_btn = QPushButton('취소')
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)

        # 현재 설정 로드
        self.load_settings()

    def load_settings(self):
        # 시리얼 설정 로드
        serial_settings = self.settings_manager.get_serial_settings()
        self.port_combo.setCurrentText(serial_settings['port'])
        self.baud_combo.setCurrentText(serial_settings['baud_rate'])
        self.data_bits_combo.setCurrentText(serial_settings['data_bits'])
        self.stop_bits_combo.setCurrentText(serial_settings['stop_bits'])
        self.parity_combo.setCurrentText(serial_settings['parity'])

        # 파일 설정 로드
        file_settings = self.settings_manager.get_file_settings()
        self.save_path_edit.setText(file_settings['save_path'])
        self.file_format_combo.setCurrentText(file_settings['format'])

    def browse_save_path(self):
        dir_path = QFileDialog.getExistingDirectory(
            self,
            "저장 경로 선택",
            self.save_path_edit.text()
        )
        if dir_path:
            self.save_path_edit.setText(dir_path)

    def save_settings(self):
        # 시리얼 설정 저장
        serial_settings = {
            'port': self.port_combo.currentText(),
            'baud_rate': self.baud_combo.currentText(),
            'data_bits': self.data_bits_combo.currentText(),
            'stop_bits': self.stop_bits_combo.currentText(),
            'parity': self.parity_combo.currentText()
        }
        self.settings_manager.update_serial_settings(serial_settings)

        # 파일 설정 저장
        file_settings = {
            'save_path': self.save_path_edit.text(),
            'format': self.file_format_combo.currentText()
        }
        self.settings_manager.update_file_settings(file_settings)

        QMessageBox.information(self, '알림', '설정이 저장되었습니다.')
        self.close() 