import serial
import serial.tools.list_ports
from typing import List, Optional, Callable
import time

class SerialManager:
    def __init__(self):
        self.serial_port: Optional[serial.Serial] = None
        self.is_connected = False
        self.callback: Optional[Callable[[bytes], None]] = None
        self._stop_thread = False

    def get_available_ports(self) -> List[str]:
        """사용 가능한 시리얼 포트 목록을 반환"""
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports

    def connect(self, port: str, baud_rate: int = 115200, 
                data_bits: int = 8, stop_bits: float = 1.0,
                parity: str = 'N', timeout: float = 1.0) -> bool:
        """시리얼 포트에 연결"""
        try:
            if self.is_connected:
                self.disconnect()

            self.serial_port = serial.Serial(
                port=port,
                baudrate=baud_rate,
                bytesize=data_bits,
                stopbits=stop_bits,
                parity=parity,
                timeout=timeout
            )
            self.is_connected = True
            return True
        except Exception as e:
            print(f"시리얼 포트 연결 실패: {e}")
            self.is_connected = False
            return False

    def disconnect(self):
        """시리얼 포트 연결 해제"""
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            self.is_connected = False

    def send_data(self, data: bytes) -> bool:
        """데이터 전송"""
        if not self.is_connected:
            return False
        try:
            self.serial_port.write(data)
            return True
        except Exception as e:
            print(f"데이터 전송 실패: {e}")
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

    def set_callback(self, callback: Callable[[bytes], None]):
        """데이터 수신 콜백 함수 설정"""
        self.callback = callback

    def start_monitoring(self):
        """데이터 모니터링 시작"""
        if not self.is_connected or not self.callback:
            return

        self._stop_thread = False
        while not self._stop_thread:
            if self.serial_port.in_waiting:
                data = self.serial_port.read(self.serial_port.in_waiting)
                if data:
                    self.callback(data)
            time.sleep(0.01)

    def stop_monitoring(self):
        """데이터 모니터링 중지"""
        self._stop_thread = True

    def is_port_open(self) -> bool:
        """포트가 열려있는지 확인"""
        return self.is_connected and self.serial_port and self.serial_port.is_open

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