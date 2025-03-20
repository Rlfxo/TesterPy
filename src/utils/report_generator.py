import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
import pandas as pd
import jinja2

class ReportGenerator:
    def __init__(self):
        self.report_dir = Path('data/reports')
        self.ensure_report_dir()
        self.template_dir = Path('templates')
        self.ensure_template_dir()

    def ensure_report_dir(self):
        """리포트 저장 디렉토리 생성"""
        if not self.report_dir.exists():
            self.report_dir.mkdir(parents=True)

    def ensure_template_dir(self):
        """템플릿 디렉토리 생성"""
        if not self.template_dir.exists():
            self.template_dir.mkdir(parents=True)
            self.create_default_template()

    def create_default_template(self):
        """기본 HTML 템플릿 생성"""
        template = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>테스트 리포트 - {{ test_type }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .summary {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 30px;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }
        .summary-item {
            text-align: center;
            padding: 15px;
            background-color: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .summary-item h3 {
            margin: 0;
            color: #666;
        }
        .summary-item p {
            margin: 10px 0 0;
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .pass {
            color: #28a745;
        }
        .fail {
            color: #dc3545;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #eee;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>테스트 리포트</h1>
            <p>테스트 유형: {{ test_type }}</p>
            <p>생성 시간: {{ timestamp }}</p>
        </div>

        <div class="summary">
            <h2>테스트 요약</h2>
            <div class="summary-grid">
                <div class="summary-item">
                    <h3>전체 테스트</h3>
                    <p>{{ total_tests }}</p>
                </div>
                <div class="summary-item">
                    <h3>통과</h3>
                    <p class="pass">{{ passed_tests }}</p>
                </div>
                <div class="summary-item">
                    <h3>실패</h3>
                    <p class="fail">{{ failed_tests }}</p>
                </div>
                <div class="summary-item">
                    <h3>통과율</h3>
                    <p>{{ "%.1f"|format(pass_rate) }}%</p>
                </div>
            </div>
        </div>

        <h2>상세 결과</h2>
        <table>
            <thead>
                <tr>
                    <th>테스트 항목</th>
                    <th>측정값</th>
                    <th>기준값</th>
                    <th>단위</th>
                    <th>결과</th>
                </tr>
            </thead>
            <tbody>
                {% for result in results %}
                <tr>
                    <td>{{ result.test_item }}</td>
                    <td>{{ "%.2f"|format(result.measured_value) }}</td>
                    <td>{{ "%.2f"|format(result.reference_value) }}</td>
                    <td>{{ result.unit }}</td>
                    <td class="{{ result.result.lower() }}">{{ result.result }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>

        <div class="footer">
            <p>EVAR Tool - 테스트 리포트</p>
            <p>생성 시간: {{ timestamp }}</p>
        </div>
    </div>
</body>
</html>
"""
        template_path = self.template_dir / 'report_template.html'
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template)

    def generate_report(self, test_data: Dict[str, Any]) -> str:
        """테스트 리포트 생성"""
        if not test_data or 'results' not in test_data:
            return None

        # 테스트 요약 정보 계산
        total_tests = len(test_data['results'])
        passed_tests = sum(1 for r in test_data['results'] if r['result'] == 'PASS')
        failed_tests = total_tests - passed_tests
        pass_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        # 템플릿 로드
        template_path = self.template_dir / 'report_template.html'
        with open(template_path, 'r', encoding='utf-8') as f:
            template = jinja2.Template(f.read())

        # 리포트 데이터 준비
        report_data = {
            'test_type': test_data['test_type'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'pass_rate': pass_rate,
            'results': test_data['results']
        }

        # 리포트 생성
        html_content = template.render(**report_data)

        # 리포트 파일 저장
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"report_{test_data['test_type']}_{timestamp}.html"
        filepath = self.report_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return str(filepath) 