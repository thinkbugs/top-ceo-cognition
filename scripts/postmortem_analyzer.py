#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
复盘分析器
自动收集决策数据，分析决策结果，提取教训和改进建议，生成复盘报告

使用方法：
1. Python模块调用：
   from postmortem_analyzer import PostmortemAnalyzer
   analyzer = PostmortemAnalyzer()
   result = analyzer.analyze_decision(decision_data)
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PostmortemResult:
    """复盘分析结果数据类"""
    success: bool
    decision_id: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class PostmortemAnalyzer:
    """复盘分析器"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.decision_history = {}
    
    def analyze_decision(self, decision_data: Dict[str, Any]) -> PostmortemResult:
        """
        分析决策，生成复盘报告
        
        参数:
            decision_data: 决策数据
                {
                    "decision_id": "决策ID",
                    "decision_title": "决策标题",
                    "decision_date": "决策日期",
                    "decision_type": "strategic/crisis/investment",
                    "context": "决策背景",
                    "options": ["选项1", "选项2", "选项3"],
                    "selected_option": "选择的选项",
                    "reasoning": "决策理由",
                    "expected_outcome": "预期结果",
                    "actual_outcome": "实际结果",
                    "outcome_quality": 80,
                    "execution_quality": 75,
                    "timeline": "按时/延迟/提前",
                    "budget": 1000000,
                    "actual_cost": 950000
                }
        
        返回:
            PostmortemResult对象
        """
        try:
            decision_id = decision_data.get("decision_id", "unknown")
            
            # 保存决策历史
            self.decision_history[decision_id] = decision_data
            
            # 分析决策结果
            result_analysis = self._analyze_result(decision_data)
            
            # 提取教训
            lessons = self._extract_lessons(decision_data, result_analysis)
            
            # 生成改进建议
            recommendations = self._generate_recommendations(decision_data, result_analysis)
            
            # 生成复盘报告
            report = self._generate_report(decision_data, result_analysis, lessons, recommendations)
            
            return PostmortemResult(
                success=True,
                decision_id=decision_id,
                result={
                    "overall_score": result_analysis["overall_score"],
                    "outcome_quality": result_analysis["outcome_quality"],
                    "execution_quality": result_analysis["execution_quality"],
                    "lessons_count": len(lessons),
                    "recommendations_count": len(recommendations)
                },
                details={
                    "result_analysis": result_analysis,
                    "lessons": lessons,
                    "recommendations": recommendations,
                    "report": report
                }
            )
            
        except Exception as e:
            return PostmortemResult(
                success=False,
                decision_id=decision_data.get("decision_id", "unknown"),
                result=None,
                error=str(e)
            )
    
    def _analyze_result(self, decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """分析决策结果"""
        result_analysis = {}
        
        # 结果质量分析
        outcome_quality = decision_data.get("outcome_quality", 70)
        result_analysis["outcome_quality"] = outcome_quality
        
        if outcome_quality >= 80:
            result_analysis["outcome_assessment"] = "优秀"
        elif outcome_quality >= 60:
            result_analysis["outcome_assessment"] = "良好"
        else:
            result_analysis["outcome_assessment"] = "需改进"
        
        # 执行质量分析
        execution_quality = decision_data.get("execution_quality", 70)
        result_analysis["execution_quality"] = execution_quality
        
        if execution_quality >= 80:
            result_analysis["execution_assessment"] = "优秀"
        elif execution_quality >= 60:
            result_analysis["execution_assessment"] = "良好"
        else:
            result_analysis["execution_assessment"] = "需改进"
        
        # 时间分析
        timeline = decision_data.get("timeline", "按时")
        result_analysis["timeline"] = timeline
        result_analysis["timeline_assessment"] = "按计划完成" if timeline == "按时" else "需要改进"
        
        # 预算分析
        budget = decision_data.get("budget", 0)
        actual_cost = decision_data.get("actual_cost", 0)
        
        if budget > 0 and actual_cost > 0:
            cost_efficiency = (budget / actual_cost) * 100
            result_analysis["budget_efficiency"] = round(cost_efficiency, 2)
            
            if cost_efficiency >= 95:
                result_analysis["budget_assessment"] = "优秀"
            elif cost_efficiency >= 80:
                result_analysis["budget_assessment"] = "良好"
            else:
                result_analysis["budget_assessment"] = "需改进"
        else:
            result_analysis["budget_assessment"] = "不适用"
        
        # 综合评分
        overall_score = (outcome_quality + execution_quality) / 2
        result_analysis["overall_score"] = round(overall_score, 2)
        
        return result_analysis
    
    def _extract_lessons(self, decision_data: Dict[str, Any], 
                        result_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """提取教训"""
        lessons = []
        
        outcome_quality = result_analysis.get("outcome_quality", 70)
        execution_quality = result_analysis.get("execution_quality", 70)
        
        # 结果质量教训
        if outcome_quality >= 80:
            lessons.append({
                "type": "成功经验",
                "lesson": f"该决策取得了优秀的结果（{outcome_quality}分）",
                "takeaway": "继续保持这种决策模式"
            })
        elif outcome_quality < 60:
            lessons.append({
                "type": "失败教训",
                "lesson": f"该决策结果不理想（{outcome_quality}分）",
                "takeaway": "需要重新评估决策逻辑和前提假设"
            })
        
        # 执行质量教训
        if execution_quality >= 80:
            lessons.append({
                "type": "成功经验",
                "lesson": f"执行过程优秀（{execution_quality}分）",
                "takeaway": "继续保持这种执行模式"
            })
        elif execution_quality < 60:
            lessons.append({
                "type": "失败教训",
                "lesson": f"执行过程需要改进（{execution_quality}分）",
                "takeaway": "需要改进项目管理和团队协作"
            })
        
        # 时间教训
        timeline = result_analysis.get("timeline", "按时")
        if timeline != "按时":
            lessons.append({
                "type": "时间管理",
                "lesson": f"项目{timeline}",
                "takeaway": "需要改进时间估算和进度管理"
            })
        
        # 预算教训
        budget_assessment = result_analysis.get("budget_assessment", "不适用")
        if budget_assessment == "需改进":
            lessons.append({
                "type": "预算管理",
                "lesson": "预算执行情况不佳",
                "takeaway": "需要改进成本控制和预算管理"
            })
        
        return lessons
    
    def _generate_recommendations(self, decision_data: Dict[str, Any],
                                  result_analysis: Dict[str, Any]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        outcome_quality = result_analysis.get("outcome_quality", 70)
        execution_quality = result_analysis.get("execution_quality", 70)
        
        # 结果质量建议
        if outcome_quality < 80:
            recommendations.append("建议在决策前进行更深入的市场调研和分析")
            recommendations.append("建议考虑更多决策选项和情景")
        
        # 执行质量建议
        if execution_quality < 80:
            recommendations.append("建议改进项目管理和团队协作")
            recommendations.append("建议建立更完善的监控和反馈机制")
        
        # 时间管理建议
        timeline = result_analysis.get("timeline", "按时")
        if timeline != "按时":
            recommendations.append("建议改进时间估算方法")
            recommendations.append("建议建立缓冲时间，应对不确定性")
        
        # 预算管理建议
        budget_assessment = result_analysis.get("budget_assessment", "不适用")
        if budget_assessment == "需改进":
            recommendations.append("建议加强成本控制")
            recommendations.append("建议建立预算监控机制")
        
        if not recommendations:
            recommendations.append("决策执行良好，继续保持！")
        
        return recommendations
    
    def _generate_report(self, decision_data: Dict[str, Any],
                        result_analysis: Dict[str, Any],
                        lessons: List[Dict[str, Any]],
                        recommendations: List[str]) -> str:
        """生成复盘报告"""
        report = f"""
