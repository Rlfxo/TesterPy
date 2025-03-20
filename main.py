import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from src.ui.main_window import MainWindow

def main():
    # Windows에서 High DPI 스케일링 활성화
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Mac에서 IMKClient 로그 메시지 숨기기
    os.environ['QT_MAC_WANTS_LAYER'] = '1'
    
    app = QApplication(sys.argv)
    
    # Windows에서 기본 폰트 크기 조정
    if sys.platform == 'win32':
        font = app.font()
        font.setPointSize(9)  # Windows 기본 폰트 크기
        app.setFont(font)
    
    main_window = MainWindow()
    main_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
