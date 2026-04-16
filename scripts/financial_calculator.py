#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务决策计算工具
提供顶级CEO常用的财务决策计算方法：DCF、IRR、ROI、LTV/CAC、NPV、盈亏平衡点

使用方法：
1. 命令行调用：python financial_calculator.py --method dcf --cash_flows 100,200,300 --discount_rate 0.1
2. Python模块调用：
   from financial_calculator import FinancialCalculator
   calculator = FinancialCalculator()
   result = calculator.calculate_dcf(cash_flows=[100, 200, 300], discount_rate=0.1)
"""

import argparse
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class CalculationResult:
    """计算结果数据类"""
    success: bool
    method: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class FinancialCalculator:
    """财务决策计算器"""
    
    def __init__(self):
        self.version = "1.0.0"
    
    def calculate_dcf(self, cash_flows: List[float], discount_rate: float, 
                     terminal_growth_rate: Optional[float] = None,
                     terminal_value: Optional[float] = None) -> CalculationResult:
        """
        计算折现现金流（DCF）
        
        参数:
            cash_flows: 未来现金流列表 [year1, year2, ...]
            discount_rate: 折现率（小数，如0.1表示10%）
            terminal_growth_rate: 终值增长率（可选）
            terminal_value: 终值（可选）
        
        返回:
            CalculationResult对象
        """
        try:
            if not cash_flows:
                return CalculationResult(False, "DCF", None, error="现金流不能为空")
            
            if discount_rate < 0 or discount_rate > 1:
                return CalculationResult(False, "DCF", None, error="折现率必须在0到1之间")
            
            # 计算每期现金流的现值
            pv_flows = []
            for i, cf in enumerate(cash_flows, 1):
                pv = cf / ((1 + discount_rate) ** i)
                pv_flows.append({
                    "year": i,
                    "cash_flow": cf,
                    "present_value": pv
                })
            
            # 计算终值现值
            pv_terminal = 0
            terminal_year = len(cash_flows)
            if terminal_growth_rate is not None:
                last_cf = cash_flows[-1]
                terminal_value = last_cf * (1 + terminal_growth_rate) / (discount_rate - terminal_growth_rate)
                pv_terminal = terminal_value / ((1 + discount_rate) ** terminal_year)
            elif terminal_value is not None:
                pv_terminal = terminal_value / ((1 + discount_rate) ** terminal_year)
            
            # 计算DCF总和
            dcf_value = sum(pv["present_value"] for pv in pv_flows) + pv_terminal
            
            return CalculationResult(
                success=True,
                method="DCF",
                result=dcf_value,
                details={
                    "discount_rate": discount_rate,
                    "pv_flows": pv_flows,
                    "pv_terminal": pv_terminal,
                    "terminal_value": terminal_value,
                    "terminal_growth_rate": terminal_growth_rate,
                    "total_pv_without_terminal": sum(pv["present_value"] for pv in pv_flows)
                }
            )
            
        except Exception as e:
            return CalculationResult(False, "DCF", None, error=str(e))
    
    def calculate_irr(self, cash_flows: List[float], max_iterations: int = 1000, 
                     tolerance: float = 1e-6) -> CalculationResult:
        """
        计算内部收益率（IRR）
        使用牛顿迭代法求解
        
        参数:
            cash_flows: 现金流列表（包含初始投资，如[-100, 20, 30, 40]）
            max_iterations: 最大迭代次数
            tolerance: 容差
        
        返回:
            CalculationResult对象
        """
        try:
            if not cash_flows:
                return CalculationResult(False, "IRR", None, error="现金流不能为空")
            
            # 牛顿迭代法求解IRR
            rate = 0.1  # 初始猜测
            for iteration in range(max_iterations):
                npv = 0
                dnpv = 0
                for i, cf in enumerate(cash_flows):
                    if i == 0:
                        npv += cf
                        dnpv -= cf / (1 + rate)
                    else:
                        npv += cf / ((1 + rate) ** i)
                        dnpv -= i * cf / ((1 + rate) ** (i + 1))
                
                if dnpv == 0:
                    break
                
                new_rate = rate - npv / dnpv
                
                if abs(new_rate - rate) < tolerance:
                    rate = new_rate
                    break
                
                rate = new_rate
            
            return CalculationResult(
                success=True,
                method="IRR",
                result=rate,
                details={
                    "irr_percentage": rate * 100,
                    "iterations": iteration + 1
                }
            )
            
        except Exception as e:
            return CalculationResult(False, "IRR", None, error=str(e))
    
    def calculate_roi(self, initial_investment: float, final_value: float, 
                     time_period: float) -> CalculationResult:
        """
        计算投资回报率（ROI）
        
        参数:
            initial_investment: 初始投资
            final_value: 最终价值
            time_period: 投资期限（年）
        
        返回:
            CalculationResult对象
        """
        try:
            if initial_investment <= 0:
                return CalculationResult(False, "ROI", None, error="初始投资必须大于0")
            
            if time_period <= 0:
                return CalculationResult(False, "ROI", None, error="投资期限必须大于0")
            
            # 计算ROI
            profit = final_value - initial_investment
            roi = (profit / initial_investment) * 100
            
            # 计算年化ROI
            annualized_roi = ((final_value / initial_investment) ** (1 / time_period) - 1) * 100
            
            return CalculationResult(
                success=True,
                method="ROI",
                result={
                    "roi_percentage": roi,
                    "profit": profit,
                    "annualized_roi_percentage": annualized_roi
                },
                details={
                    "initial_investment": initial_investment,
                    "final_value": final_value,
                    "time_period": time_period
                }
            )
            
        except Exception as e:
            return CalculationResult(False, "ROI", None, error=str(e))
    
    def calculate_ltv_cac(self, average_revenue_per_user: float, 
                          customer_lifetime_months: float,
                          monthly_churn_rate: float,
                          cac: float) -> CalculationResult:
        """
        计算LTV（客户生命周期价值）和LTV/CAC比率
        
        参数:
            average_revenue_per_user: 平均每用户月收入
            customer_lifetime_months: 客户生命周期（月）
            monthly_churn_rate: 月流失率（小数，如0.05表示5%）
            cac: 获客成本
        
        返回:
            CalculationResult对象
        """
        try:
            if average_revenue_per_user <= 0:
                return CalculationResult(False, "LTV/CAC", None, error="平均收入必须大于0")
            
            if cac <= 0:
                return CalculationResult(False, "LTV/CAC", None, error="获客成本必须大于0")
            
            if monthly_churn_rate <= 0 or monthly_churn_rate >= 1:
                return CalculationResult(False, "LTV/CAC", None, error="流失率必须在0到1之间")
            
            # 计算LTV（使用简单方法）
            ltv_simple = average_revenue_per_user * customer_lifetime_months
            
            # 计算LTV（使用流失率方法）
            ltv_churn = average_revenue_per_user / monthly_churn_rate
            
            # 计算LTV/CAC比率
            ltv_cac_ratio = ltv_churn / cac
            
            return CalculationResult(
                success=True,
                method="LTV/CAC",
                result={
                    "ltv_simple": ltv_simple,
                    "ltv_churn": ltv_churn,
                    "ltv_cac_ratio": ltv_cac_ratio,
                    "is_healthy": ltv_cac_ratio >= 3  # LTV/CAC >= 3为健康
                },
                details={
                    "average_revenue_per_user": average_revenue_per_user,
                    "customer_lifetime_months": customer_lifetime_months,
                    "monthly_churn_rate": monthly_churn_rate,
                    "cac": cac
                }
            )
            
        except Exception as e:
            return CalculationResult(False, "LTV/CAC", None, error=str(e))
    
    def calculate_npv(self, cash_flows: List[float], discount_rate: float) -> CalculationResult:
        """
        计算净现值（NPV）
        
        参数:
            cash_flows: 现金流列表（包含初始投资，如[-100, 20, 30, 40]）
            discount_rate: 折现率（小数）
        
        返回:
            CalculationResult对象
        """
        try:
            if not cash_flows:
                return CalculationResult(False, "NPV", None, error="现金流不能为空")
            
            npv = 0
            pv_details = []
            
            for i, cf in enumerate(cash_flows):
                pv = cf / ((1 + discount_rate) ** i)
                npv += pv
                pv_details.append({
                    "period": i,
                    "cash_flow": cf,
                    "present_value": pv
                })
            
            return CalculationResult(
                success=True,
                method="NPV",
                result=npv,
                details={
                    "discount_rate": discount_rate,
                    "pv_details": pv_details,
                    "is_profitable": npv > 0
                }
            )
            
        except Exception as e:
            return CalculationResult(False, "NPV", None, error=str(e))
    
    def calculate_break_even(self, fixed_costs: float, variable_cost_per_unit: float,
                           selling_price_per_unit: float) -> CalculationResult:
        """
        计算盈亏平衡点
        
        参数:
            fixed_costs: 固定成本
            variable_cost_per_unit: 单位可变成本
            selling_price_per_unit: 单位售价
        
        返回:
            CalculationResult对象
        """
        try:
            if fixed_costs < 0:
                return CalculationResult(False, "Break-Even", None, error="固定成本不能为负")
            
            if variable_cost_per_unit < 0:
                return CalculationResult(False, "Break-Even", None, error="可变成本不能为负")
            
            if selling_price_per_unit <= 0:
                return CalculationResult(False, "Break-Even", None, error="售价必须大于0")
            
            if selling_price_per_unit <= variable_cost_per_unit:
                return CalculationResult(False, "Break-Even", None, 
                                       error="售价必须大于可变成本")
            
            # 计算盈亏平衡点（数量）
            contribution_margin = selling_price_per_unit - variable_cost_per_unit
            break_even_units = fixed_costs / contribution_margin
            
            # 计算盈亏平衡点（收入）
            break_even_revenue = break_even_units * selling_price_per_unit
            
            return CalculationResult(
                success=True,
                method="Break-Even",
                result={
                    "break_even_units": break_even_units,
                    "break_even_revenue": break_even_revenue,
                    "contribution_margin": contribution_margin,
                    "contribution_margin_ratio": contribution_margin / selling_price_per_unit
                },
                details={
                    "fixed_costs": fixed_costs,
                    "variable_cost_per_unit": variable_cost_per_unit,
                    "selling_price_per_unit": selling_price_per_unit
                }
            )
            
        except Exception as e:
            return CalculationResult(False, "Break-Even", None, error=str(e))


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description="财务决策计算工具")
    parser.add_argument("--method", type=str, required=True,
                       choices=["dcf", "irr", "roi", "ltv_cac", "npv", "break_even"],
                       help="计算方法")
    
    # DCF参数
    parser.add_argument("--cash_flows", type=str, help="现金流，用逗号分隔（如100,200,300）")
    parser.add_argument("--discount_rate", type=float, help="折现率（小数，如0.1表示10%）")
    parser.add_argument("--terminal_growth_rate", type=float, help="终值增长率")
    parser.add_argument("--terminal_value", type=float, help="终值")
    
    # IRR参数
    parser.add_argument("--max_iterations", type=int, default=1000, help="最大迭代次数")
    
    # ROI参数
    parser.add_argument("--initial_investment", type=float, help="初始投资")
    parser.add_argument("--final_value", type=float, help="最终价值")
    parser.add_argument("--time_period", type=float, help="投资期限（年）")
    
    # LTV/CAC参数
    parser.add_argument("--average_revenue_per_user", type=float, help="平均每用户月收入")
    parser.add_argument("--customer_lifetime_months", type=float, help="客户生命周期（月）")
    parser.add_argument("--monthly_churn_rate", type=float, help="月流失率（小数）")
    parser.add_argument("--cac", type=float, help="获客成本")
    
    # 盈亏平衡点参数
    parser.add_argument("--fixed_costs", type=float, help="固定成本")
    parser.add_argument("--variable_cost_per_unit", type=float, help="单位可变成本")
    parser.add_argument("--selling_price_per_unit", type=float, help="单位售价")
    
    args = parser.parse_args()
    
    calculator = FinancialCalculator()
    result = None
    
    if args.method == "dcf":
        if not args.cash_flows or args.discount_rate is None:
            print("错误: DCF方法需要--cash_flows和--discount_rate参数")
            sys.exit(1)
        
        cash_flows = [float(x) for x in args.cash_flows.split(",")]
        result = calculator.calculate_dcf(
            cash_flows=cash_flows,
            discount_rate=args.discount_rate,
            terminal_growth_rate=args.terminal_growth_rate,
            terminal_value=args.terminal_value
        )
    
    elif args.method == "irr":
        if not args.cash_flows:
            print("错误: IRR方法需要--cash_flows参数")
            sys.exit(1)
        
        cash_flows = [float(x) for x in args.cash_flows.split(",")]
        result = calculator.calculate_irr(cash_flows=cash_flows)
    
    elif args.method == "roi":
        if args.initial_investment is None or args.final_value is None or args.time_period is None:
            print("错误: ROI方法需要--initial_investment、--final_value和--time_period参数")
            sys.exit(1)
        
        result = calculator.calculate_roi(
            initial_investment=args.initial_investment,
            final_value=args.final_value,
            time_period=args.time_period
        )
    
    elif args.method == "ltv_cac":
        if args.average_revenue_per_user is None or args.customer_lifetime_months is None or \
           args.monthly_churn_rate is None or args.cac is None:
            print("错误: LTV/CAC方法需要--average_revenue_per_user、--customer_lifetime_months、--monthly_churn_rate和--cac参数")
            sys.exit(1)
        
        result = calculator.calculate_ltv_cac(
            average_revenue_per_user=args.average_revenue_per_user,
            customer_lifetime_months=args.customer_lifetime_months,
            monthly_churn_rate=args.monthly_churn_rate,
            cac=args.cac
        )
    
    elif args.method == "npv":
        if not args.cash_flows or args.discount_rate is None:
            print("错误: NPV方法需要--cash_flows和--discount_rate参数")
            sys.exit(1)
        
        cash_flows = [float(x) for x in args.cash_flows.split(",")]
        result = calculator.calculate_npv(cash_flows=cash_flows, discount_rate=args.discount_rate)
    
    elif args.method == "break_even":
        if args.fixed_costs is None or args.variable_cost_per_unit is None or args.selling_price_per_unit is None:
            print("错误: 盈亏平衡点方法需要--fixed_costs、--variable_cost_per_unit和--selling_price_per_unit参数")
            sys.exit(1)
        
        result = calculator.calculate_break_even(
            fixed_costs=args.fixed_costs,
            variable_cost_per_unit=args.variable_cost_per_unit,
            selling_price_per_unit=args.selling_price_per_unit
        )
    
    # 输出结果
    if result.success:
        print(f"\n✓ {result.method} 计算成功")
        print(f"结果: {result.result}")
        if result.details:
            print(f"\n详细信息:")
            for key, value in result.details.items():
                print(f"  {key}: {value}")
    else:
        print(f"\n✗ {result.method} 计算失败")
        print(f"错误: {result.error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
