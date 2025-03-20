import serial
import serial.tools.list_ports
from threading import Thread, Event
from typing import Optional
import time

class SerialManager:
    def __init__(self):
        self.serial_port = None
        self.monitoring = False
        self.monitor_thread = None
        self.stop_event = Event()
        self.data_callback = None
        
    def get_available_ports(self):
        """사용 가능한 시리얼 포트 목록 반환"""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports
        
    def connect(self, port, baudrate=9600):
        """시리얼 포트 연결"""
        try:
            self.serial_port = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=1
            )
            return True
        except Exception as e:
            print(f"연결 오류: {str(e)}")
            self.serial_port = None
            raise
            
    def disconnect(self):
        """시리얼 포트 연결 해제"""
        if self.serial_port:
            self.stop_monitoring()
            self.serial_port.close()
            self.serial_port = None
            
    def is_port_open(self):
        """포트 연결 상태 확인"""
        return self.serial_port is not None and self.serial_port.is_open
        
    def set_callback(self, callback):
        """데이터 수신 콜백 설정"""
        self.data_callback = callback
        
    def start_monitoring(self):
        """데이터 모니터링 시작"""
        if not self.is_port_open():
            raise Exception("포트가 연결되지 않았습니다.")
            
        if self.monitoring:
            return
            
        self.monitoring = True
        self.stop_event.clear()
        self.monitor_thread = Thread(target=self._monitor_data)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """데이터 모니터링 정지"""
        self.monitoring = False
        if self.monitor_thread:
            self.stop_event.set()
            self.monitor_thread.join()
            self.monitor_thread = None
            
    def _monitor_data(self):
        """데이터 모니터링 스레드"""
        while self.monitoring and not self.stop_event.is_set():
            if self.serial_port.in_waiting:
                try:
                    data = self.serial_port.readline().decode('utf-8').strip()
                    if data and self.data_callback:
                        self.data_callback(data)
                except Exception as e:
                    print(f"데이터 수신 오류: {str(e)}")
            time.sleep(0.1)  # CPU 사용량 감소
            
    def send_data(self, data):
        """데이터 전송"""
        if not self.is_port_open():
            raise Exception("포트가 연결되지 않았습니다.")
            
        try:
            if isinstance(data, str):
                data = data.encode('utf-8')
            self.serial_port.write(data)
            return True
        except Exception as e:
            print(f"전송 오류: {str(e)}")
            return False

    def read_data(self, size: int = 1024) -> Optional[bytes]:
        """데이터 수신"""
        if not self.is_connected:
            return None
        try:
            if self.serial_port.in_waiting:
                return self.serial_port.read(size)
            return None
        except Exception as e:
            print(f"데이터 수신 실패: {e}")
            return None

    def get_port_info(self) -> dict:
        """현재 포트 정보 반환"""
        if not self.is_connected or not self.serial_port:
            return {}
        
        return {
            'port': self.serial_port.port,
            'baudrate': self.serial_port.baudrate,
            'bytesize': self.serial_port.bytesize,
            'stopbits': self.serial_port.stopbits,
            'parity': self.serial_port.parity,
            'timeout': self.serial_port.timeout
        } 