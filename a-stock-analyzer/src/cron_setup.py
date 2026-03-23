#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设置定时任务配置
生成 cron 配置和提醒配置
"""

import json
from datetime import datetime

WORKSPACE = "/root/.openclaw/workspace/a-stock-analyzer"
USER_ID = "0CE0E229BBAEF99D1E8835B3E07728DE"

# 每天 7 点的 cron 表达式 (分 时 日 月 周)
CRON_EXPR = "0 7 * * *"

cron_config = {
    "name": "daily-a-stock-analysis",
    "description": "每日 A 股深度分析 - 巴菲特投资哲学",
    "schedule": {
        "kind": "cron",
        "expr": CRON_EXPR,
        "tz": "Asia/Shanghai"
    },
    "task": {
        "command": "python3 /root/.openclaw/workspace/a-stock-analyzer/src/daily_runner.py",
        "cwd": WORKSPACE,
        "timeout": 300
    },
    "notification": {
        "enabled": True,
        "channel": "qqbot",
        "to": USER_ID,
        "message": "📊 小财助手：今日 A 股分析报告已生成！\n\n查看报告：https://github.com/YOUR_USERNAME/daily-a-stock-analysis\n\n今天分析的公司已推送到 GitHub，欢迎查看～"
    }
}

# 保存配置
with open(f"{WORKSPACE}/cron_config.json", 'w', encoding='utf-8') as f:
    json.dump(cron_config, f, ensure_ascii=False, indent=2)

print("✅ 定时任务配置已保存")
print(f"   文件：{WORKSPACE}/cron_config.json")
print(f"   时间：每天 07:00 (Asia/Shanghai)")
print(f"\n⚠️  需要在 OpenClaw 中注册此定时任务")
