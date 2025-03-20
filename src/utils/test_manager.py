import os
import json
from datetime import datetime, timedelta
import random
from pathlib import Path

class TestManager:
    def __init__(self):
        self.data_dir = Path('data')
        self.ensure_data_dir()
        self.test_items = {
            '전압': {'unit': 'V', 'reference': 3.3, 'tolerance': 0.1},
            '전류': {'unit': 'mA', 'reference': 100, 'tolerance': 5},
            '온도': {'unit': '°C', 'reference': 25, 'tolerance': 2},
            '저항': {'unit': 'Ω', 'reference': 1000, 'tolerance': 50}
        }

    def ensure_data_dir(self):
        """데이터 디렉토리 생성"""
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True)

    def run_test(self, test_item):
        """테스트 실행"""
        if test_item not in self.test_items:
            raise ValueError(f'알 수 없는 테스트 항목: {test_item}')
            
        item_info = self.test_items[test_item]
        reference = item_info['reference']
        tolerance = item_info['tolerance']
        
        # 테스트 측정값 생성 (실제로는 장비에서 측정)
        measured = reference + (random.random() - 0.5) * tolerance * 2
        
        # 오차율 계산
        error = abs(measured - reference) / reference * 100
        
        # 결과 판정
        result = 'PASS' if error <= (tolerance / reference * 100) else 'FAIL'
        
        return {
            'test_item': test_item,
            'measured_value': measured,
            'reference_value': reference,
            'error': error,
            'result': result,
            'unit': item_info['unit']
        }

    def save_test_results(self, results):
        """테스트 결과 저장"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        test_data = {
            'timestamp': timestamp,
            'results': results
        }
        
        filepath = self.data_dir / f'test_{timestamp}.json'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, ensure_ascii=False, indent=2)
            
        return str(filepath)

    def get_test_history(self, test_type=None, start_date=None):
        """테스트 이력 조회"""
        history = []
        
        # JSON 파일 목록 조회
        json_files = sorted(self.data_dir.glob('test_*.json'), reverse=True)
        
        for file in json_files:
            with open(file, 'r', encoding='utf-8') as f:
                test_data = json.load(f)
                
            test_date = datetime.strptime(test_data['timestamp'][:8], '%Y%m%d').date()
            
            # 날짜 필터 적용
            if start_date and test_date < start_date:
                continue
                
            # 테스트 유형 필터 적용
            for result in test_data['results']:
                if test_type and result['test_item'] != test_type:
                    continue
                    
                history.append({
                    'timestamp': test_data['timestamp'],
                    'test_item': result['test_item'],
                    'measured_value': result['measured_value'],
                    'reference_value': result['reference_value'],
                    'error': result['error'],
                    'result': result['result']
                })
                
        return history

    def get_test_detail(self, test_id):
        """테스트 상세 정보 조회"""
        filepath = self.data_dir / f'test_{test_id}.json'
        if not filepath.exists():
            return None
            
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    def delete_test(self, test_id):
        """테스트 삭제"""
        filepath = self.data_dir / f'test_{test_id}.json'
        if filepath.exists():
            filepath.unlink()
            return True
        return False

    def get_test_statistics(self, period='day'):
        """테스트 통계 조회"""
        # 시작 날짜 설정
        if period == 'day':
            start_date = datetime.now().date()
        elif period == 'week':
            start_date = datetime.now().date() - timedelta(days=7)
        elif period == 'month':
            start_date = datetime.now().date() - timedelta(days=30)
        else:
            start_date = None
            
        # 테스트 이력 조회
        history = self.get_test_history(start_date=start_date)
        
        # 통계 계산
        total_tests = len(history)
        total_passed = sum(1 for test in history if test['result'] == 'PASS')
        total_failed = total_tests - total_passed
        
        # 테스트 유형별 통계
        test_types = {}
        for test in history:
            test_item = test['test_item']
            if test_item not in test_types:
                test_types[test_item] = {
                    'count': 0,
                    'passed': 0,
                    'failed': 0,
                    'pass_rate': 0
                }
                
            stats = test_types[test_item]
            stats['count'] += 1
            if test['result'] == 'PASS':
                stats['passed'] += 1
            else:
                stats['failed'] += 1
            stats['pass_rate'] = (stats['passed'] / stats['count']) * 100
            
        # 일별 통계
        daily_stats = {}
        for test in history:
            date = test['timestamp'][:8]  # YYYYMMDD
            if date not in daily_stats:
                daily_stats[date] = {
                    'date': date,
                    'total': 0,
                    'passed': 0,
                    'failed': 0,
                    'pass_rate': 0
                }
                
            stats = daily_stats[date]
            stats['total'] += 1
            if test['result'] == 'PASS':
                stats['passed'] += 1
            else:
                stats['failed'] += 1
            stats['pass_rate'] = (stats['passed'] / stats['total']) * 100
            
        return {
            'total_tests': total_tests,
            'total_passed': total_passed,
            'total_failed': total_failed,
            'average_pass_rate': (total_passed / total_tests * 100) if total_tests > 0 else 0,
            'test_types': test_types,
            'daily_stats': sorted(daily_stats.values(), key=lambda x: x['date'], reverse=True)
        } 