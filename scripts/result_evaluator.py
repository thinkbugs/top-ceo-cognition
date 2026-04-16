#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
决策结果评估器
评估决策质量，给出评分和建议，对比顶级CEO决策

使用方法：
1. Python模块调用：
   from result_evaluator import ResultEvaluator
   evaluator = ResultEvaluator()
   result = evaluator.evaluate_decision(decision_data)
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """评估结果数据类"""
    success: bool
    decision_id: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ResultEvaluator:
    """决策结果评估器"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.evaluation_dimensions = [
            "战略思维",
            "风险管理",
            "组织管理",
            "产品创新",
            "领导力"
        ]
    
    def evaluate_decision(self, decision_data: Dict[str, Any]) -> EvaluationResult:
        """
        评估决策质量
        
        参数:
            decision_data: 决策数据
                {
                    "decision_id": "决策ID",
                    "decision_type": "strategic/crisis/investment",
                    "context": "决策背景",
                    "options": ["选项1", "选项2", "选项3"],
                    "selected_option": "选择的选项",
                    "expected_outcome": "预期结果",
                    "actual_outcome": "实际结果",
                    "execution_quality": 85,
                    "result_quality": 80,
                    "timeline": "按时/延迟/提前"
                }
        
        返回:
            EvaluationResult对象
        """
        try:
            decision_id = decision_data.get("decision_id", "unknown")
            
            # 评估维度
            evaluations = {}
            
            # 1. 战略思维评估
            strategic_score = self._evaluate_strategic(decision_data)
            evaluations["战略思维"] = strategic_score
            
            # 2. 风险管理评估
            risk_score = self._evaluate_risk(decision_data)
            evaluations["风险管理"] = risk_score
            
            # 3. 组织管理评估
            organization_score = self._evaluate_organization(decision_data)
            evaluations["组织管理"] = organization_score
            
            # 4. 产品创新评估
            innovation_score = self._evaluate_innovation(decision_data)
            evaluations["产品创新"] = innovation_score
            
            # 5. 领导力评估
            leadership_score = self._evaluate_leadership(decision_data)
            evaluations["领导力"] = leadership_score
            
            # 综合评分
            overall_score = sum(evaluations.values()) / len(evaluations)
            
            # 生成建议
            recommendations = self._generate_recommendations(evaluations)
            
            # 评级
            grade = self._get_grade(overall_score)
            
            return EvaluationResult(
                success=True,
                decision_id=decision_id,
                result={
                    "overall_score": round(overall_score, 2),
                    "grade": grade,
                    "dimension_scores": {k: round(v, 2) for k, v in evaluations.items()}
                },
                details={
                    "recommendations": recommendations,
                    "strengths": [k for k, v in evaluations.items() if v >= 80],
                    "weaknesses": [k for k, v in evaluations.items() if v < 60],
                    "evaluation_date": str(__import__('datetime').datetime.now())
                }
            )
            
        except Exception as e:
            return EvaluationResult(
                success=False,
                decision_id=decision_data.get("decision_id", "unknown"),
                result=None,
                error=str(e)
            )
    
    def _evaluate_strategic(self, decision_data: Dict[str, Any]) -> float:
        """评估战略思维能力"""
        score = 70  # 基础分
        
        # 检查是否有明确的战略目标
        if decision_data.get("expected_outcome"):
            score += 10
        
        # 检查是否考虑了长期影响
        if decision_data.get("timeline") == "按时":
            score += 10
        
        # 检查决策类型
        decision_type = decision_data.get("decision_type", "")
        if decision_type == "strategic":
            score += 10
        
        return min(score, 100)
    
    def _evaluate_risk(self, decision_data: Dict[str, Any]) -> float:
        """评估风险管理能力"""
        score = 70  # 基础分
        
        # 检查是否有应对风险的准备
        execution_quality = decision_data.get("execution_quality", 50)
        if execution_quality >= 70:
            score += 15
        
        # 检查结果质量
        result_quality = decision_data.get("result_quality", 50)
        if result_quality >= 70:
            score += 15
        
        return min(score, 100)
    
    def _evaluate_organization(self, decision_data: Dict[str, Any]) -> float:
        """评估组织管理能力"""
        score = 70  # 基础分
        
        # 检查执行质量
        execution_quality = decision_data.get("execution_quality", 50)
        score += (execution_quality - 50) * 0.3
        
        return min(score, 100)
    
    def _evaluate_innovation(self, decision_data: Dict[str, Any]) -> float:
        """评估产品创新能力"""
        score = 70  # 基础分
        
        # 检查结果质量
        result_quality = decision_data.get("result_quality", 50)
        score += (result_quality - 50) * 0.3
        
        return min(score, 100)
    
    def _evaluate_leadership(self, decision_data: Dict[str, Any]) -> float:
        """评估领导力能力"""
        score = 70  # 基础分
        
        # 检查执行质量和结果质量
        execution_quality = decision_data.get("execution_quality", 50)
        result_quality = decision_data.get("result_quality", 50)
        score += ((execution_quality + result_quality) / 2 - 50) * 0.3
        
        return min(score, 100)
    
    def _generate_recommendations(self, evaluations: Dict[str, float]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        for dimension, score in evaluations.items():
            if score < 60:
                recommendations.append(f"{dimension}能力需要加强，建议深入学习相关案例和方法")
            elif score < 80:
                recommendations.append(f"{dimension}能力良好，可以通过实战演练进一步提升")
        
        if not recommendations:
            recommendations.append("各方面能力均衡，继续保持！")
        
        return recommendations
    
    def _get_grade(self, score: float) -> str:
        """获取评级"""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        else:
            return "D"
    
    def compare_with_ceo(self, user_decision: Dict[str, Any], 
                        ceo_reference: Dict[str, Any]) -> EvaluationResult:
        """
        对比用户决策与CEO决策
        
        参数:
            user_decision: 用户决策数据
            ceo_reference: CEO参考决策
        
        返回:
            EvaluationResult对象
        """
        try:
            # 计算相似度
            similarity = self._calculate_similarity(user_decision, ceo_reference)
            
            # 生成对比分析
            comparison = {
                "similarity": similarity,
                "ceo_approach": ceo_reference.get("approach", "未知"),
                "user_approach": user_decision.get("approach", "未知"),
                "key_differences": self._identify_differences(user_decision, ceo_reference)
            }
            
            # 生成学习建议
            learning_suggestions = []
            if similarity >= 80:
                learning_suggestions.append("你的决策与顶级CEO高度一致，继续保持！")
            elif similarity >= 60:
                learning_suggestions.append("你的决策与顶级CEO较为接近，可以进一步学习其思维方式")
            else:
                learning_suggestions.append("建议深入学习顶级CEO的决策逻辑，提升战略思维")
            
            return EvaluationResult(
                success=True,
                decision_id="comparison",
                result={
                    "similarity": round(similarity, 2)
                },
                details={
                    "comparison": comparison,
                    "learning_suggestions": learning_suggestions
                }
            )
            
        except Exception as e:
            return EvaluationResult(
                success=False,
                decision_id="comparison",
                result=None,
                error=str(e)
            )
    
    def _calculate_similarity(self, decision1: Dict[str, Any], 
                            decision2: Dict[str, Any]) -> float:
        """计算两个决策的相似度"""
        # 简化版相似度计算
        similarity = 70  # 基础相似度
        
        # 检查决策类型
        if decision1.get("decision_type") == decision2.get("decision_type"):
            similarity += 10
        
        # 检查选择
        if decision1.get("selected_option") == decision2.get("selected_option"):
            similarity += 20
        
        return min(similarity, 100)
    
    def _identify_differences(self, user_decision: Dict[str, Any],
                             ceo_reference: Dict[str, Any]) -> List[str]:
        """识别用户决策与CEO决策的差异"""
        differences = []
        
        user_option = user_decision.get("selected_option")
        ceo_option = ceo_reference.get("selected_option")
        
        if user_option != ceo_option:
            differences.append(f"你的选择: {user_option}, CEO选择: {ceo_option}")
        
        return differences


if __name__ == "__main__":
    # 示例使用
    evaluator = ResultEvaluator()
    
    # 示例决策数据
    decision_data = {
        "decision_id": "test_001",
        "decision_type": "strategic",
        "context": "市场扩张决策",
        "options": ["继续深耕核心市场", "扩张到相关细分市场", "进入新兴市场"],
        "selected_option": "扩张到相关细分市场",
        "expected_outcome": "市场份额提升到40%",
        "actual_outcome": "市场份额提升到38%",
        "execution_quality": 85,
        "result_quality": 80,
        "timeline": "按时"
    }
    
    result = evaluator.evaluate_decision(decision_data)
    
    if result.success:
        print(f"\n✓ 决策评估成功")
        print(f"综合评分: {result.result['overall_score']}/100")
        print(f"评级: {result.result['grade']}")
        print(f"\n维度评分:")
        for dimension, score in result.result['dimension_scores'].items():
            print(f"  {dimension}: {score}")
        
        if result.details:
            print(f"\n建议:")
            for rec in result.details['recommendations']:
                print(f"  - {rec}")
    else:
        print(f"\n✗ 决策评估失败: {result.error}")
