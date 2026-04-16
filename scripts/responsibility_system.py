#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
责任承担系统
实现行为责任承担：决策归因、结果跟踪、失败分析、改进措施、透明沟通

使用方法：
1. Python模块调用：
   from responsibility_system import ResponsibilitySystem
   system = ResponsibilitySystem()
   result = system.make_decision(decision_data)
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ResponsibilityResult:
    """责任承担结果数据类"""
    success: bool
    responsibility_type: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class DecisionLog:
    """决策日志"""
    
    def __init__(self):
        self.decisions = {}
    
    def log(self, decision_data: Dict[str, Any]) -> str:
        """记录决策"""
        decision_id = f"decision_{len(self.decisions)}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.decisions[decision_id] = {
            "decision_id": decision_id,
            "title": decision_data.get("title", ""),
            "context": decision_data.get("context", ""),
            "options": decision_data.get("options", []),
            "selected_option": decision_data.get("selected_option", ""),
            "reasoning": decision_data.get("reasoning", ""),
            "decision_maker": decision_data.get("decision_maker", "AI"),
            "timestamp": datetime.now().isoformat(),
            "status": "pending",
            "result": None,
            "responsibility": []
        }
        
        return decision_id
    
    def add_responsibility(self, decision_id: str, responsible_party: str, 
                         responsibility_description: str):
        """添加责任"""
        if decision_id in self.decisions:
            self.decisions[decision_id]["responsibility"].append({
                "party": responsible_party,
                "description": responsibility_description,
                "timestamp": datetime.now().isoformat()
            })
    
    def update_status(self, decision_id: str, status: str, result: Optional[Dict] = None):
        """更新决策状态"""
        if decision_id in self.decisions:
            self.decisions[decision_id]["status"] = status
            if result:
                self.decisions[decision_id]["result"] = result


class ResultTracker:
    """结果跟踪器"""
    
    def __init__(self):
        self.tracking = {}
    
    def start_tracking(self, decision_id: str, expected_outcomes: List[str]):
        """开始跟踪"""
        self.tracking[decision_id] = {
            "decision_id": decision_id,
            "expected_outcomes": expected_outcomes,
            "tracking_points": [],
            "current_status": "in_progress",
            "started_at": datetime.now().isoformat()
        }
    
    def add_tracking_point(self, decision_id: str, metric: str, value: Any):
        """添加跟踪点"""
        if decision_id in self.tracking:
            self.tracking[decision_id]["tracking_points"].append({
                "timestamp": datetime.now().isoformat(),
                "metric": metric,
                "value": value
            })
    
    def complete_tracking(self, decision_id: str, success: bool, final_result: Dict):
        """完成跟踪"""
        if decision_id in self.tracking:
            self.tracking[decision_id]["current_status"] = "completed"
            self.tracking[decision_id]["success"] = success
            self.tracking[decision_id]["final_result"] = final_result
            self.tracking[decision_id]["completed_at"] = datetime.now().isoformat()


class FailureAnalyzer:
    """失败分析器"""
    
    def analyze(self, decision_id: str, actual_result: Dict, 
                expected_result: Dict) -> Dict[str, Any]:
        """分析失败原因"""
        # 简化版的失败分析
        
        failure_reasons = []
        responsibility = "unknown"
        
        # 分析结果差异
        if actual_result.get("success", False) == False:
            failure_reasons.append("结果未达到预期")
            
            # 分析原因
            if "data_issue" in actual_result.get("error", "").lower():
                failure_reasons.append("数据问题")
                responsibility = "AI数据分析"
            elif "assumption_wrong" in actual_result.get("error", "").lower():
                failure_reasons.append("假设错误")
                responsibility = "AI决策建议"
            else:
                failure_reasons.append("执行问题")
                responsibility = "执行团队"
        
        return {
            "decision_id": decision_id,
            "failure_reasons": failure_reasons,
            "responsibility": responsibility,
            "root_cause": failure_reasons[0] if failure_reasons else "未知",
            "analyzed_at": datetime.now().isoformat()
        }


