#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化 GitHub 仓库
"""

import subprocess
import os
from pathlib import Path
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace/a-stock-analyzer"
REPO_NAME = "daily-a-stock-analysis"
REPO_PATH = f"{WORKSPACE}/github_repos/{REPO_NAME}"

def init_github_repo():
    """初始化 GitHub 仓库"""
    print(f"\n{'='*60}")
    print(f"📦 初始化 GitHub 仓库：{REPO_NAME}")
    print(f"{'='*60}\n")
    
    repo_path = Path(REPO_PATH)
    
    if repo_path.exists():
        print(f"仓库目录已存在：{repo_path}")
        return
    
    # 创建目录
    repo_path.mkdir(parents=True, exist_ok=True)
    print(f"✅ 创建目录：{repo_path}")
    
    # 初始化 git
    subprocess.run(['git', 'init'], cwd=REPO_PATH, capture_output=True)
    print("✅ Git 仓库初始化")
    
    # 创建 README
    readme = f"""# 📊 每日 A 股深度分析

> 基于巴菲特投资哲学的 A 股公司深度分析报告

## 🎯 项目说明

本项目每天分析一家沪深 300 成分股公司，采用巴菲特价值投资哲学框架：

1. **净资产收益率 (ROE)** - 巴菲特最看重的指标
2. **自由现金流** - 现金为王
3. **护城河** - 竞争优势
4. **管理层** - 诚信与能力
5. **估值** - 安全边际

## 📅 最新报告

- [{datetime.now().strftime('%Y-%m-%d')}](./reports/) - 查看最新分析

## 📁 目录结构

```
daily-a-stock-analysis/
├── README.md           # 本文件
├── reports/            # 每日分析报告
│   ├── 2026-03-10_600519_贵州茅台.md
│   └── ...
└── ...
```

## 📊 分析顺序

按照沪深 300 成分股当前市值排序，每天分析一家公司，约 300 天完成一轮。

## ⏰ 更新时间

每日早上 7:00 前自动更新

## 🤖 自动化

本报告由 **小财助手** 自动生成，使用以下技术栈：
- Python 3
- 巴菲特价值投资分析框架
- 数据源：akshare / 东方财富 / 新浪财经

## 📈 投资等级说明

| 等级 | 含义 | 建议 |
|------|------|------|
| 🟢 A | 强烈推荐 | ROE>20%, 现金流健康，护城河宽 |
| 🟡 B | 值得关注 | 部分指标符合，需观察 |
| 🔴 C | 谨慎对待 | 不符合巴菲特标准 |

---

> ⚠️ **免责声明**: 本报告基于公开数据自动生成，不构成投资建议。投资有风险，决策需谨慎。

*报告由 小财助手 自动生成*
*分析框架：巴菲特价值投资哲学*
"""
    
    with open(f"{REPO_PATH}/README.md", 'w', encoding='utf-8') as f:
        f.write(readme)
    print("✅ 创建 README.md")
    
    # 创建 reports 目录
    reports_dir = repo_path / "reports"
    reports_dir.mkdir(exist_ok=True)
    print("✅ 创建 reports 目录")
    
    # 复制最新报告
    daily_report = f"{WORKSPACE}/reports/daily-analysis.md"
    if os.path.exists(daily_report):
        today = datetime.now().strftime('%Y-%m-%d')
        dest = reports_dir / f"{today}-analysis.md"
        with open(daily_report, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(dest, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ 复制最新报告：{dest}")
    
    # Git 提交
    subprocess.run(['git', 'add', '.'], cwd=REPO_PATH, capture_output=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit: daily A-stock analysis reports'], 
                  cwd=REPO_PATH, capture_output=True)
    print("✅ 首次 Git 提交")
    
    print(f"\n📂 仓库已初始化：{REPO_PATH}")
    print(f"\n⚠️  注意：需要手动设置 GitHub remote 并推送")
    print(f"   cd {REPO_PATH}")
    print(f"   git remote add origin https://github.com/YOUR_USERNAME/{REPO_NAME}.git")
    print(f"   git push -u origin main")

if __name__ == "__main__":
    init_github_repo()
