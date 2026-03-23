# 📊 小财助手 - 每日 A 股深度分析系统

> 基于巴菲特投资哲学的自动化股票分析系统

## 🎯 项目简介

本系统每天自动分析一家沪深 300 成分股公司，采用巴菲特价值投资哲学框架，生成深度分析报告并推送到 GitHub。

## 📁 目录结构

```
a-stock-analyzer/
├── config.json              # 系统配置
├── cron_config.json         # 定时任务配置
├── src/                     # 源代码
│   ├── fetch_stocks.py      # 获取沪深 300 成分股
│   ├── analyze_stock.py     # 公司分析核心脚本
│   ├── daily_runner.py      # 每日调度脚本
│   └── init_github.py       # GitHub 仓库初始化
├── data/                    # 数据缓存
│   ├── hs300_stocks.json    # 沪深 300 成分股列表
│   └── progress.json        # 分析进度
├── reports/                 # 生成的报告
│   ├── daily-analysis.md    # 最新日报
│   └── YYYY-MM-DD_代码_公司.md
└── github_repos/            # GitHub 仓库本地副本
    └── daily-a-stock-analysis/
```

## 🚀 快速开始

### 1. 初始化股票列表

```bash
cd /root/.openclaw/workspace/a-stock-analyzer
python3 src/fetch_stocks.py
```

### 2. 手动测试分析

```bash
# 使用演示数据（推荐首次使用）
python3 src/analyze_stock.py 600519 贵州茅台 demo

# 使用实时数据（需要安装 akshare）
pip install akshare
python3 src/analyze_stock.py 600519 贵州茅台 live
```

### 3. 初始化 GitHub 仓库

```bash
python3 src/init_github.py

# 然后手动推送到 GitHub
cd github_repos/daily-a-stock-analysis
git remote add origin https://github.com/YOUR_USERNAME/daily-a-stock-analysis.git
git push -u origin main
```

### 4. 设置定时任务

定时任务配置已保存在 `cron_config.json`，需要在 OpenClaw 中注册：

- **时间**: 每天 07:00 (Asia/Shanghai)
- **任务**: 执行 `daily_runner.py`
- **通知**: 完成后发送 QQ 消息提醒

## 📊 分析框架

### 核心指标

1. **净资产收益率 (ROE)** - 巴菲特最看重的指标
   - 优秀：>20%
   - 良好：>15%
   - 一般：>10%

2. **自由现金流 (FCF)** - 现金为王
   - 持续为正表示公司造血能力强

3. **护城河评分** - 综合评估
   - 基于 ROE、现金流、负债率等

4. **业务构成** - 营收来源分析
   - 主营业务占比
   - 各业务毛利率

### 投资等级

| 等级 | 含义 | 标准 |
|------|------|------|
| 🟢 A | 强烈推荐 | ROE>20%, FCF>0, 负债安全 |
| 🟡 B | 值得关注 | 部分指标符合 |
| 🔴 C | 谨慎对待 | 不符合巴菲特标准 |

## 📈 数据源

### 演示模式（默认）
- 使用内置的历史近似数据
- 适合测试和演示
- 无需 API key

### 实时模式
- **akshare** (推荐): `pip install akshare`
- **tushare**: 需要 API key
- **东方财富 API**: 需要特殊请求头

## 🔧 配置说明

### config.json

```json
{
  "github": {
    "repoName": "daily-a-stock-analysis",
    "visibility": "public"
  },
  "stockPool": "hs300",
  "schedule": {
    "timezone": "Asia/Shanghai",
    "runTime": "07:00"
  }
}
```

### 添加更多公司数据

编辑 `src/analyze_stock.py` 中的 `DEMO_DATA` 字典，添加新公司的历史数据。

## 📝 报告示例

报告采用 Markdown 格式，包含：

- 公司概览（市值、PE、PB 等）
- ROE 历史趋势（5 年）
- 现金流分析（5 年）
- 营收利润增长
- 业务构成
- 巴菲特投资评估
- 投资建议

## ⚠️ 免责声明

- 本报告基于公开数据自动生成
- **不构成投资建议**
- 投资有风险，决策需谨慎
- 演示数据为历史近似值，仅供参考

## 🤖 小财助手

本系统由 **小财助手** 驱动，采用巴菲特价值投资哲学框架。

---

*最后更新：2026-03-10*
