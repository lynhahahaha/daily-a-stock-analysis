#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
推送到 Gitee 仓库的脚本
"""
import os
import base64
import requests
from pathlib import Path

GITEE_OWNER = "lynhahaha"
GITEE_REPO = "daily-a-stock-analysis"
GITEE_TOKEN = "b0f57aab37ed4d3b6e49f96c7e7b2f98"
GITEE_API = "https://gitee.com/api/v5"

WORKSPACE = "/root/.openclaw/workspace"
REPORTS_DIR = f"{WORKSPACE}/reports"

def get_file_sha(path):
    """获取文件在 Gitee 上的 SHA"""
    url = f"{GITEE_API}/repos/{GITEE_OWNER}/{GITEE_REPO}/contents/{path}"
    params = {"access_token": GITEE_TOKEN}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        # 如果是目录返回 None
        if isinstance(data, list):
            return None
        return data.get("sha")
    return None

def create_or_update_file(path, content, message):
    """创建或更新文件"""
    # 检查文件是否存在
    sha = get_file_sha(path)
    
    url = f"{GITEE_API}/repos/{GITEE_OWNER}/{GITEE_REPO}/contents/{path}"
    data = {
        "access_token": GITEE_TOKEN,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8'),
        "message": message,
        "branch": "main"
    }
    
    # 只有文件存在时才需要 sha（更新操作）
    if sha:
        data["sha"] = sha
        # 更新文件
        resp = requests.put(url, params={"access_token": GITEE_TOKEN}, json=data)
    else:
        # 创建新文件（不需要 sha）
        data.pop("sha", None)
        resp = requests.post(url, params={"access_token": GITEE_TOKEN}, json=data)
    
    if resp.status_code in [200, 201]:
        print(f"✅ 推送成功：{path}")
        return True
    else:
        print(f"❌ 推送失败：{path} - {resp.text}")
        return False

def main():
    # 推送最新报告
    reports = list(Path(REPORTS_DIR).glob("*.md"))
    if not reports:
        print("❌ 未找到报告文件")
        return
    
    # 推送最新的报告
    latest_report = max(reports, key=lambda p: p.stat().st_mtime)
    print(f"📄 推送报告：{latest_report.name}")
    
    with open(latest_report, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 推送到 reports 目录
    gitee_path = f"reports/{latest_report.name}"
    create_or_update_file(gitee_path, content, f"feat: add {latest_report.stem}")
    
    # 更新 README
    readme = """# 📊 每日 A 股深度分析

> 基于巴菲特投资哲学的 A 股公司深度分析报告

## 📅 最新报告

查看 [reports](./reports/) 目录获取最新分析报告

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

每日早上 7:30 自动更新

---

*报告由 小财助手 自动生成*
*分析框架：巴菲特价值投资哲学*
*数据源：东方财富、新浪财经*

## 🔗 仓库地址

https://gitee.com/lynhahaha/daily-a-stock-analysis
"""
    create_or_update_file("README.md", readme, "feat: update README")

if __name__ == "__main__":
    main()
