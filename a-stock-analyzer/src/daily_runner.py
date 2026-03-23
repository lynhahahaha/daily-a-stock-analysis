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

def push_to_github():
    """推送到 GitHub"""
    print(f"\n{'='*60}")
    print("📤 推送到 GitHub...")
    print(f"{'='*60}\n")
    
    # 加载配置
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    repo_name = config['github']['repoName']
    repo_path = f"{WORKSPACE}/github_repos/{repo_name}"
    
    # 创建或克隆仓库
    github_dir = Path(repo_path)
    
    if not github_dir.exists():
        print(f"📁 创建仓库目录：{repo_path}")
        github_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化 git
        subprocess.run(['git', 'init'], cwd=repo_path, capture_output=True)
        subprocess.run(['git', 'remote', 'add', 'origin', f'https://github.com/openclaw-bot/{repo_name}.git'], 
                      cwd=repo_path, capture_output=True)
    
    # 复制最新报告
    daily_report = f"{REPORTS_DIR}/daily-analysis.md"
    if os.path.exists(daily_report):
        today = datetime.now().strftime('%Y-%m-%d')
        # 读取报告第一行获取公司名称
        with open(daily_report, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            # 提取公司名，如 "# 📊 贵州茅台 (600519) 深度分析报告"
            if '📊' in first_line and '(' in first_line:
                company = first_line.split('📊')[1].split('(')[0].strip()
                code = first_line.split('(')[1].split(')')[0].strip()
                dest_file = f"{repo_path}/reports/{today}-{company}-{code}.md"
            else:
                dest_file = f"{repo_path}/reports/{today}-analysis.md"
        Path(f"{repo_path}/reports").mkdir(parents=True, exist_ok=True)
        
        with open(daily_report, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 更新 README
        readme_content = f"""# 📊 每日 A 股深度分析

> 基于巴菲特投资哲学的 A 股公司深度分析报告

## 📅 最新报告

- [{today}](./reports/{today}-analysis.md) - {today}

## 📁 历史报告

查看所有 [历史报告](./reports/)

## 🎯 分析框架

本报告采用巴菲特价值投资哲学，重点关注：

1. **净资产收益率 (ROE)** - 巴菲特最看重的指标
2. **自由现金流** - 现金为王
3. **护城河** - 竞争优势
4. **管理层** - 诚信与能力
5. **估值** - 安全边际

## 📊 分析顺序

按照沪深 300 成分股当前市值排序，每天分析一家公司。

## ⏰ 更新时间

每日早上 7:00 前完成更新

---

*报告由 小财助手 自动生成*
*分析框架：巴菲特价值投资哲学*
*数据源：东方财富、新浪财经*
"""
        
        with open(f"{repo_path}/README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Git 操作
        subprocess.run(['git', 'add', '.'], cwd=repo_path, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'feat: add {today} analysis report'], 
                      cwd=repo_path, capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main', '-f'], 
                      cwd=repo_path, capture_output=True)
        
        print(f"✅ 已推送到 GitHub: https://github.com/openclaw-bot/{repo_name}")
        return True
    
    print("❌ 未找到报告文件")
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
    
    # 推送到 GitHub
    push_to_github()
    
    print(f"\n{'='*60}")
    print("✅ 所有任务完成！")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
