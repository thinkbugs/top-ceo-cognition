#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增长模型计算工具
提供AARRR增长模型、用户增长预测、收入增长预测、同期群分析、漏斗分析

使用方法：
1. 命令行调用：python growth_calculator.py --method aarrr --acquisition 1000 --activation 800 --retention 600 --revenue 400 --referral 200
2. Python模块调用：
   from growth_calculator import GrowthCalculator
   calculator = GrowthCalculator()
   result = calculator.calculate_aarrr(acquisition=1000, activation=800, retention=600, revenue=400, referral=200)
"""

import argparse
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class GrowthResult:
    """增长分析结果数据类"""
    success: bool
    method: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    recommendations: Optional[List[str]] = None


class GrowthCalculator:
    """增长模型计算器"""
    
    def __init__(self):
        self.version = "1.0.0"
    
    def calculate_aarrr(self, acquisition: int, activation: int, retention: int,
                       revenue: int, referral: int) -> GrowthResult:
        """
        计算AARRR增长模型（获取、激活、留存、变现、推荐）
        
        参数:
            acquisition: 获取用户数
            activation: 激活用户数
            retention: 留存用户数
            revenue: 付费用户数
            referral: 推荐用户数
        
        返回:
            GrowthResult对象
        """
        try:
            if acquisition <= 0:
                return GrowthResult(False, "AARRR", None, error="获取用户数必须大于0")
            
            # 计算各阶段转化率
            activation_rate = (activation / acquisition) * 100 if acquisition > 0 else 0
            retention_rate = (retention / activation) * 100 if activation > 0 else 0
            revenue_rate = (revenue / retention) * 100 if retention > 0 else 0
            referral_rate = (referral / revenue) * 100 if revenue > 0 else 0
            
            # 计算总体转化率
            overall_conversion = (revenue / acquisition) * 100 if acquisition > 0 else 0
            
            # 生成建议
            recommendations = []
            if activation_rate < 40:
                recommendations.append(f"激活率较低({activation_rate:.1f}%)，建议优化onboarding流程")
            if retention_rate < 30:
                recommendations.append(f"留存率较低({retention_rate:.1f}%)，建议改进产品体验")
            if revenue_rate < 10:
                recommendations.append(f"变现率较低({revenue_rate:.1f}%)，建议优化定价策略")
            if referral_rate < 20:
                recommendations.append(f"推荐率较低({referral_rate:.1f}%)，建议设计推荐激励")
            
            return GrowthResult(
                success=True,
                method="AARRR",
                result={
                    "acquisition": acquisition,
                    "activation": activation,
                    "retention": retention,
                    "revenue": revenue,
                    "referral": referral
                },
                details={
                    "activation_rate": activation_rate,
                    "retention_rate": retention_rate,
                    "revenue_rate": revenue_rate,
                    "referral_rate": referral_rate,
                    "overall_conversion": overall_conversion
                },
                recommendations=recommendations
            )
            
        except Exception as e:
            return GrowthResult(False, "AARRR", None, error=str(e))
    
    def predict_user_growth(self, initial_users: int, monthly_growth_rate: float,
                           months: int, churn_rate: Optional[float] = None) -> GrowthResult:
        """
        预测用户增长
        
        参数:
            initial_users: 初始用户数
            monthly_growth_rate: 月增长率（小数，如0.1表示10%）
            months: 预测月数
            churn_rate: 月流失率（可选）
        
        返回:
            GrowthResult对象
        """
        try:
            if initial_users <= 0:
                return GrowthResult(False, "User Growth Prediction", None, 
                                   error="初始用户数必须大于0")
            
            if months <= 0:
                return GrowthResult(False, "User Growth Prediction", None, 
                                   error="预测月数必须大于0")
            
            if monthly_growth_rate < 0:
                return GrowthResult(False, "User Growth Prediction", None, 
                                   error="增长率不能为负")
            
            # 预测用户增长
            growth_predictions = []
            current_users = initial_users
            
            for month in range(1, months + 1):
                if churn_rate is not None:
                    # 考虑流失率
                    new_users = current_users * monthly_growth_rate
                    churned_users = current_users * churn_rate
                    current_users = current_users + new_users - churned_users
                else:
                    # 不考虑流失率
                    current_users = current_users * (1 + monthly_growth_rate)
                
                growth_predictions.append({
                    "month": month,
                    "users": round(current_users, 2),
                    "growth_from_initial": ((current_users - initial_users) / initial_users) * 100
                })
            
            return GrowthResult(
                success=True,
                method="User Growth Prediction",
                result={
                    "initial_users": initial_users,
                    "final_users": round(current_users, 2),
                    "total_growth": ((current_users - initial_users) / initial_users) * 100,
                    "months": months
                },
                details={
                    "monthly_growth_rate": monthly_growth_rate,
                    "churn_rate": churn_rate,
                    "predictions": growth_predictions
                }
            )
            
        except Exception as e:
            return GrowthResult(False, "User Growth Prediction", None, error=str(e))
    
    def predict_revenue_growth(self, initial_revenue: float, monthly_growth_rate: float,
                              months: int) -> GrowthResult:
        """
        预测收入增长
        
        参数:
            initial_revenue: 初始收入
            monthly_growth_rate: 月增长率（小数）
            months: 预测月数
        
        返回:
            GrowthResult对象
        """
        try:
            if initial_revenue <= 0:
                return GrowthResult(False, "Revenue Growth Prediction", None, 
                                   error="初始收入必须大于0")
            
            if months <= 0:
                return GrowthResult(False, "Revenue Growth Prediction", None, 
                                   error="预测月数必须大于0")
            
            if monthly_growth_rate < 0:
                return GrowthResult(False, "Revenue Growth Prediction", None, 
                                   error="增长率不能为负")
            
            # 预测收入增长
            revenue_predictions = []
            current_revenue = initial_revenue
            
            for month in range(1, months + 1):
                current_revenue = current_revenue * (1 + monthly_growth_rate)
                revenue_predictions.append({
                    "month": month,
                    "revenue": round(current_revenue, 2),
                    "growth_from_initial": ((current_revenue - initial_revenue) / initial_revenue) * 100
                })
            
            return GrowthResult(
                success=True,
                method="Revenue Growth Prediction",
                result={
                    "initial_revenue": initial_revenue,
                    "final_revenue": round(current_revenue, 2),
                    "total_growth": ((current_revenue - initial_revenue) / initial_revenue) * 100,
                    "months": months
                },
                details={
                    "monthly_growth_rate": monthly_growth_rate,
                    "predictions": revenue_predictions
                }
            )
            
        except Exception as e:
            return GrowthResult(False, "Revenue Growth Prediction", None, error=str(e))
    
    def analyze_cohort(self, cohort_data: Dict[str, List[int]]) -> GrowthResult:
        """
        同期群分析
        
        参数:
            cohort_data: 同期群数据字典
                {"2024-01": [1000, 600, 400, 300], ...}
                每个列表代表：初始用户数，第1月留存，第2月留存，第3月留存...
        
        返回:
            GrowthResult对象
        """
        try:
            if not cohort_data:
                return GrowthResult(False, "Cohort Analysis", None, 
                                   error="同期群数据不能为空")
            
            cohort_analysis = {}
            
            for cohort_name, data in cohort_data.items():
                if not data:
                    continue
                
                initial_users = data[0]
                retention_rates = []
                
                for i in range(1, len(data)):
                    if initial_users > 0:
                        retention_rate = (data[i] / initial_users) * 100
                    else:
                        retention_rate = 0
                    retention_rates.append({
                        "month": i,
                        "retention_count": data[i],
                        "retention_rate": round(retention_rate, 2)
                    })
                
                cohort_analysis[cohort_name] = {
                    "initial_users": initial_users,
                    "retention_rates": retention_rates
                }
            
            # 计算平均留存率
            avg_retention_rates = []
            max_months = max(len(data) for data in cohort_data.values()) - 1
            
            for month in range(1, max_months + 1):
                rates = []
                for cohort_name, data in cohort_data.items():
                    if len(data) > month:
                        rates.append(data[month] / data[0] * 100)
                if rates:
                    avg_retention_rates.append({
                        "month": month,
                        "avg_retention_rate": round(sum(rates) / len(rates), 2)
                    })
            
            return GrowthResult(
                success=True,
                method="Cohort Analysis",
                result={
                    "cohort_count": len(cohort_data),
                    "max_months": max_months
                },
                details={
                    "cohort_analysis": cohort_analysis,
                    "average_retention_rates": avg_retention_rates
                }
            )
            
        except Exception as e:
            return GrowthResult(False, "Cohort Analysis", None, error=str(e))
    
    def analyze_funnel(self, funnel_steps: Dict[str, int]) -> GrowthResult:
        """
        漏斗分析
        
        参数:
            funnel_steps: 漏斗步骤字典
                {"访问": 10000, "注册": 5000, "激活": 3000, "付费": 1000}
        
        返回:
            GrowthResult对象
        """
        try:
            if not funnel_steps or len(funnel_steps) < 2:
                return GrowthResult(False, "Funnel Analysis", None, 
                                   error="漏斗步骤数据不能为空且至少需要2个步骤")
            
            steps = list(funnel_steps.keys())
            funnel_analysis = []
            
            prev_count = None
            for i, step in enumerate(steps):
                count = funnel_steps[step]
                
                if i == 0:
                    conversion_rate = 100.0
                    dropoff_rate = 0.0
                else:
                    conversion_rate = (count / prev_count) * 100 if prev_count > 0 else 0
                    dropoff_rate = 100 - conversion_rate
                
                funnel_analysis.append({
                    "step": i + 1,
                    "name": step,
                    "count": count,
                    "conversion_rate": round(conversion_rate, 2),
                    "dropoff_rate": round(dropoff_rate, 2)
                })
                
                prev_count = count
            
            # 计算总体转化率
            first_count = funnel_steps[steps[0]]
            last_count = funnel_steps[steps[-1]]
            overall_conversion = (last_count / first_count) * 100 if first_count > 0 else 0
            
            # 生成建议
            recommendations = []
            max_dropoff_step = max(funnel_analysis[1:], key=lambda x: x["dropoff_rate"])
            if max_dropoff_step["dropoff_rate"] > 50:
                recommendations.append(f"最大流失步骤: {max_dropoff_step['name']} (流失率{max_dropoff_step['dropoff_rate']:.1f}%)，建议优化")
            
            if overall_conversion < 5:
                recommendations.append(f"总体转化率较低({overall_conversion:.1f}%)，建议优化整个漏斗")
            
            return GrowthResult(
                success=True,
                method="Funnel Analysis",
                result={
                    "steps_count": len(steps),
                    "overall_conversion": round(overall_conversion, 2)
                },
                details={
                    "funnel_analysis": funnel_analysis,
                    "first_step": steps[0],
                    "last_step": steps[-1],
                    "first_count": first_count,
                    "last_count": last_count
                },
                recommendations=recommendations
            )
            
        except Exception as e:
            return GrowthResult(False, "Funnel Analysis", None, error=str(e))


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description="增长模型计算工具")
    parser.add_argument("--method", type=str, required=True,
                       choices=["aarrr", "user_growth", "revenue_growth", "cohort", "funnel"],
                       help="计算方法")
    
    # AARRR参数
    parser.add_argument("--acquisition", type=int, help="获取用户数")
    parser.add_argument("--activation", type=int, help="激活用户数")
    parser.add_argument("--retention", type=int, help="留存用户数")
    parser.add_argument("--revenue", type=int, help="付费用户数")
    parser.add_argument("--referral", type=int, help="推荐用户数")
    
    # 用户增长预测参数
    parser.add_argument("--initial_users", type=int, help="初始用户数")
    parser.add_argument("--monthly_growth_rate", type=float, help="月增长率（小数）")
    parser.add_argument("--months", type=int, help="预测月数")
    parser.add_argument("--churn_rate", type=float, help="月流失率（小数）")
    
    # 收入增长预测参数
    parser.add_argument("--initial_revenue", type=float, help="初始收入")
    
    args = parser.parse_args()
    
    calculator = GrowthCalculator()
    result = None
    
    if args.method == "aarrr":
        if args.acquisition is None or args.activation is None or args.retention is None or \
           args.revenue is None or args.referral is None:
            print("错误: AARRR方法需要--acquisition、--activation、--retention、--revenue和--referral参数")
            sys.exit(1)
        
        result = calculator.calculate_aarrr(
            acquisition=args.acquisition,
            activation=args.activation,
            retention=args.retention,
            revenue=args.revenue,
            referral=args.referral
        )
    
    elif args.method == "user_growth":
        if args.initial_users is None or args.monthly_growth_rate is None or args.months is None:
            print("错误: 用户增长预测需要--initial_users、--monthly_growth_rate和--months参数")
            sys.exit(1)
        
        result = calculator.predict_user_growth(
            initial_users=args.initial_users,
            monthly_growth_rate=args.monthly_growth_rate,
            months=args.months,
            churn_rate=args.churn_rate
        )
    
    elif args.method == "revenue_growth":
        if args.initial_revenue is None or args.monthly_growth_rate is None or args.months is None:
            print("错误: 收入增长预测需要--initial_revenue、--monthly_growth_rate和--months参数")
            sys.exit(1)
        
        result = calculator.predict_revenue_growth(
            initial_revenue=args.initial_revenue,
            monthly_growth_rate=args.monthly_growth_rate,
            months=args.months
        )
    
    elif args.method == "cohort":
        print("错误: 同期群分析不支持命令行调用，请使用Python模块调用")
        sys.exit(1)
    
    elif args.method == "funnel":
        print("错误: 漏斗分析不支持命令行调用，请使用Python模块调用")
        sys.exit(1)
    
    # 输出结果
    if result.success:
        print(f"\n✓ {result.method} 计算成功")
        print(f"结果: {result.result}")
        if result.details:
            print(f"\n详细信息:")
            for key, value in result.details.items():
                if key in ["predictions", "cohort_analysis", "funnel_analysis"]:
                    print(f"  {key}:")
                    for item in value:
                        print(f"    {item}")
                else:
                    print(f"  {key}: {value}")
        if result.recommendations:
            print(f"\n建议:")
            for rec in result.recommendations:
                print(f"  - {rec}")
    else:
        print(f"\n✗ {result.method} 计算失败")
        print(f"错误: {result.error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
