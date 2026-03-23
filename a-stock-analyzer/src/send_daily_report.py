#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日 A 股分析报告发送脚本
执行分析并发送 QQ 提醒
"""

import subprocess
import sys
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace/a-stock-analyzer"
USER_ID = "0CE0E229BBAEF99D1E8835B3E07728DE"

def main():
    today = datetime.now().strftime('%Y-%m-%d')
    
    # 执行分析
    print(f"[{today}] 开始执行每日分析...")
    result = subprocess.run(
        ['python3', f'{WORKSPACE}/src/daily_runner.py'],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print(f"分析失败：{result.stderr}")
        return
    
    # 读取最新报告获取公司名
    try:
        with open(f'{WORKSPACE}/reports/daily-analysis.md', 'r', encoding='utf-8') as f:
            first_line = f.readline()
            # 提取公司名，如 "# 📊 贵州茅台 (600519) 深度分析报告"
            if '📊' in first_line and '(' in first_line:
                company = first_line.split('📊')[1].split('(')[0].strip()
                code = first_line.split('(')[1].split(')')[0].strip()
            else:
                company, code = "未知公司", "未知"
    except:
        company, code = "未知公司", "未知"
    
    print(f"✅ {today} 分析完成：{company}({code})")
    print(f"📄 报告：{WORKSPACE}/reports/daily-analysis.md")
    print(f"🔗 GitHub: https://github.com/lynhahahaha/daily-a-stock-analysis")

if __name__ == "__main__":
    main()
