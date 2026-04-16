#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CEO决策模拟器
提供安全的沙盒模拟环境，模拟真实CEO决策场景，提供即时反馈和评分

使用方法：
1. 命令行调用：python decision_simulator.py --scenario strategic --user_choice "扩张市场"
2. Python模块调用：
   from decision_simulator import DecisionSimulator
   simulator = DecisionSimulator()
   result = simulator.simulate_decision(scenario_type="strategic", user_choice="扩张市场")
"""

import argparse
import sys
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SimulationResult:
    """模拟结果数据类"""
    success: bool
    scenario: str
    user_choice: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    score: Optional[int] = None
    feedback: Optional[str] = None


class DecisionSimulator:
    """CEO决策模拟器"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.scenarios = self._init_scenarios()
    
    def _init_scenarios(self) -> Dict[str, List[Dict[str, Any]]]:
        """初始化决策场景库"""
        return {
            "strategic": [
                {
                    "id": "strategic_001",
                    "title": "市场扩张决策",
                    "description": "公司主营业务增长放缓，面临市场扩张的关键决策",
                    "background": "你的公司主营业务在核心市场已经占据30%市场份额，增长率从30%下降到15%。竞争对手正在积极扩张。",
                    "options": [
                        {"id": "opt1", "text": "继续深耕核心市场，提升渗透率", "score": 70, "risk": "低", "return": "中"},
                        {"id": "opt2", "text": "扩张到相关细分市场", "score": 85, "risk": "中", "return": "高"},
                        {"id": "opt3", "text": "进入新兴市场", "score": 60, "risk": "高", "return": "高"},
                        {"id": "opt4", "text": "多元化业务", "score": 50, "risk": "高", "return": "不确定"}
                    ],
                    "ceo_reference": {
                        "musk": "选择opt2，相关扩张，风险可控",
                        "bezos": "选择opt2，Day1文化，持续扩张",
                        "buffett": "选择opt1，能力圈内深耕"
                    }
                },
                {
                    "id": "strategic_002",
                    "title": "产品创新决策",
                    "description": "面对技术变革，需要决定产品创新方向",
                    "background": "行业出现新技术，可能颠覆现有产品。公司有足够的研发资源，但需要决定投入方向。",
                    "options": [
                        {"id": "opt1", "text": "渐进式创新，优化现有产品", "score": 65, "risk": "低", "return": "中"},
                        {"id": "opt2", "text": "颠覆式创新，开发新产品", "score": 90, "risk": "高", "return": "极高"},
                        {"id": "opt3", "text": "双轨并行，同时优化和创新", "score": 75, "risk": "中", "return": "中高"},
                        {"id": "opt4", "text": "观望等待，降低风险", "score": 40, "risk": "低", "return": "低"}
                    ],
                    "ceo_reference": {
                        "musk": "选择opt2，第一性原理，颠覆创新",
                        "jobs": "选择opt2，产品极致，颠覆创新",
                        "bezos": "选择opt3，Day1文化，双轨并行"
                    }
                },
                {
                    "id": "strategic_003",
                    "title": "投资决策",
                    "description": "公司有充裕现金流，需要决定投资方向",
                    "background": "公司现金流充裕，面临多个投资机会：收购竞争对手、研发新技术、拓展新业务、回购股票。",
                    "options": [
                        {"id": "opt1", "text": "收购竞争对手，巩固市场地位", "score": 75, "risk": "中", "return": "中高"},
                        {"id": "opt2", "text": "投入研发，保持技术领先", "score": 85, "risk": "中", "return": "高"},
                        {"id": "opt3", "text": "拓展新业务，寻找第二增长曲线", "score": 80, "risk": "中高", "return": "高"},
                        {"id": "opt4", "text": "回购股票，提升股东价值", "score": 60, "risk": "低", "return": "中"}
                    ],
                    "ceo_reference": {
                        "buffett": "选择opt2，护城河，技术领先",
                        "bezos": "选择opt2，长期投资，持续创新",
                        "musk": "选择opt2，第一性原理，技术突破"
                    }
                }
            ],
            "crisis": [
                {
                    "id": "crisis_001",
                    "title": "公关危机应对",
                    "description": "产品出现质量问题，引发公关危机",
                    "background": "公司产品出现质量问题，客户投诉激增，媒体负面报道，股价下跌15%。需要立即应对。",
                    "options": [
                        {"id": "opt1", "text": "快速道歉，召回产品", "score": 80, "risk": "高", "return": "长期价值"},
                        {"id": "opt2", "text": "淡化问题，等待风波过去", "score": 30, "risk": "高", "return": "低"},
                        {"id": "opt3", "text": "主动公布调查结果，透明化处理", "score": 90, "risk": "中", "return": "高"},
                        {"id": "opt4", "text": "快速修复问题，补偿用户", "score": 85, "risk": "中", "return": "高"}
                    ],
                    "ceo_reference": {
                        "jobs": "选择opt3，透明化，建立信任",
                        "musk": "选择opt4，快速行动，解决问题",
                        "cook": "选择opt3，透明化，建立信任"
                    }
                },
                {
                    "id": "crisis_002",
                    "title": "现金流危机",
                    "description": "公司现金流紧张，面临破产风险",
                    "background": "公司现金流紧张，只有3个月资金。需要立即采取措施。",
                    "options": [
                        {"id": "opt1", "text": "裁员降本，快速止血", "score": 70, "risk": "中", "return": "短期生存"},
                        {"id": "opt2", "text": "紧急融资，稀释股权", "score": 75, "risk": "高", "return": "生存但稀释"},
                        {"id": "opt3", "text": "出售资产，快速变现", "score": 65, "risk": "中", "return": "短期生存"},
                        {"id": "opt4", "text": "业务转型，寻找新收入", "score": 80, "risk": "高", "return": "长期价值"}
                    ],
                    "ceo_reference": {
                        "musk": "选择opt2，融资，保留核心",
                        "jobs": "选择opt4，转型，寻找新机会",
                        "bezos": "选择opt2，融资，长期价值"
                    }
                }
            ],
            "investment": [
                {
                    "id": "investment_001",
                    "title": "创业投资决策",
                    "description": "评估一个创业项目，决定是否投资",
                    "background": "一个AI创业公司寻求投资，团队优秀，产品有潜力，但市场竞争激烈。估值5000万美元，需要融资1000万美元。",
                    "options": [
                        {"id": "opt1", "text": "全额投资，占股20%", "score": 70, "risk": "高", "return": "不确定"},
                        {"id": "opt2", "text": "部分投资，占股10%", "score": 80, "risk": "中", "return": "中高"},
                        {"id": "opt3", "text": "观望等待，更多信息", "score": 60, "risk": "低", "return": "不确定"},
                        {"id": "opt4", "text": "不投资，风险太大", "score": 50, "risk": "低", "return": "无"}
                    ],
                    "ceo_reference": {
                        "buffett": "选择opt3，能力圈，观望等待",
                        "thiel": "选择opt1，大胆投资，高回报",
                        "horowitz": "选择opt2，部分投资，降低风险"
                    }
                }
            ]
        }
    
    def list_scenarios(self, scenario_type: Optional[str] = None) -> SimulationResult:
        """
        列出可用的决策场景
        
        参数:
            scenario_type: 场景类型（strategic/crisis/investment），不指定则列出所有
        
        返回:
            SimulationResult对象
        """
        try:
            if scenario_type:
                if scenario_type not in self.scenarios:
                    return SimulationResult(
                        success=False,
                        scenario=scenario_type,
                        user_choice="",
                        result=None,
                        error=f"未找到场景类型: {scenario_type}"
                    )
                scenarios = self.scenarios[scenario_type]
            else:
                scenarios = []
                for type_scenarios in self.scenarios.values():
                    scenarios.extend(type_scenarios)
            
            scenario_list = []
            for scenario in scenarios:
                scenario_list.append({
                    "id": scenario["id"],
                    "title": scenario["title"],
                    "description": scenario["description"],
                    "type": scenario_type or "multiple"
                })
            
            return SimulationResult(
                success=True,
                scenario=scenario_type or "all",
                user_choice="",
                result={"count": len(scenario_list), "scenarios": scenario_list}
            )
            
        except Exception as e:
            return SimulationResult(
                success=False,
                scenario=scenario_type or "all",
                user_choice="",
                result=None,
                error=str(e)
            )
    
    def simulate_decision(self, scenario_type: str, scenario_id: str, 
                        user_choice: str) -> SimulationResult:
        """
        模拟CEO决策
        
        参数:
            scenario_type: 场景类型（strategic/crisis/investment）
            scenario_id: 场景ID
            user_choice: 用户选择
        
        返回:
            SimulationResult对象
        """
        try:
            if scenario_type not in self.scenarios:
                return SimulationResult(
                    success=False,
                    scenario=scenario_type,
                    user_choice=user_choice,
                    result=None,
                    error=f"未找到场景类型: {scenario_type}"
                )
            
            # 查找场景
            scenario = None
            for s in self.scenarios[scenario_type]:
                if s["id"] == scenario_id:
                    scenario = s
                    break
            
            if not scenario:
                return SimulationResult(
                    success=False,
                    scenario=scenario_type,
                    user_choice=user_choice,
                    result=None,
                    error=f"未找到场景: {scenario_id}"
                )
            
            # 查找用户选择
            selected_option = None
            for option in scenario["options"]:
                if option["text"] == user_choice or option["id"] == user_choice:
                    selected_option = option
                    break
            
            if not selected_option:
                return SimulationResult(
                    success=False,
                    scenario=scenario_type,
                    user_choice=user_choice,
                    result=None,
                    error=f"未找到选项: {user_choice}"
                )
            
            # 生成反馈
            score = selected_option["score"]
            risk = selected_option["risk"]
            return_value = selected_option["return"]
            
            # 生成反馈
            if score >= 80:
                feedback = "优秀！你的决策符合顶级CEO的思维模式。"
            elif score >= 60:
                feedback = "良好，但还有优化空间。"
            else:
                feedback = "建议重新思考，参考顶级CEO的决策逻辑。"
            
            # CEO参考
            ceo_references = scenario.get("ceo_reference", {})
            
            return SimulationResult(
                success=True,
                scenario=scenario_id,
                user_choice=user_choice,
                result={
                    "score": score,
                    "risk": risk,
                    "return": return_value
                },
                details={
                    "scenario_title": scenario["title"],
                    "scenario_background": scenario["background"],
                    "all_options": scenario["options"],
                    "selected_option": selected_option,
                    "ceo_references": ceo_references
                },
                score=score,
                feedback=feedback
            )
            
        except Exception as e:
            return SimulationResult(
                success=False,
                scenario=scenario_type,
                user_choice=user_choice,
                result=None,
                error=str(e)
            )
    
    def get_scenario_details(self, scenario_type: str, scenario_id: str) -> SimulationResult:
        """
        获取场景详细信息
        
        参数:
            scenario_type: 场景类型
            scenario_id: 场景ID
        
        返回:
            SimulationResult对象
        """
        try:
            if scenario_type not in self.scenarios:
                return SimulationResult(
                    success=False,
                    scenario=scenario_type,
                    user_choice="",
                    result=None,
                    error=f"未找到场景类型: {scenario_type}"
                )
            
            scenario = None
            for s in self.scenarios[scenario_type]:
                if s["id"] == scenario_id:
                    scenario = s
                    break
            
            if not scenario:
                return SimulationResult(
                    success=False,
                    scenario=scenario_type,
                    user_choice="",
                    result=None,
                    error=f"未找到场景: {scenario_id}"
                )
            
            return SimulationResult(
                success=True,
                scenario=scenario_id,
                user_choice="",
                result=scenario
            )
            
        except Exception as e:
            return SimulationResult(
                success=False,
                scenario=scenario_type,
                user_choice="",
                result=None,
                error=str(e)
            )


