import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

class VisualizationManager:
    def __init__(self):
        self.graph_dir = Path('data/graphs')
        self.ensure_graph_dir()

    def ensure_graph_dir(self):
        """그래프 저장 디렉토리 생성"""
        if not self.graph_dir.exists():
            self.graph_dir.mkdir(parents=True)

    def create_test_summary_graph(self, stats: Dict[str, Any]) -> str:
        """테스트 요약 그래프 생성"""
        plt.figure(figsize=(10, 6))
        
        # 테스트 유형별 통과율
        test_types = list(stats['test_types'].keys())
        pass_rates = [stats['test_types'][t]['pass_rate'] for t in test_types]
        
        plt.bar(test_types, pass_rates)
        plt.title('테스트 유형별 통과율')
        plt.xlabel('테스트 유형')
        plt.ylabel('통과율 (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # 그래프 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = self.graph_dir / f"test_summary_{timestamp}.png"
        plt.savefig(filepath)
        plt.close()
        
        return str(filepath)

    def create_daily_trend_graph(self, stats: Dict[str, Any]) -> str:
        """일별 추이 그래프 생성"""
        plt.figure(figsize=(12, 6))
        
        # 일별 데이터 준비
        dates = [stat['date'] for stat in stats['daily_stats']]
        pass_rates = [stat['pass_rate'] for stat in stats['daily_stats']]
        
        # 날짜 형식 변환
        dates = [f"{d[:4]}-{d[4:6]}-{d[6:]}" for d in dates]
        
        plt.plot(dates, pass_rates, marker='o')
        plt.title('일별 테스트 통과율 추이')
        plt.xlabel('날짜')
        plt.ylabel('통과율 (%)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        
        # 그래프 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = self.graph_dir / f"daily_trend_{timestamp}.png"
        plt.savefig(filepath)
        plt.close()
        
        return str(filepath)

    def create_test_distribution_graph(self, stats: Dict[str, Any]) -> str:
        """테스트 분포 그래프 생성"""
        plt.figure(figsize=(10, 6))
        
        # 테스트 유형별 분포
        test_types = list(stats['test_types'].keys())
        counts = [stats['test_types'][t]['count'] for t in test_types]
        
        plt.pie(counts, labels=test_types, autopct='%1.1f%%')
        plt.title('테스트 유형별 분포')
        
        # 그래프 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = self.graph_dir / f"test_distribution_{timestamp}.png"
        plt.savefig(filepath)
        plt.close()
        
        return str(filepath)

    def create_test_result_graph(self, test_data: Dict[str, Any]) -> str:
        """개별 테스트 결과 그래프 생성"""
        plt.figure(figsize=(12, 6))
        
        # 테스트 결과 데이터 준비
        test_items = [r['test_item'] for r in test_data['results']]
        measured_values = [r['measured_value'] for r in test_data['results']]
        reference_values = [r['reference_value'] for r in test_data['results']]
        
        # 막대 그래프 생성
        x = range(len(test_items))
        width = 0.35
        
        plt.bar([i - width/2 for i in x], measured_values, width, label='측정값')
        plt.bar([i + width/2 for i in x], reference_values, width, label='기준값')
        
        plt.title('테스트 항목별 측정값과 기준값 비교')
        plt.xlabel('테스트 항목')
        plt.ylabel('값')
        plt.xticks(x, test_items, rotation=45)
        plt.legend()
        plt.tight_layout()
        
        # 그래프 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filepath = self.graph_dir / f"test_result_{timestamp}.png"
        plt.savefig(filepath)
        plt.close()
        
        return str(filepath) 