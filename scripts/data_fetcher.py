#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外部数据获取脚本
集成多个公开API，获取财经数据、新闻数据、市场数据

使用方法：
1. Python模块调用：
   from data_fetcher import DataFetcher
   fetcher = DataFetcher()
   result = fetcher.get_stock_data("AAPL")
"""

import json
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class FetchResult:
    """数据获取结果数据类"""
    success: bool
    data_source: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class DataFetcher:
    """外部数据获取器"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.timeout = 30
        
        # API配置（示例配置，实际使用需要替换为真实API密钥）
        self.apis = {
            "yahoo_finance": {
                "base_url": "https://query1.finance.yahoo.com/v8/finance/chart/",
                "enabled": True
            },
            "alpha_vantage": {
                "base_url": "https://www.alphavantage.co/query",
                "api_key": "YOUR_API_KEY",  # 需要替换为真实API密钥
                "enabled": False  # 需要API密钥才能启用
            },
            "news_api": {
                "base_url": "https://newsapi.org/v2/everything",
                "api_key": "YOUR_API_KEY",  # 需要替换为真实API密钥
                "enabled": False  # 需要API密钥才能启用
            }
        }
    
    def get_stock_data(self, symbol: str, period: str = "1y") -> FetchResult:
        """
        获取股票数据
        
        参数:
            symbol: 股票代码（如 "AAPL", "GOOGL"）
            period: 时间周期（"1d", "1w", "1m", "1y"）
        
        返回:
            FetchResult对象
        """
        try:
            # 使用Yahoo Finance API（不需要API密钥）
            url = f"{self.apis['yahoo_finance']['base_url']}{symbol}"
            params = {
                "interval": "1d",
                "range": period
            }
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            
            if response.status_code != 200:
                return FetchResult(
                    success=False,
                    data_source="yahoo_finance",
                    result=None,
                    error=f"API请求失败，状态码: {response.status_code}"
                )
            
            data = response.json()
            
            # 解析数据
            chart_data = data.get("chart", {}).get("result", [{}])[0]
            meta = chart_data.get("meta", {})
            timestamp = chart_data.get("timestamp", [])
            indicators = chart_data.get("indicators", {})
            
            # 提取价格数据
            quote = indicators.get("quote", [{}])[0]
            
            if not timestamp:
                return FetchResult(
                    success=False,
                    data_source="yahoo_finance",
                    result=None,
                    error="未找到股票数据"
                )
            
            # 构建结果
            price_data = []
            for i, ts in enumerate(timestamp):
                price_data.append({
                    "date": datetime.fromtimestamp(ts).strftime("%Y-%m-%d"),
                    "open": quote["open"][i],
                    "high": quote["high"][i],
                    "low": quote["low"][i],
                    "close": quote["close"][i],
                    "volume": quote["volume"][i]
                })
            
            # 提取元数据
            result = {
                "symbol": symbol,
                "company_name": meta.get("longName", ""),
                "current_price": meta.get("regularMarketPrice", 0),
                "previous_close": meta.get("previousClose", 0),
                "change": meta.get("regularMarketPrice", 0) - meta.get("previousClose", 0),
                "change_percent": ((meta.get("regularMarketPrice", 0) - meta.get("previousClose", 0)) / 
                                 meta.get("previousClose", 1)) * 100,
                "market_cap": meta.get("marketCap", 0),
                "volume": meta.get("regularMarketVolume", 0),
                "52_week_high": meta.get("fiftyTwoWeekHigh", 0),
                "52_week_low": meta.get("fiftyTwoWeekLow", 0),
                "price_history": price_data
            }
            
            return FetchResult(
                success=True,
                data_source="yahoo_finance",
                result=result,
                details={
                    "data_points": len(price_data),
                    "period": period,
                    "retrieved_at": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return FetchResult(
                success=False,
                data_source="yahoo_finance",
                result=None,
                error=str(e)
            )
    
    def get_financial_data(self, symbol: str) -> FetchResult:
        """
        获取财务数据
        
        参数:
            symbol: 股票代码
        
        返回:
            FetchResult对象
        """
        try:
            # 模拟财务数据（实际应该从API获取）
            # 这里返回示例数据，实际使用时需要集成真实的财务数据API
            
            result = {
                "symbol": symbol,
                "revenue": {
                    "annual": [
                        {"year": "2023", "value": 383.29e9},
                        {"year": "2022", "value": 365.82e9},
                        {"year": "2021", "value": 365.82e9},
                        {"year": "2020", "value": 274.52e9},
                        {"year": "2019", "value": 260.17e9}
                    ]
                },
                "net_income": {
                    "annual": [
                        {"year": "2023", "value": 99.80e9},
                        {"year": "2022", "value": 94.68e9},
                        {"year": "2021", "value": 94.68e9},
                        {"year": "2020", "value": 57.41e9},
                        {"year": "2019", "value": 55.26e9}
                    ]
                },
                "total_assets": {
                    "annual": [
                        {"year": "2023", "value": 352.58e9},
                        {"year": "2022", "value": 352.76e9}
                    ]
                },
                "total_liabilities": {
                    "annual": [
                        {"year": "2023", "value": 290.44e9},
                        {"year": "2022", "value": 302.08e9}
                    ]
                },
                "cash_flow": {
                    "operating": 99.58e9,
                    "investing": -11.11e9,
                    "financing": -10.73e9,
                    "free": 88.47e9
                }
            }
            
            return FetchResult(
                success=True,
                data_source="simulated",
                result=result,
                details={
                    "note": "这是模拟数据，实际使用时需要集成真实的财务数据API"
                }
            )
            
        except Exception as e:
            return FetchResult(
                success=False,
                data_source="simulated",
                result=None,
                error=str(e)
            )
    
    def get_company_news(self, symbol: str, limit: int = 10) -> FetchResult:
        """
        获取公司新闻
        
        参数:
            symbol: 股票代码
            limit: 返回数量限制
        
        返回:
            FetchResult对象
        """
        try:
            # 模拟新闻数据（实际应该从API获取）
            
            result = {
                "symbol": symbol,
                "news": [
                    {
                        "title": f"{symbol} 发布季度财报，营收超出预期",
                        "date": "2024-01-01",
                        "source": "财经新闻",
                        "url": "https://example.com/news/1",
                        "summary": f"{symbol} 公司发布最新季度财报，营收和利润均超出分析师预期，股价应声上涨。"
                    },
                    {
                        "title": f"{symbol} 宣布重大战略调整",
                        "date": "2024-01-02",
                        "source": "行业观察",
                        "url": "https://example.com/news/2",
                        "summary": f"{symbol} 宣布进行重大战略调整，将重点投入新兴市场，预计未来三年将投资10亿美元。"
                    }
                ]
            }
            
            # 限制返回数量
            result["news"] = result["news"][:limit]
            
            return FetchResult(
                success=True,
                data_source="simulated",
                result=result,
                details={
                    "news_count": len(result["news"]),
                    "note": "这是模拟数据，实际使用时需要集成真实的新闻API"
                }
            )
            
        except Exception as e:
            return FetchResult(
                success=False,
                data_source="simulated",
                result=None,
                error=str(e)
            )
    
    def get_market_trends(self, market: str = "US") -> FetchResult:
        """
        获取市场趋势
        
        参数:
            market: 市场类型（"US", "CN", "EU"）
        
        返回:
            FetchResult对象
        """
        try:
            # 模拟市场趋势数据
            
            result = {
                "market": market,
                "trends": {
                    "index": {
                        "S&P 500": {"current": 4783.35, "change": 0.52, "change_percent": 1.09},
                        "NASDAQ": {"current": 14963.87, "change": 65.00, "change_percent": 0.44},
                        "DOW JONES": {"current": 37654.33, "change": 158.83, "change_percent": 0.42}
                    },
                    "sectors": {
                        "Technology": {"change_percent": 1.2},
                        "Healthcare": {"change_percent": 0.5},
                        "Finance": {"change_percent": -0.3},
                        "Energy": {"change_percent": 2.1},
                        "Consumer": {"change_percent": 0.8}
                    },
                    "sentiment": "positive",
                    "risk_level": "low"
                }
            }
            
            return FetchResult(
                success=True,
                data_source="simulated",
                result=result,
                details={
                    "note": "这是模拟数据，实际使用时需要集成真实的市场数据API"
                }
            )
            
        except Exception as e:
            return FetchResult(
                success=False,
                data_source="simulated",
                result=None,
                error=str(e)
            )
    
    def get_competitor_data(self, symbol: str) -> FetchResult:
        """
        获取竞争对手数据
        
        参数:
            symbol: 股票代码
        
        返回:
            FetchResult对象
        """
        try:
            # 模拟竞争对手数据
            
            competitors = {
                "AAPL": ["MSFT", "GOOGL", "AMZN", "META"],
                "MSFT": ["AAPL", "GOOGL", "AMZN", "META"],
                "GOOGL": ["AAPL", "MSFT", "META", "AMZN"]
            }
            
            competitor_symbols = competitors.get(symbol, [])
            
            result = {
                "symbol": symbol,
                "competitors": competitor_symbols,
                "comparison": []
            }
            
            for comp_symbol in competitor_symbols:
                # 模拟竞争对手数据
                result["comparison"].append({
                    "symbol": comp_symbol,
                    "market_cap": "1000B",
                    "pe_ratio": 25.5,
                    "revenue_growth": 10.2
                })
            
            return FetchResult(
                success=True,
                data_source="simulated",
                result=result,
                details={
                    "competitor_count": len(competitor_symbols),
                    "note": "这是模拟数据，实际使用时需要集成真实的竞争对手数据API"
                }
            )
            
        except Exception as e:
            return FetchResult(
                success=False,
                data_source="simulated",
                result=None,
                error=str(e)
            )


if __name__ == "__main__":
    # 示例使用
    fetcher = DataFetcher()
    
    # 获取股票数据
    print("\n获取股票数据:")
    result = fetcher.get_stock_data("AAPL", period="1mo")
    if result.success:
        print(f"✓ 获取成功")
        print(f"公司: {result.result['company_name']}")
        print(f"当前价格: ${result.result['current_price']}")
        print(f"涨跌: {result.result['change']:.2f} ({result.result['change_percent']:.2f}%)")
        print(f"数据点: {result.details['data_points']}个")
    else:
        print(f"✗ 获取失败: {result.error}")
    
    # 获取财务数据
    print("\n获取财务数据:")
    result = fetcher.get_financial_data("AAPL")
    if result.success:
        print(f"✓ 获取成功")
        revenue = result.result['revenue']['annual'][0]
        print(f"最新营收: ${revenue['value']/1e9:.2f}B ({revenue['year']})")
    else:
        print(f"✗ 获取失败: {result.error}")
    
    # 获取公司新闻
    print("\n获取公司新闻:")
    result = fetcher.get_company_news("AAPL", limit=2)
    if result.success:
        print(f"✓ 获取成功")
        for news in result.result['news']:
            print(f"  - {news['title']}")
    else:
        print(f"✗ 获取失败: {result.error}")
    
    # 获取市场趋势
    print("\n获取市场趋势:")
    result = fetcher.get_market_trends("US")
    if result.success:
        print(f"✓ 获取成功")
        print(f"市场情绪: {result.result['trends']['sentiment']}")
        print(f"风险水平: {result.result['trends']['risk_level']}")
    else:
        print(f"✗ 获取失败: {result.error}")
