import json
import os
from pathlib import Path

class SettingsManager:
    def __init__(self):
        self.settings_file = 'config/settings.json'
        self.default_settings = {
            'serial': {
                'port': 'COM1',
                'baud_rate': '115200',
                'data_bits': '8',
                'stop_bits': '1',
                'parity': 'None'
            },
            'file': {
                'save_path': str(Path.home() / 'Documents' / 'EVAR'),
                'format': 'CSV'
            }
        }
        self.ensure_config_dir()
        self.load_settings()

    def ensure_config_dir(self):
        """설정 파일이 저장될 디렉토리가 존재하는지 확인하고 없으면 생성"""
        config_dir = os.path.dirname(self.settings_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

    def load_settings(self):
        """설정 파일을 로드하거나 기본 설정을 사용"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    self.settings = json.load(f)
            else:
                self.settings = self.default_settings.copy()
                self.save_settings()
        except Exception as e:
            print(f"설정 파일 로드 중 오류 발생: {e}")
            self.settings = self.default_settings.copy()

    def save_settings(self):
        """현재 설정을 파일로 저장"""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"설정 파일 저장 중 오류 발생: {e}")

    def get_serial_settings(self):
        """시리얼 통신 설정 반환"""
        return self.settings.get('serial', self.default_settings['serial'])

    def get_file_settings(self):
        """파일 저장 설정 반환"""
        return self.settings.get('file', self.default_settings['file'])

    def update_serial_settings(self, settings):
        """시리얼 통신 설정 업데이트"""
        self.settings['serial'] = settings
        self.save_settings()

    def update_file_settings(self, settings):
        """파일 저장 설정 업데이트"""
        self.settings['file'] = settings
        self.save_settings() 