#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
战略分解工具
提供10年愿景分解为3年战略、3年战略分解为1年计划、1年计划分解为季度计划、OKR生成

使用方法：
1. 命令行调用：python strategy_decomposer.py --method vision_to_strategy --vision "成为全球最大的AI公司" --year_count 3
2. Python模块调用：
   from strategy_decomposer import StrategyDecomposer
   decomposer = StrategyDecomposer()
   result = decomposer.vision_to_strategy(vision="成为全球最大的AI公司", year_count=3)
"""

import argparse
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class StrategyResult:
    """战略分解结果数据类"""
    success: bool
    method: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class StrategyDecomposer:
    """战略分解器"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.current_year = datetime.now().year
    
    def vision_to_strategy(self, vision: str, year_count: int = 3,
                          key_milestones: Optional[List[str]] = None) -> StrategyResult:
        """
        将10年愿景分解为3年战略
        
        参数:
            vision: 10年愿景描述
            year_count: 战略年数（默认3年）
            key_milestones: 关键里程碑（可选）
        
        返回:
            StrategyResult对象
        """
        try:
            if not vision:
                return StrategyResult(False, "Vision to Strategy", None, 
                                     error="愿景不能为空")
            
            if year_count <= 0:
                return StrategyResult(False, "Vision to Strategy", None, 
                                     error="年数必须大于0")
            
            # 生成年度战略
            yearly_strategies = []
            for i in range(year_count):
                year = self.current_year + i
                yearly_strategies.append({
                    "year": year,
                    "focus": f"第{i+1}年：{vision}的阶段性目标",
                    "milestones": [f"里程碑{i+1}-{j+1}" for j in range(3)]
                })
            
            # 如果提供了关键里程碑，进行分配
            if key_milestones:
                for i, milestone in enumerate(key_milestones):
                    if i < len(yearly_strategies):
                        yearly_strategies[i]["key_milestone"] = milestone
            
            return StrategyResult(
                success=True,
                method="Vision to Strategy",
                result={
                    "vision": vision,
                    "year_count": year_count,
                    "start_year": self.current_year,
                    "end_year": self.current_year + year_count - 1
                },
                details={
                    "yearly_strategies": yearly_strategies
                }
            )
            
        except Exception as e:
            return StrategyResult(False, "Vision to Strategy", None, error=str(e))
    
    def strategy_to_plan(self, strategic_goals: List[str], year: int) -> StrategyResult:
        """
        将3年战略分解为1年计划
        
        参数:
            strategic_goals: 战略目标列表
            year: 目标年份
        
        返回:
            StrategyResult对象
        """
        try:
            if not strategic_goals:
                return StrategyResult(False, "Strategy to Plan", None, 
                                     error="战略目标不能为空")
            
            # 生成季度计划
            quarterly_plans = []
            quarters = ["Q1", "Q2", "Q3", "Q4"]
            
            for i, quarter in enumerate(quarters):
                # 每季度分配部分目标
                goal_index = i % len(strategic_goals)
                quarterly_plans.append({
                    "quarter": f"{year}-{quarter}",
                    "strategic_goal": strategic_goals[goal_index],
                    "key_tasks": [f"任务{quarter}-{j+1}" for j in range(5)],
                    "metrics": [f"指标{quarter}-{j+1}" for j in range(3)]
                })
            
            return StrategyResult(
                success=True,
                method="Strategy to Plan",
                result={
                    "year": year,
                    "strategic_goals_count": len(strategic_goals),
                    "strategic_goals": strategic_goals
                },
                details={
                    "quarterly_plans": quarterly_plans
                }
            )
            
        except Exception as e:
            return StrategyResult(False, "Strategy to Plan", None, error=str(e))
    
    def plan_to_quarterly(self, annual_goal: str, year: int, quarter: int) -> StrategyResult:
        """
        将1年计划分解为季度计划
        
        参数:
            annual_goal: 年度目标
            year: 年份
            quarter: 季度（1-4）
        
        返回:
            StrategyResult对象
        """
        try:
            if not annual_goal:
                return StrategyResult(False, "Plan to Quarterly", None, 
                                     error="年度目标不能为空")
            
            if quarter < 1 or quarter > 4:
                return StrategyResult(False, "Plan to Quarterly", None, 
                                     error="季度必须在1到4之间")
            
            # 生成月度计划
            monthly_plans = []
            months_in_quarter = {
                1: [1, 2, 3],
                2: [4, 5, 6],
                3: [7, 8, 9],
                4: [10, 11, 12]
            }
            
            for month in months_in_quarter[quarter]:
                monthly_plans.append({
                    "month": f"{year}-{month:02d}",
                    "focus": f"{annual_goal}的月度执行",
                    "key_actions": [f"行动{month}-{j+1}" for j in range(7)],
                    "deliverables": [f"交付物{month}-{j+1}" for j in range(3)]
                })
            
            return StrategyResult(
                success=True,
                method="Plan to Quarterly",
                result={
                    "quarter": f"{year}-Q{quarter}",
                    "annual_goal": annual_goal
                },
                details={
                    "monthly_plans": monthly_plans
                }
            )
            
        except Exception as e:
            return StrategyResult(False, "Plan to Quarterly", None, error=str(e))
    
    def quarterly_to_weekly(self, quarterly_goal: str, year: int, quarter: int) -> StrategyResult:
        """
        将季度计划分解为周度计划
        
        参数:
            quarterly_goal: 季度目标
            year: 年份
            quarter: 季度（1-4）
        
        返回:
            StrategyResult对象
        """
        try:
            if not quarterly_goal:
                return StrategyResult(False, "Quarterly to Weekly", None, 
                                     error="季度目标不能为空")
            
            if quarter < 1 or quarter > 4:
                return StrategyResult(False, "Quarterly to Weekly", None, 
                                     error="季度必须在1到4之间")
            
            # 每季度约13周
            weeks_count = 13
            weekly_plans = []
            
            for week in range(1, weeks_count + 1):
                weekly_plans.append({
                    "week": f"{year}-Q{quarter}-W{week}",
                    "focus": f"{quarterly_goal}的周度执行",
                    "daily_tasks": [f"任务{week}-{day}" for day in range(1, 8)],
                    "weekly_goal": f"周目标{week}",
                    "deliverable": f"周交付物{week}"
                })
            
            return StrategyResult(
                success=True,
                method="Quarterly to Weekly",
                result={
                    "quarter": f"{year}-Q{quarter}",
                    "quarterly_goal": quarterly_goal,
                    "weeks_count": weeks_count
                },
                details={
                    "weekly_plans": weekly_plans
                }
            )
            
        except Exception as e:
            return StrategyResult(False, "Quarterly to Weekly", None, error=str(e))
    
    def generate_okr(self, objective: str, year: Optional[int] = None,
                    quarter: Optional[int] = None, key_result_count: int = 3) -> StrategyResult:
        """
        生成OKR（目标与关键结果）
        
        参数:
            objective: 目标（O）
            year: 年份（可选）
            quarter: 季度（可选）
            key_result_count: 关键结果数量（默认3个）
        
        返回:
            StrategyResult对象
        """
        try:
            if not objective:
                return StrategyResult(False, "OKR Generation", None, 
                                     error="目标不能为空")
            
            if key_result_count <= 0:
                return StrategyResult(False, "OKR Generation", None, 
                                     error="关键结果数量必须大于0")
            
            # 生成关键结果（KR）
            key_results = []
            for i in range(key_result_count):
                key_results.append({
                    "kr_id": f"KR{i+1}",
                    "description": f"关键结果{i+1}：与{objective}相关的可衡量结果",
                    "metric": f"指标{i+1}",
                    "target": f"目标值{i+1}",
                    "current_value": 0,
                    "unit": "单位"
                })
            
            # 确定周期
            period = ""
            if year and quarter:
                period = f"{year}-Q{quarter}"
            elif year:
                period = str(year)
            else:
                period = "自定义周期"
            
            return StrategyResult(
                success=True,
                method="OKR Generation",
                result={
                    "period": period,
                    "objective": objective,
                    "key_results_count": key_result_count
                },
                details={
                    "key_results": key_results,
                    "okr_id": f"OKR-{year if year else 'X'}-{quarter if quarter else 'X'}"
                }
            )
            
        except Exception as e:
            return StrategyResult(False, "OKR Generation", None, error=str(e))
    
    def decompose_full_strategy(self, vision: str, year_count: int = 3) -> StrategyResult:
        """
        完整战略分解：10年愿景→3年战略→1年计划→季度计划→月度计划→OKR
        
        参数:
            vision: 10年愿景
            year_count: 战略年数（默认3年）
        
        返回:
            StrategyResult对象
        """
        try:
            if not vision:
                return StrategyResult(False, "Full Strategy Decomposition", None, 
                                     error="愿景不能为空")
            
            # 第1步：10年愿景→3年战略
            vision_result = self.vision_to_strategy(vision, year_count)
            if not vision_result.success:
                return vision_result
            
            # 第2步：3年战略→1年计划（只分解第一年）
            first_year_strategies = vision_result.details["yearly_strategies"][0]
            plan_result = self.strategy_to_plan(
                strategic_goals=[first_year_strategies["focus"]],
                year=self.current_year
            )
            if not plan_result.success:
                return plan_result
            
            # 第3步：1年计划→季度计划（只分解第一季度）
            first_quarter_plan = plan_result.details["quarterly_plans"][0]
            quarterly_result = self.plan_to_quarterly(
                annual_goal=first_quarter_plan["strategic_goal"],
                year=self.current_year,
                quarter=1
            )
            if not quarterly_result.success:
                return quarterly_result
            
            # 第4步：生成Q1的OKR
            okr_result = self.generate_okr(
                objective=first_quarter_plan["strategic_goal"],
                year=self.current_year,
                quarter=1,
                key_result_count=3
            )
            if not okr_result.success:
                return okr_result
            
            return StrategyResult(
                success=True,
                method="Full Strategy Decomposition",
                result={
                    "vision": vision,
                    "strategy_period": f"{self.current_year}-{self.current_year + year_count - 1}"
                },
                details={
                    "vision_to_strategy": vision_result.details,
                    "strategy_to_plan": plan_result.details,
                    "plan_to_quarterly": quarterly_result.details,
                    "okr": okr_result.details
                }
            )
            
        except Exception as e:
            return StrategyResult(False, "Full Strategy Decomposition", None, error=str(e))


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description="战略分解工具")
    parser.add_argument("--method", type=str, required=True,
                       choices=["vision_to_strategy", "strategy_to_plan", "plan_to_quarterly", 
                               "quarterly_to_weekly", "generate_okr", "full_decompose"],
                       help="分解方法")
    
    # 通用参数
    parser.add_argument("--vision", type=str, help="10年愿景")
    parser.add_argument("--year", type=int, help="年份")
    parser.add_argument("--quarter", type=int, help="季度（1-4）")
    parser.add_argument("--year_count", type=int, default=3, help="战略年数")
    
    # OKR参数
    parser.add_argument("--objective", type=str, help="目标（O）")
    parser.add_argument("--key_result_count", type=int, default=3, help="关键结果数量")
    
    args = parser.parse_args()
    
    decomposer = StrategyDecomposer()
    result = None
    
    if args.method == "vision_to_strategy":
        if not args.vision:
            print("错误: 愿景分解需要--vision参数")
            sys.exit(1)
        
        result = decomposer.vision_to_strategy(
            vision=args.vision,
            year_count=args.year_count
        )
    
    elif args.method == "strategy_to_plan":
        print("错误: 战略到计划不支持命令行调用，请使用Python模块调用")
        sys.exit(1)
    
    elif args.method == "plan_to_quarterly":
        print("错误: 计划到季度不支持命令行调用，请使用Python模块调用")
        sys.exit(1)
    
    elif args.method == "quarterly_to_weekly":
        print("错误: 季度到周度不支持命令行调用，请使用Python模块调用")
        sys.exit(1)
    
    elif args.method == "generate_okr":
        if not args.objective:
            print("错误: OKR生成需要--objective参数")
            sys.exit(1)
        
        result = decomposer.generate_okr(
            objective=args.objective,
            year=args.year,
            quarter=args.quarter,
            key_result_count=args.key_result_count
        )
    
    elif args.method == "full_decompose":
        if not args.vision:
            print("错误: 完整战略分解需要--vision参数")
            sys.exit(1)
        
        result = decomposer.decompose_full_strategy(
            vision=args.vision,
            year_count=args.year_count
        )
    
    # 输出结果
    if result.success:
        print(f"\n✓ {result.method} 成功")
        print(f"结果: {result.result}")
        if result.details:
            print(f"\n详细信息:")
            for key, value in result.details.items():
                if isinstance(value, list):
                    print(f"  {key}:")
                    for item in value:
                        print(f"    {item}")
                elif isinstance(value, dict):
                    print(f"  {key}:")
                    for k, v in value.items():
                        print(f"    {k}: {v}")
                else:
                    print(f"  {key}: {value}")
    else:
        print(f"\n✗ {result.method} 失败")
        print(f"错误: {result.error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
