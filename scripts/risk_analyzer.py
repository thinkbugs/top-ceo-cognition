#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
风险分析工具
提供决策树分析、蒙特卡洛模拟、敏感性分析、压力测试

使用方法：
1. 命令行调用：python risk_analyzer.py --method sensitivity --base_value 100 --variables price:0.1,volume:0.2,cost:0.15
2. Python模块调用：
   from risk_analyzer import RiskAnalyzer
   analyzer = RiskAnalyzer()
   result = analyzer.sensitivity_analysis(base_value=100, variables={"price": 0.1, "volume": 0.2, "cost": 0.15})
"""

import argparse
import sys
import random
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class RiskResult:
    """风险分析结果数据类"""
    success: bool
    method: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    recommendations: Optional[List[str]] = None


class RiskAnalyzer:
    """风险分析器"""
    
    def __init__(self):
        self.version = "1.0.0"
    
    def decision_tree(self, tree_structure: Dict[str, Any]) -> RiskResult:
        """
        决策树分析
        
        参数:
            tree_structure: 决策树结构
                {
                    "name": "决策根节点",
                    "type": "decision",  # decision或chance
                    "branches": [
                        {
                            "name": "分支1",
                            "probability": 0.5,  # 如果是chance节点
                            "payoff": 100,  # 如果是叶子节点
                            "children": [...]  # 如果是内部节点
                        }
                    ]
                }
        
        返回:
            RiskResult对象
        """
        try:
            if not tree_structure:
                return RiskResult(False, "Decision Tree", None, 
                                error="决策树结构不能为空")
            
            # 计算期望值
            expected_value = self._calculate_decision_tree_expected_value(tree_structure)
            
            # 生成决策路径建议
            best_path = self._find_best_path(tree_structure)
            
            return RiskResult(
                success=True,
                method="Decision Tree",
                result={
                    "expected_value": expected_value,
                    "best_path": best_path
                },
                details={
                    "tree_structure": tree_structure
                }
            )
            
        except Exception as e:
            return RiskResult(False, "Decision Tree", None, error=str(e))
    
    def _calculate_decision_tree_expected_value(self, node: Dict[str, Any]) -> float:
        """递归计算决策树期望值"""
        if "payoff" in node:
            return float(node["payoff"])
        
        total_ev = 0
        for branch in node.get("branches", []):
            if "children" in branch:
                branch_ev = self._calculate_decision_tree_expected_value(branch)
            else:
                branch_ev = float(branch.get("payoff", 0))
            
            probability = float(branch.get("probability", 1.0))
            total_ev += branch_ev * probability
        
        return total_ev
    
    def _find_best_path(self, node: Dict[str, Any]) -> List[str]:
        """找到最佳决策路径"""
        path = []
        path.append(node.get("name", "根节点"))
        
        if "branches" in node:
            best_branch = None
            best_value = float("-inf")
            
            for branch in node["branches"]:
                if "payoff" in branch:
                    branch_value = float(branch["payoff"])
                elif "children" in branch:
                    branch_value = self._calculate_decision_tree_expected_value(branch)
                else:
                    continue
                
                if branch_value > best_value:
                    best_value = branch_value
                    best_branch = branch
            
            if best_branch:
                path.append(best_branch.get("name", "分支"))
                if "children" in best_branch:
                    child_path = self._find_best_path(best_branch["children"][0])
                    path.extend(child_path)
        
        return path
    
    def monte_carlo_simulation(self, base_value: float, variables: Dict[str, Dict[str, float]],
                              iterations: int = 10000, confidence_level: float = 0.95) -> RiskResult:
        """
        蒙特卡洛模拟
        
        参数:
            base_value: 基准值
            variables: 变量分布参数
                {
                    "variable1": {"mean": 100, "std": 10, "distribution": "normal"},
                    "variable2": {"min": 80, "max": 120, "distribution": "uniform"}
                }
            iterations: 模拟次数
            confidence_level: 置信水平（0-1）
        
        返回:
            RiskResult对象
        """
        try:
            if base_value <= 0:
                return RiskResult(False, "Monte Carlo Simulation", None, 
                                error="基准值必须大于0")
            
            if iterations <= 0:
                return RiskResult(False, "Monte Carlo Simulation", None, 
                                error="模拟次数必须大于0")
            
            if not variables:
                return RiskResult(False, "Monte Carlo Simulation", None, 
                                error="变量不能为空")
            
            # 运行模拟
            results = []
            for _ in range(iterations):
                simulated_value = base_value
                
                for var_name, var_params in variables.items():
                    distribution = var_params.get("distribution", "normal")
                    
                    if distribution == "normal":
                        mean = var_params.get("mean", 0)
                        std = var_params.get("std", 1)
                        change = random.gauss(mean, std)
                    elif distribution == "uniform":
                        min_val = var_params.get("min", 0)
                        max_val = var_params.get("max", 1)
                        change = random.uniform(min_val, max_val)
                    else:
                        continue
                    
                    simulated_value += change
                
                results.append(simulated_value)
            
            # 计算统计量
            results.sort()
            mean_value = sum(results) / len(results)
            median_value = results[len(results) // 2]
            std_value = (sum((x - mean_value) ** 2 for x in results) / len(results)) ** 0.5
            
            # 计算百分位数
            p5 = results[int(len(results) * 0.05)]
            p25 = results[int(len(results) * 0.25)]
            p75 = results[int(len(results) * 0.75)]
            p95 = results[int(len(results) * 0.95)]
            
            return RiskResult(
                success=True,
                method="Monte Carlo Simulation",
                result={
                    "mean": round(mean_value, 2),
                    "median": round(median_value, 2),
                    "std": round(std_value, 2)
                },
                details={
                    "iterations": iterations,
                    "confidence_level": confidence_level,
                    "percentiles": {
                        "5%": round(p5, 2),
                        "25%": round(p25, 2),
                        "75%": round(p75, 2),
                        "95%": round(p95, 2)
                    },
                    "min": round(min(results), 2),
                    "max": round(max(results), 2)
                }
            )
            
        except Exception as e:
            return RiskResult(False, "Monte Carlo Simulation", None, error=str(e))
    
    def sensitivity_analysis(self, base_value: float, variables: Dict[str, float],
                           change_percentage: float = 0.1) -> RiskResult:
        """
        敏感性分析
        
        参数:
            base_value: 基准值
            variables: 变量及其影响系数
                {"price": 0.1, "volume": 0.2, "cost": 0.15}
                表示：价格每变化10%，价值变化10%；销量每变化10%，价值变化20%
            change_percentage: 变化百分比（默认10%）
        
        返回:
            RiskResult对象
        """
        try:
            if base_value <= 0:
                return RiskResult(False, "Sensitivity Analysis", None, 
                                error="基准值必须大于0")
            
            if not variables:
                return RiskResult(False, "Sensitivity Analysis", None, 
                                error="变量不能为空")
            
            # 计算敏感性
            sensitivity_results = []
            
            for var_name, coefficient in variables.items():
                # 增加变化百分比
                positive_change = base_value * (1 + coefficient * change_percentage)
                positive_impact = ((positive_change - base_value) / base_value) * 100
                
                # 减少变化百分比
                negative_change = base_value * (1 - coefficient * change_percentage)
                negative_impact = ((negative_change - base_value) / base_value) * 100
                
                sensitivity_results.append({
                    "variable": var_name,
                    "coefficient": coefficient,
                    "positive_change": round(positive_change, 2),
                    "positive_impact": round(positive_impact, 2),
                    "negative_change": round(negative_change, 2),
                    "negative_impact": round(negative_impact, 2),
                    "sensitivity_score": round(abs(coefficient) * 100, 2)
                })
            
            # 按敏感性排序
            sensitivity_results.sort(key=lambda x: x["sensitivity_score"], reverse=True)
            
            # 生成建议
            recommendations = []
            most_sensitive = sensitivity_results[0] if sensitivity_results else None
            if most_sensitive and most_sensitive["sensitivity_score"] > 50:
                recommendations.append(f"{most_sensitive['variable']}最敏感（敏感性{most_sensitive['sensitivity_score']}%），建议重点关注")
            
            least_sensitive = sensitivity_results[-1] if sensitivity_results else None
            if least_sensitive and least_sensitive["sensitivity_score"] < 10:
                recommendations.append(f"{least_sensitive['variable']}不敏感（敏感性{least_sensitive['sensitivity_score']}%），可以降低关注优先级")
            
            return RiskResult(
                success=True,
                method="Sensitivity Analysis",
                result={
                    "base_value": base_value,
                    "change_percentage": change_percentage * 100
                },
                details={
                    "sensitivity_results": sensitivity_results
                },
                recommendations=recommendations
            )
            
        except Exception as e:
            return RiskResult(False, "Sensitivity Analysis", None, error=str(e))
    
    def stress_test(self, base_value: float, stress_scenarios: List[Dict[str, Any]]) -> RiskResult:
        """
        压力测试
        
        参数:
            base_value: 基准值
            stress_scenarios: 压力测试场景
                [
                    {"name": "市场下跌", "variables": {"price": -0.2, "volume": -0.15}},
                    {"name": "成本上升", "variables": {"cost": 0.3}},
                    {"name": "极端情况", "variables": {"price": -0.5, "volume": -0.4, "cost": 0.5}}
                ]
        
        返回:
            RiskResult对象
        """
        try:
            if base_value <= 0:
                return RiskResult(False, "Stress Test", None, 
                                error="基准值必须大于0")
            
            if not stress_scenarios:
                return RiskResult(False, "Stress Test", None, 
                                error="压力测试场景不能为空")
            
            # 运行压力测试
            stress_results = []
            
            for scenario in stress_scenarios:
                scenario_name = scenario.get("name", "未命名场景")
                variables = scenario.get("variables", {})
                
                # 计算压力测试后的值
                stressed_value = base_value
                total_impact = 0
                
                for var_name, change in variables.items():
                    stressed_value = stressed_value * (1 + change)
                    impact = base_value * change
                    total_impact += impact
                
                # 计算影响百分比
                impact_percentage = ((stressed_value - base_value) / base_value) * 100
                
                # 评估风险等级
                if impact_percentage > -20:
                    risk_level = "低"
                elif impact_percentage > -40:
                    risk_level = "中"
                else:
                    risk_level = "高"
                
                stress_results.append({
                    "scenario": scenario_name,
                    "stressed_value": round(stressed_value, 2),
                    "impact_percentage": round(impact_percentage, 2),
                    "risk_level": risk_level,
                    "variables": variables
                })
            
            # 生成建议
            recommendations = []
            high_risk_scenarios = [s for s in stress_results if s["risk_level"] == "高"]
            if high_risk_scenarios:
                recommendations.append(f"发现{len(high_risk_scenarios)}个高风险场景，建议制定应对策略")
                for scenario in high_risk_scenarios:
                    recommendations.append(f"  - {scenario['scenario']}: 影响{scenario['impact_percentage']}%")
            
            return RiskResult(
                success=True,
                method="Stress Test",
                result={
                    "base_value": base_value,
                    "scenarios_count": len(stress_scenarios)
                },
                details={
                    "stress_results": stress_results
                },
                recommendations=recommendations
            )
            
        except Exception as e:
            return RiskResult(False, "Stress Test", None, error=str(e))


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description="风险分析工具")
    parser.add_argument("--method", type=str, required=True,
                       choices=["decision_tree", "monte_carlo", "sensitivity", "stress_test"],
                       help="分析方法")
    
    # 通用参数
    parser.add_argument("--base_value", type=float, help="基准值")
    
    # 敏感性分析参数
    parser.add_argument("--variables", type=str, help="变量（用逗号分隔，如price:0.1,volume:0.2）")
    parser.add_argument("--change_percentage", type=float, default=0.1, help="变化百分比")
    
    # 蒙特卡洛模拟参数
    parser.add_argument("--iterations", type=int, default=10000, help="模拟次数")
    parser.add_argument("--confidence_level", type=float, default=0.95, help="置信水平")
    
    args = parser.parse_args()
    
    analyzer = RiskAnalyzer()
    result = None
    
    if args.method == "decision_tree":
        print("错误: 决策树分析不支持命令行调用，请使用Python模块调用")
        sys.exit(1)
    
    elif args.method == "monte_carlo":
        print("错误: 蒙特卡洛模拟不支持命令行调用，请使用Python模块调用")
        sys.exit(1)
    
    elif args.method == "sensitivity":
        if args.base_value is None or not args.variables:
            print("错误: 敏感性分析需要--base_value和--variables参数")
            sys.exit(1)
        
        # 解析变量
        variables = {}
        for var_str in args.variables.split(","):
            parts = var_str.split(":")
            if len(parts) == 2:
                variables[parts[0]] = float(parts[1])
        
        result = analyzer.sensitivity_analysis(
            base_value=args.base_value,
            variables=variables,
            change_percentage=args.change_percentage
        )
    
    elif args.method == "stress_test":
        print("错误: 压力测试不支持命令行调用，请使用Python模块调用")
        sys.exit(1)
    
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
                else:
                    print(f"  {key}: {value}")
        if result.recommendations:
            print(f"\n建议:")
            for rec in result.recommendations:
                print(f"  - {rec}")
    else:
        print(f"\n✗ {result.method} 失败")
        print(f"错误: {result.error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
