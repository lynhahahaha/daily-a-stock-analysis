#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
沪深 300 成分股获取脚本
数据源：东方财富 API
"""

import requests
import json
from datetime import datetime

def get_hs300_stocks():
    """获取沪深 300 成分股列表"""
    # 东方财富沪深 300 成分股 API
    url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
    params = {
        "reportName": "RPT_INDEX_COMPONENT",
        "columns": "SECURITY_CODE,SECURITY_NAME_ABBR,INDEX_CODE,INDEX_NAME",
        "filter": '(INDEX_CODE="000300.SH")',
        "pageSize": 500,
        "pageNumber": 1,
        "sortTypes": "-1",
        "sortColumns": "ADD_DATE"
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('success') and data.get('result'):
            stocks = data['result']['data']
            stock_list = []
            for stock in stocks:
                stock_list.append({
                    'code': stock['SECURITY_CODE'],
                    'name': stock['SECURITY_NAME_ABBR'],
                    'index': '沪深 300'
                })
            return stock_list
    
    except Exception as e:
        print(f"获取沪深 300 成分股失败：{e}")
    
    # 备用方案：返回一些常见的沪深 300 成分股
    fallback_stocks = [
        {'code': '600519', 'name': '贵州茅台', 'index': '沪深 300'},
        {'code': '000858', 'name': '五粮液', 'index': '沪深 300'},
        {'code': '601318', 'name': '中国平安', 'index': '沪深 300'},
        {'code': '600036', 'name': '招商银行', 'index': '沪深 300'},
        {'code': '000333', 'name': '美的集团', 'index': '沪深 300'},
        {'code': '601888', 'name': '中国中免', 'index': '沪深 300'},
        {'code': '002415', 'name': '海康威视', 'index': '沪深 300'},
        {'code': '600276', 'name': '恒瑞医药', 'index': '沪深 300'},
        {'code': '601398', 'name': '工商银行', 'index': '沪深 300'},
        {'code': '600900', 'name': '长江电力', 'index': '沪深 300'},
        {'code': '000651', 'name': '格力电器', 'index': '沪深 300'},
        {'code': '601166', 'name': '兴业银行', 'index': '沪深 300'},
        {'code': '600887', 'name': '伊利股份', 'index': '沪深 300'},
        {'code': '002594', 'name': '比亚迪', 'index': '沪深 300'},
        {'code': '601012', 'name': '隆基绿能', 'index': '沪深 300'},
    ]
    return fallback_stocks

def get_market_cap(stock_code):
    """获取市值（用于排序）"""
    try:
        # 新浪财经实时行情
        url = f"https://hq.sinajs.cn/sz{stock_code}" if stock_code.startswith('0') or stock_code.startswith('3') else f"https://hq.sinajs.cn/sh{stock_code}"
        response = requests.get(url, timeout=5)
        data = response.text
        if '=' in data:
            parts = data.split('=')[1].strip('"').split(',')
            if len(parts) > 20:
                # 总市值 = 股价 * 总股本
                price = float(parts[3]) if parts[3] else 0
                # 从东方财富获取更准确的市值
                return get_market_cap_eastmoney(stock_code)
    except:
        pass
    return 0

def get_market_cap_eastmoney(stock_code):
    """从东方财富获取市值"""
    try:
        suffix = ".SZ" if stock_code.startswith('0') or stock_code.startswith('3') else ".SH"
        url = "https://push2.eastmoney.com/api/qt/stock/get"
        params = {
            "secid": f"{stock_code}{suffix}",
            "fields": "f116"  # 总市值
        }
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        if data.get('data'):
            return data['data'].get('f116', 0)
    except:
        pass
    return 0

def main():
    print("正在获取沪深 300 成分股...")
    stocks = get_hs300_stocks()
    print(f"获取到 {len(stocks)} 只成分股")
    
    # 获取市值并排序
    print("正在获取市值数据...")
    for stock in stocks:
        market_cap = get_market_cap(stock['code'])
        stock['marketCap'] = market_cap
        print(f"  {stock['name']} ({stock['code']}): {market_cap/100000000:.2f}亿")
    
    # 按市值降序排序
    stocks.sort(key=lambda x: x.get('marketCap', 0), reverse=True)
    
    # 保存结果
    output_file = "/root/.openclaw/workspace/a-stock-analyzer/data/hs300_stocks.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(stocks, f, ensure_ascii=False, indent=2)
    
    print(f"\n已保存到：{output_file}")
    print(f"共 {len(stocks)} 家公司，将按市值顺序每天分析一家")

if __name__ == "__main__":
    main()