def main():
    """命令行接口"""
    parser = argparse.ArgumentParser(description="CEO决策模拟器")
    parser.add_argument("--action", type=str, required=True,
                       choices=["list", "simulate", "details"],
                       help="操作类型")
    parser.add_argument("--scenario_type", type=str, 
                       choices=["strategic", "crisis", "investment"],
                       help="场景类型")
    parser.add_argument("--scenario_id", type=str, help="场景ID")
    parser.add_argument("--user_choice", type=str, help="用户选择")
    
    args = parser.parse_args()
    
    simulator = DecisionSimulator()
    result = None
    
    if args.action == "list":
        result = simulator.list_scenarios(args.scenario_type)
    
    elif args.action == "details":
        if not args.scenario_type or not args.scenario_id:
            print("错误: details操作需要--scenario_type和--scenario_id参数")
            sys.exit(1)
        
        result = simulator.get_scenario_details(args.scenario_type, args.scenario_id)
    
    elif args.action == "simulate":
        if not args.scenario_type or not args.scenario_id or not args.user_choice:
            print("错误: simulate操作需要--scenario_type、--scenario_id和--user_choice参数")
            sys.exit(1)
        
        result = simulator.simulate_decision(args.scenario_type, args.scenario_id, args.user_choice)
    
    # 输出结果
    if result.success:
        print(f"\n✓ 决策模拟成功")
        print(f"评分: {result.score}/100")
        print(f"反馈: {result.feedback}")
        if result.details:
            print(f"\n详细信息:")
            print(json.dumps(result.details, indent=2, ensure_ascii=False))
    else:
        print(f"\n✗ 决策模拟失败")
        print(f"错误: {result.error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