class ImprovementEngine:
    """改进引擎"""
    
    def generate_improvements(self, failure_analysis: Dict) -> List[Dict[str, Any]]:
        """生成改进措施"""
        improvements = []
        
        failure_reasons = failure_analysis.get("failure_reasons", [])
        
        for reason in failure_reasons:
            if "数据问题" in reason:
                improvements.append({
                    "type": "data_quality",
                    "description": "改进数据质量和数据验证机制",
                    "priority": "high",
                    "estimated_effort": "2周"
                })
            elif "假设错误" in reason:
                improvements.append({
                    "type": "assumption_validation",
                    "description": "加强假设验证和情景分析",
                    "priority": "high",
                    "estimated_effort": "1周"
                })
            elif "执行问题" in reason:
                improvements.append({
                    "type": "execution_process",
                    "description": "改进执行流程和沟通机制",
                    "priority": "medium",
                    "estimated_effort": "1周"
                })
        
        # 通用改进措施
        improvements.append({
            "type": "monitoring",
            "description": "加强实时监控和早期预警",
            "priority": "medium",
            "estimated_effort": "1周"
        })
        
        return improvements


class ResponsibilitySystem:
    """责任承担系统"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.decision_log = DecisionLog()
        self.result_tracker = ResultTracker()
        self.failure_analyzer = FailureAnalyzer()
        self.improvement_engine = ImprovementEngine()
    
    def make_decision(self, decision_data: Dict[str, Any]) -> ResponsibilityResult:
        """
        做决策并承担建议责任
        
        参数:
            decision_data: 决策数据
                {
                    "title": "决策标题",
                    "context": "决策背景",
                    "options": ["选项1", "选项2"],
                    "selected_option": "选择的选项",
                    "reasoning": "决策理由",
                    "expected_outcomes": ["预期结果1", "预期结果2"]
                }
        
        返回:
            ResponsibilityResult对象
        """
        try:
            # 1. 记录决策
            decision_id = self.decision_log.log(decision_data)
            
            # 2. 承担AI建议责任
            self.decision_log.add_responsibility(
                decision_id,
                "AI建议者",
                "基于数据分析提供决策建议"
            )
            
            # 3. 开始跟踪结果
            expected_outcomes = decision_data.get("expected_outcomes", [])
            self.result_tracker.start_tracking(decision_id, expected_outcomes)
            
            # 4. 更新决策状态
            self.decision_log.update_status(decision_id, "in_progress")
            
            return ResponsibilityResult(
                success=True,
                responsibility_type="decision_making",
                result={
                    "decision_id": decision_id,
                    "status": "in_progress",
                    "ai_responsibility": "提供决策建议",
                    "tracking_started": True
                },
                details={
                    "decision": decision_data,
                    "logged_at": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return ResponsibilityResult(
                success=False,
                responsibility_type="decision_making",
                result=None,
                error=str(e)
            )
    
    def report_result(self, decision_id: str, actual_result: Dict) -> ResponsibilityResult:
        """
        报告决策结果
        
        参数:
            decision_id: 决策ID
            actual_result: 实际结果
                {
                    "success": True/False,
                    "metrics": {"metric1": value1, ...},
                    "notes": "备注"
                }
        
        返回:
            ResponsibilityResult对象
        """
        try:
            success = actual_result.get("success", False)
            metrics = actual_result.get("metrics", {})
            
            # 1. 完成跟踪
            self.result_tracker.complete_tracking(decision_id, success, actual_result)
            
            # 2. 更新决策状态
            status = "completed_success" if success else "completed_failure"
            self.decision_log.update_status(decision_id, status, actual_result)
            
            # 3. 如果失败，进行失败分析
            if not success:
                expected_result = self.decision_log.decisions[decision_id].get("expected_outcomes", [])
                failure_analysis = self.failure_analyzer.analyze(
                    decision_id, 
                    actual_result, 
                    {"expected_outcomes": expected_result}
                )
                
                # 4. 生成改进措施
                improvements = self.improvement_engine.generate_improvements(failure_analysis)
                
                # 5. 承担责任
                if failure_analysis["responsibility"] == "AI决策建议":
                    self.decision_log.add_responsibility(
                        decision_id,
                        "AI",
                        f"决策建议错误: {failure_analysis['root_cause']}"
                    )
                
                return ResponsibilityResult(
                    success=True,
                    responsibility_type="result_reporting",
                    result={
                        "decision_id": decision_id,
                        "status": status,
                        "success": False,
                        "ai_responsibility": failure_analysis["responsibility"]
                    },
                    details={
                        "failure_analysis": failure_analysis,
                        "improvements": improvements,
                        "reported_at": datetime.now().isoformat()
                    }
                )
            else:
                return ResponsibilityResult(
                    success=True,
                    responsibility_type="result_reporting",
                    result={
                        "decision_id": decision_id,
                        "status": status,
                        "success": True
                    },
                    details={
                        "metrics": metrics,
                        "reported_at": datetime.now().isoformat()
                    }
                )
            
        except Exception as e:
            return ResponsibilityResult(
                success=False,
                responsibility_type="result_reporting",
                result=None,
                error=str(e)
            )
    
    def get_responsibility_report(self, decision_id: str) -> ResponsibilityResult:
        """
        获取责任报告
        
        参数:
            decision_id: 决策ID
        
        返回:
            ResponsibilityResult对象
        """
        try:
            if decision_id not in self.decision_log.decisions:
                return ResponsibilityResult(
                    success=False,
                    responsibility_type="responsibility_report",
                    result=None,
                    error=f"未找到决策: {decision_id}"
                )
            
            decision = self.decision_log.decisions[decision_id]
            
            report = {
                "decision_id": decision_id,
                "title": decision["title"],
                "decision_maker": decision["decision_maker"],
                "status": decision["status"],
                "responsibilities": decision["responsibility"],
                "result": decision.get("result"),
                "tracking_info": self.result_tracker.tracking.get(decision_id)
            }
            
            return ResponsibilityResult(
                success=True,
                responsibility_type="responsibility_report",
                result=report,
                details={"generated_at": datetime.now().isoformat()}
            )
            
        except Exception as e:
            return ResponsibilityResult(
                success=False,
                responsibility_type="responsibility_report",
                result=None,
                error=str(e)
            )


if __name__ == "__main__":
    # 示例使用
    system = ResponsibilitySystem()
    
    # 做决策
    print("\n做决策:")
    decision_data = {
        "title": "进入新市场",
        "context": "公司希望进入东南亚市场",
        "options": ["直接投资", "合作伙伴", "并购"],
        "selected_option": "合作伙伴",
        "reasoning": "合作伙伴模式风险较低，可以快速进入市场",
        "expected_outcomes": ["6个月内进入3个主要市场", "市场份额达到5%"]
    }
    
    result = system.make_decision(decision_data)
    if result.success:
        print(f"✓ 决策成功")
        print(f"决策ID: {result.result['decision_id']}")
        print(f"AI责任: {result.result['ai_responsibility']}")
        print(f"状态: {result.result['status']}")
    else:
        print(f"✗ 决策失败: {result.error}")
    
    decision_id = result.result["decision_id"]
    
    # 报告结果（失败）
    print("\n报告结果:")
    actual_result = {
        "success": False,
        "metrics": {"market_penetration": "2%", "time_elapsed": "9个月"},
        "notes": "合作伙伴选择错误，进展缓慢",
        "error": "假设错误: 合作伙伴能力被高估"
    }
    
    result = system.report_result(decision_id, actual_result)
    if result.success:
        print(f"✓ 结果报告成功")
        print(f"决策ID: {result.result['decision_id']}")
        print(f"状态: {result.result['status']}")
        print(f"成功: {result.result['success']}")
        
        if result.details.get("failure_analysis"):
            print(f"\n失败分析:")
            failure = result.details["failure_analysis"]
            print(f"  原因: {failure['failure_reasons']}")
            print(f"  责任: {failure['responsibility']}")
            print(f"  根本原因: {failure['root_cause']}")
            
            print(f"\n改进措施:")
            for imp in result.details["improvements"]:
                print(f"  - {imp['description']} (优先级: {imp['priority']})")
    else:
        print(f"✗ 结果报告失败: {result.error}")
    
    # 获取责任报告
    print("\n获取责任报告:")
    result = system.get_responsibility_report(decision_id)
    if result.success:
        print(f"✓ 责任报告生成成功")
        print(f"决策标题: {result.result['title']}")
        print(f"决策者: {result.result['decision_maker']}")
        print(f"状态: {result.result['status']}")
        print(f"责任列表:")
        for resp in result.result['responsibilities']:
            print(f"  - {resp['party']}: {resp['description']}")
    else:
        print(f"✗ 责任报告生成失败: {result.error}")
