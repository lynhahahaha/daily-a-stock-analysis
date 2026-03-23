#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日 A 股分析主调度脚本
1. 读取公司列表和当前进度
2. 分析下一家公司
3. 推送到 GitHub
4. 发送 QQ 提醒
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = "/root/.openclaw/workspace/a-stock-analyzer"
DATA_FILE = f"{WORKSPACE}/data/hs300_stocks.json"
PROGRESS_FILE = f"{WORKSPACE}/data/progress.json"
REPORTS_DIR = f"{WORKSPACE}/reports"
CONFIG_FILE = f"{WORKSPACE}/config.json"

def load_progress() -> dict:
    """加载分析进度"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'currentIndex': 0,
        'lastAnalyzeDate': None,
        'totalStocks': 0,
    }

def save_progress(progress: dict):
    """保存分析进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def load_stocks() -> list:
    """加载股票列表"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def analyze_today():
    """执行今日分析"""
    print(f"\n{'='*60}")
    print(f"📊 每日 A 股分析 - {datetime.now().strftime('%Y-%m-%d')}")
    print(f"{'='*60}\n")
    
    # 加载数据
    stocks = load_stocks()
    progress = load_progress()
    
    if not stocks:
        print("❌ 未找到股票列表，请先运行 fetch_stocks.py")
        return False
    
    progress['totalStocks'] = len(stocks)
    
    # 检查是否需要新分析（每天只分析一次）
    today = datetime.now().strftime('%Y-%m-%d')
    if progress.get('lastAnalyzeDate') == today:
        print(f"✅ 今日已完成分析：{stocks[progress['currentIndex']]['name']}")
        print(f"   报告位置：{REPORTS_DIR}/daily-analysis.md")
        return True
    
    # 获取今天要分析的公司
    current_index = progress.get('currentIndex', 0)
    if current_index >= len(stocks):
        print("🎉 恭喜！已完成所有沪深 300 成分股分析")
        print("   将重新开始第一轮分析...")
        current_index = 0
    
    stock = stocks[current_index]
    code = stock['code']
    name = stock['name']
    
    print(f"📈 今日分析目标：{name}({code})")
    print(f"   进度：{current_index + 1}/{len(stocks)}")
    print(f"   市值排名：{current_index + 1}")
    
    # 执行分析
    analyze_script = f"{WORKSPACE}/src/analyze_stock.py"
    try:
        result = subprocess.run(
            ['python3', analyze_script, code, name],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"❌ 分析失败：{result.stderr}")
            return False
        
        print(result.stdout)
        
    except subprocess.TimeoutExpired:
        print("❌ 分析超时")
        return False
    except Exception as e:
        print(f"❌ 分析异常：{e}")
        return False
    
    # 更新进度
    progress['currentIndex'] = current_index + 1
    progress['lastAnalyzeDate'] = today
    save_progress(progress)
    
    print(f"\n✅ 今日分析完成！")
    print(f"   下一家：{stocks[current_index + 1]['name'] if current_index + 1 < len(stocks) else '重新开始第一轮'}")
    
    return True

def push_to_gitee():
    """推送到 Gitee - 使用 Python API"""
    print(f"\n{'='*60}")
    print("📤 推送到 Gitee...")
    print(f"{'='*60}\n")
    
    # 使用 Python 脚本推送到 Gitee
    push_script = f"{WORKSPACE}/../scripts/push_to_gitee.py"
    if os.path.exists(push_script):
        result = subprocess.run(['python3', push_script], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ 推送失败：{result.stderr}")
            return False
        return True
    else:
        print(f"❌ 未找到推送脚本：{push_script}")
        return False

def main():
    """主函数"""
    print(f"\n{'='*60}")
    print(f"🤖 小财助手 - 每日 A 股分析系统")
    print(f"{'='*60}")
    
    # 执行分析
    if not analyze_today():
        print("\n❌ 分析失败，退出")
        sys.exit(1)
    
    # 推送到 Gitee
    push_to_gitee()
    
    print(f"\n{'='*60}")
    print("✅ 所有任务完成！")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
