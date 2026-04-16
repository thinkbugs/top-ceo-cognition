#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
能力追踪器
跟踪用户的决策能力演变，提供个性化建议，预测发展趋势

使用方法：
1. Python模块调用：
   from ability_tracker import AbilityTracker
   tracker = AbilityTracker()
   result = tracker.track_ability(decision_data)
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from statistics import mean


@dataclass
class TrackingResult:
    """追踪结果数据类"""
    success: bool
    user_id: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AbilityTracker:
    """能力追踪器"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.user_profiles = {}
        self.ability_dimensions = [
            "战略思维",
            "风险管理",
            "组织管理",
            "产品创新",
            "领导力"
        ]
    
    def track_ability(self, decision_data: Dict[str, Any]) -> TrackingResult:
        """
        追踪能力
        
        参数:
            decision_data: 决策数据
                {
                    "user_id": "用户ID",
                    "decision_id": "决策ID",
                    "decision_type": "strategic/crisis/investment",
                    "scores": {
                        "战略思维": 80,
                        "风险管理": 75,
                        "组织管理": 70,
                        "产品创新": 85,
                        "领导力": 75
                    },
                    "overall_score": 78
                }
        
        返回:
            TrackingResult对象
        """
        try:
            user_id = decision_data.get("user_id", "default")
            
            # 获取或创建用户档案
            profile = self._get_or_create_profile(user_id)
            
            # 更新能力数据
            profile = self._update_ability(profile, decision_data)
            
            # 分析能力趋势
            trend_analysis = self._analyze_trend(profile)
            
            # 计算能力排名
            ranking = self._calculate_ranking(profile)
            
            # 生成个性化建议
            recommendations = self._generate_recommendations(profile, trend_analysis)
            
            # 预测发展趋势
            prediction = self._predict_trend(profile, trend_analysis)
            
            # 保存用户档案
            self.user_profiles[user_id] = profile
            
            return TrackingResult(
                success=True,
                user_id=user_id,
                result={
                    "overall_score": profile["current_overall_score"],
                    "ability_level": profile["ability_level"],
                    "ranking_level": ranking["level"],
                    "trend": trend_analysis["overall_trend"]
                },
                details={
                    "dimension_scores": profile["current_scores"],
                    "trend_analysis": trend_analysis,
                    "ranking": ranking,
                    "recommendations": recommendations,
                    "prediction": prediction,
                    "decision_count": profile["decision_count"]
                }
            )
            
        except Exception as e:
            return TrackingResult(
                success=False,
                user_id=decision_data.get("user_id", "default"),
                result=None,
                error=str(e)
            )
    
    def _get_or_create_profile(self, user_id: str) -> Dict[str, Any]:
        """获取或创建用户档案"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "decision_count": 0,
                "decision_history": [],
                "score_history": [],
                "current_scores": {},
                "current_overall_score": 0,
                "ability_level": "初级",
                "dimension_trends": {}
            }
        
        return self.user_profiles[user_id]
    
    def _update_ability(self, profile: Dict[str, Any], 
                       decision_data: Dict[str, Any]) -> Dict[str, Any]:
        """更新能力数据"""
        scores = decision_data.get("scores", {})
        overall_score = decision_data.get("overall_score", 0)
        
        # 记录决策
        profile["decision_count"] += 1
        profile["decision_history"].append({
            "decision_id": decision_data.get("decision_id", "unknown"),
            "decision_type": decision_data.get("decision_type", "unknown"),
            "timestamp": datetime.now().isoformat()
        })
        
        # 记录分数
        profile["score_history"].append({
            "timestamp": datetime.now().isoformat(),
            "scores": scores,
            "overall_score": overall_score
        })
        
        # 更新当前分数
        for dimension in self.ability_dimensions:
            if dimension in scores:
                profile["current_scores"][dimension] = scores[dimension]
        
        profile["current_overall_score"] = overall_score
        
        # 更新能力等级
        profile["ability_level"] = self._get_ability_level(overall_score)
        
        return profile
    
    def _analyze_trend(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """分析能力趋势"""
        trend_analysis = {
            "overall_trend": "stable",
            "dimension_trends": {},
            "improvement_rate": 0,
            "stability": 0
        }
        
        if len(profile["score_history"]) < 2:
            return trend_analysis
        
        # 获取最近的分数记录
        recent_scores = profile["score_history"][-5:]
        
        # 计算整体趋势
        overall_scores = [s["overall_score"] for s in recent_scores]
        if len(overall_scores) >= 2:
            improvement_rate = overall_scores[-1] - overall_scores[0]
            trend_analysis["improvement_rate"] = improvement_rate
            
            if improvement_rate > 5:
                trend_analysis["overall_trend"] = "improving"
            elif improvement_rate < -5:
                trend_analysis["overall_trend"] = "declining"
        
        # 计算稳定性
        if len(overall_scores) > 2:
            avg_score = mean(overall_scores)
            variance = sum((s - avg_score) ** 2 for s in overall_scores) / len(overall_scores)
            stability = max(0, 100 - variance)
            trend_analysis["stability"] = round(stability, 2)
        
        # 计算各维度趋势
        for dimension in self.ability_dimensions:
            if dimension in profile["current_scores"]:
                dimension_scores = [
                    s["scores"].get(dimension, 0) 
                    for s in recent_scores 
                    if dimension in s["scores"]
                ]
                
                if len(dimension_scores) >= 2:
                    improvement = dimension_scores[-1] - dimension_scores[0]
                    if improvement > 5:
                        trend_analysis["dimension_trends"][dimension] = "improving"
                    elif improvement < -5:
                        trend_analysis["dimension_trends"][dimension] = "declining"
                    else:
                        trend_analysis["dimension_trends"][dimension] = "stable"
        
        return trend_analysis
    
    def _calculate_ranking(self, profile: Dict[str, Any]) -> Dict[str, Any]:
        """计算能力排名"""
        overall_score = profile["current_overall_score"]
        
        # 基于分数确定排名等级
        if overall_score >= 90:
            level = "顶尖"
            percentile = 95
        elif overall_score >= 85:
            level = "优秀"
            percentile = 85
        elif overall_score >= 80:
            level = "良好"
            percentile = 70
        elif overall_score >= 75:
            level = "中上"
            percentile = 50
        elif overall_score >= 70:
            level = "中等"
            percentile = 35
        elif overall_score >= 60:
            level = "中下"
            percentile = 20
        else:
            level = "初级"
            percentile = 5
        
        return {
            "level": level,
            "percentile": percentile,
            "score": overall_score
        }
    
    def _get_ability_level(self, score: float) -> str:
        """获取能力等级"""
        if score >= 90:
            return "顶级"
        elif score >= 80:
            return "高级"
        elif score >= 70:
            return "中级"
        elif score >= 60:
            return "初级"
        else:
            return "入门"
    
    def _generate_recommendations(self, profile: Dict[str, Any],
                                 trend_analysis: Dict[str, Any]) -> List[str]:
        """生成个性化建议"""
        recommendations = []
        
        overall_score = profile["current_overall_score"]
        trend = trend_analysis.get("overall_trend", "stable")
        improvement_rate = trend_analysis.get("improvement_rate", 0)
        
        # 基于趋势的建议
        if trend == "improving":
            recommendations.append(f"你的决策能力正在快速提升（+{improvement_rate:.1f}分），继续保持！")
        elif trend == "declining":
            recommendations.append(f"你的决策能力有所下降（{improvement_rate:.1f}分），建议分析原因，及时调整")
        
        # 基于分数的建议
        if overall_score >= 80:
            recommendations.append("你已经具备优秀的决策能力，可以挑战更复杂的决策场景")
        elif overall_score >= 70:
            recommendations.append("你的决策能力良好，可以通过更多实战进一步提升")
        elif overall_score >= 60:
            recommendations.append("建议加强理论学习，提升决策框架和思维模型")
        else:
            recommendations.append("建议从基础开始学习决策理论和方法")
        
        # 基于维度的建议
        dimension_trends = trend_analysis.get("dimension_trends", {})
        for dimension, dim_trend in dimension_trends.items():
            if dim_trend == "declining":
                recommendations.append(f"{dimension}能力有所下降，建议加强相关学习")
            elif dim_trend == "improving":
                score = profile["current_scores"].get(dimension, 0)
                if score < 80:
                    recommendations.append(f"{dimension}能力正在提升，建议继续加强")
        
        # 基于稳定性的建议
        stability = trend_analysis.get("stability", 0)
        if stability < 70:
            recommendations.append("你的决策稳定性有待提高，建议保持稳定的决策模式")
        
        return recommendations
    
    def _predict_trend(self, profile: Dict[str, Any],
                      trend_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """预测发展趋势"""
        prediction = {
            "next_month_score": profile["current_overall_score"],
            "next_quarter_score": profile["current_overall_score"],
            "confidence": "medium",
            "recommendations": []
        }
        
        current_score = profile["current_overall_score"]
        improvement_rate = trend_analysis.get("improvement_rate", 0)
        stability = trend_analysis.get("stability", 0)
        decision_count = profile["decision_count"]
        
        # 基于改进率预测
        if improvement_rate > 0 and stability > 70:
            # 稳定增长
            prediction["next_month_score"] = min(95, current_score + improvement_rate * 0.3)
            prediction["next_quarter_score"] = min(95, current_score + improvement_rate)
            prediction["confidence"] = "high"
        elif improvement_rate > 0:
            # 波动增长
            prediction["next_month_score"] = min(95, current_score + improvement_rate * 0.2)
            prediction["next_quarter_score"] = min(95, current_score + improvement_rate * 0.7)
            prediction["confidence"] = "medium"
        else:
            # 无明显改进
            prediction["next_month_score"] = current_score
            prediction["next_quarter_score"] = current_score
            prediction["confidence"] = "low"
        
        # 生成预测建议
        if prediction["confidence"] == "high":
            prediction["recommendations"].append("根据当前趋势，你的决策能力有望持续提升")
        elif prediction["confidence"] == "medium":
            prediction["recommendations"].append("你的决策能力有一定提升潜力，但需要更稳定的决策模式")
        else:
            prediction["recommendations"].append("需要加强学习和实战，提升决策能力")
        
        # 舍入
        prediction["next_month_score"] = round(prediction["next_month_score"], 2)
        prediction["next_quarter_score"] = round(prediction["next_quarter_score"], 2)
        
        return prediction
    
    def get_profile(self, user_id: str) -> TrackingResult:
        """
        获取用户档案
        
        参数:
            user_id: 用户ID
        
        返回:
            TrackingResult对象
        """
        try:
            if user_id not in self.user_profiles:
                return TrackingResult(
                    success=False,
                    user_id=user_id,
                    result=None,
                    error=f"未找到用户档案: {user_id}"
                )
            
            profile = self.user_profiles[user_id]
            
            return TrackingResult(
                success=True,
                user_id=user_id,
                result={
                    "overall_score": profile["current_overall_score"],
                    "ability_level": profile["ability_level"],
                    "decision_count": profile["decision_count"]
                },
                details=profile
            )
            
        except Exception as e:
            return TrackingResult(
                success=False,
                user_id=user_id,
                result=None,
                error=str(e)
            )


if __name__ == "__main__":
    # 示例使用
    tracker = AbilityTracker()
    
    # 追踪能力
    decision_data = {
        "user_id": "user_001",
        "decision_id": "decision_001",
        "decision_type": "strategic",
        "scores": {
            "战略思维": 80,
            "风险管理": 75,
            "组织管理": 70,
            "产品创新": 85,
            "领导力": 75
        },
        "overall_score": 77
    }
    
    result = tracker.track_ability(decision_data)
    
    if result.success:
        print(f"\n✓ 能力追踪成功")
        print(f"综合评分: {result.result['overall_score']}/100")
        print(f"能力等级: {result.result['ability_level']}")
        print(f"排名等级: {result.result['ranking_level']}")
        print(f"趋势: {result.result['trend']}")
        
        if result.details:
            print(f"\n维度评分:")
            for dimension, score in result.details['dimension_scores'].items():
                print(f"  {dimension}: {score}")
            
            print(f"\n个性化建议:")
            for i, rec in enumerate(result.details['recommendations'], 1):
                print(f"  {i}. {rec}")
            
            print(f"\n发展趋势预测:")
            prediction = result.details['prediction']
            print(f"  下月预期: {prediction['next_month_score']}/100")
            print(f"  下季预期: {prediction['next_quarter_score']}/100")
            print(f"  预测置信度: {prediction['confidence']}")
    else:
        print(f"\n✗ 能力追踪失败: {result.error}")