# 决策复盘报告

## 基本信息
- 决策ID: {decision_data.get('decision_id', 'unknown')}
- 决策标题: {decision_data.get('decision_title', '未知')}
- 决策日期: {decision_data.get('decision_date', '未知')}
- 复盘日期: {datetime.now().strftime('%Y-%m-%d')}

## 决策背景
{decision_data.get('context', '未提供')}

## 决策选择
- 选择方案: {decision_data.get('selected_option', '未知')}
- 决策理由: {decision_data.get('reasoning', '未提供')}

## 结果分析
### 结果质量
- 评分: {result_analysis.get('outcome_quality', 0)}/100
- 评估: {result_analysis.get('outcome_assessment', '未知')}

### 执行质量
- 评分: {result_analysis.get('execution_quality', 0)}/100
- 评估: {result_analysis.get('execution_assessment', '未知')}

### 时间管理
- 情况: {result_analysis.get('timeline', '未知')}
- 评估: {result_analysis.get('timeline_assessment', '未知')}

### 预算管理
- 效率: {result_analysis.get('budget_efficiency', 'N/A')}%
- 评估: {result_analysis.get('budget_assessment', 'N/A')}

### 综合评分
- 总分: {result_analysis.get('overall_score', 0)}/100

## 经验教训
"""
        
        for lesson in lessons:
            report += f"### {lesson['type']}\n"
            report += f"- 教训: {lesson['lesson']}\n"
            report += f"- 启示: {lesson['takeaway']}\n\n"
        
        report += "## 改进建议\n"
        for i, rec in enumerate(recommendations, 1):
            report += f"{i}. {rec}\n"
        
        report += "\n## 总结\n"
        overall_score = result_analysis.get('overall_score', 0)
        if overall_score >= 80:
            report += "该决策整体表现优秀，建议继续保持这种模式。"
        elif overall_score >= 60:
            report += "该决策表现良好，但仍有改进空间。"
        else:
            report += "该决策表现不佳，需要深入分析原因，改进决策和执行能力。"
        
        return report
    
    def get_decision_history(self, limit: int = 10) -> PostmortemResult:
        """
        获取决策历史
        
        参数:
            limit: 返回数量限制
        
        返回:
            PostmortemResult对象
        """
        try:
            decisions = list(self.decision_history.values())[-limit:]
            
            return PostmortemResult(
                success=True,
                decision_id="history",
                result={
                    "total_count": len(self.decision_history),
                    "returned_count": len(decisions)
                },
                details={
                    "decisions": decisions
                }
            )
            
        except Exception as e:
            return PostmortemResult(
                success=False,
                decision_id="history",
                result=None,
                error=str(e)
            )


if __name__ == "__main__":
    # 示例使用
    analyzer = PostmortemAnalyzer()
    
    # 分析决策
    decision_data = {
        "decision_id": "decision_001",
        "decision_title": "市场扩张战略",
        "decision_date": "2024-01-01",
        "decision_type": "strategic",
        "context": "公司主营业务增长放缓，决定拓展到相关细分市场",
        "options": ["继续深耕核心市场", "扩张到相关细分市场", "进入新兴市场"],
        "selected_option": "扩张到相关细分市场",
        "reasoning": "相关细分市场风险可控，增长潜力大",
        "expected_outcome": "占据细分市场30%份额",
        "actual_outcome": "占据细分市场28%份额",
        "outcome_quality": 75,
        "execution_quality": 80,
        "timeline": "按时",
        "budget": 1000000,
        "actual_cost": 950000
    }
    
    result = analyzer.analyze_decision(decision_data)
    
    if result.success:
        print(f"\n✓ 复盘分析成功")
        print(f"综合评分: {result.result['overall_score']}/100")
        print(f"结果质量: {result.result['outcome_quality']}/100")
        print(f"执行质量: {result.result['execution_quality']}/100")
        
        if result.details:
            print(f"\n经验教训:")
            for lesson in result.details['lessons']:
                print(f"  - [{lesson['type']}] {lesson['lesson']}")
            
            print(f"\n改进建议:")
            for i, rec in enumerate(result.details['recommendations'], 1):
                print(f"  {i}. {rec}")
            
            print(f"\n复盘报告:")
            print(result.details['report'])
    else:
        print(f"\n✗ 复盘分析失败: {result.error}")
