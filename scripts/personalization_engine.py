#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
个性化适配引擎
基于用户画像和行为数据，提供个性化推荐和适配

使用方法：
1. Python模块调用：
   from personalization_engine import PersonalizationEngine
   engine = PersonalizationEngine()
   result = engine.get_recommendations(user_id)
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class PersonalizationResult:
    """个性化结果数据类"""
    success: bool
    user_id: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class PersonalizationEngine:
    """个性化适配引擎"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.user_profiles = {}
        self.case_library = {
            "strategic": ["Netflix转型流媒体", "亚马逊进入云计算", "苹果推出iPhone"],
            "crisis": ["三星Note7爆炸事件", "丰田召回事件"],
            "investment": ["巴菲特投资比亚迪", "软银投资阿里巴巴"],
            "organization": ["微软纳德拉转型", "Google重组"],
            "innovation": ["Airbnb颠覆酒店业"]
        }
    
    def create_profile(self, user_data: Dict[str, Any]) -> PersonalizationResult:
        """
        创建用户画像
        
        参数:
            user_data: 用户数据
                {
                    "user_id": "用户ID",
                    "industry": "行业",
                    "company_size": "公司规模",
                    "role": "角色",
                    "experience": "经验年限",
                    "interests": ["战略", "危机应对", "投资"]
                }
        
        返回:
            PersonalizationResult对象
        """
        try:
            user_id = user_data.get("user_id", "unknown")
            
            # 创建用户画像
            profile = {
                "user_id": user_id,
                "industry": user_data.get("industry", "其他"),
                "company_size": user_data.get("company_size", "中型"),
                "role": user_data.get("role", "管理者"),
                "experience": user_data.get("experience", 5),
                "interests": user_data.get("interests", []),
                "ability_scores": {
                    "战略思维": 70,
                    "风险管理": 70,
                    "组织管理": 70,
                    "产品创新": 70,
                    "领导力": 70
                },
                "decision_history": [],
                "learning_progress": {
                    "strategic": 0,
                    "crisis": 0,
                    "investment": 0,
                    "organization": 0,
                    "innovation": 0
                },
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            
            # 保存用户画像
            self.user_profiles[user_id] = profile
            
            return PersonalizationResult(
                success=True,
                user_id=user_id,
                result={"message": "用户画像创建成功"},
                details=profile
            )
            
        except Exception as e:
            return PersonalizationResult(
                success=False,
                user_id=user_data.get("user_id", "unknown"),
                result=None,
                error=str(e)
            )
    
    def get_recommendations(self, user_id: str) -> PersonalizationResult:
        """
        获取个性化推荐
        
        参数:
            user_id: 用户ID
        
        返回:
            PersonalizationResult对象
        """
        try:
            if user_id not in self.user_profiles:
                return PersonalizationResult(
                    success=False,
                    user_id=user_id,
                    result=None,
                    error=f"未找到用户画像: {user_id}"
                )
            
            profile = self.user_profiles[user_id]
            
            # 基于用户画像生成推荐
            recommendations = []
            
            # 推荐案例
            for interest in profile["interests"]:
                cases = self.case_library.get(interest, [])
                for case in cases:
                    recommendations.append({
                        "type": "case",
                        "title": case,
                        "category": interest,
                        "priority": self._calculate_priority(profile, interest)
                    })
            
            # 推荐学习路径
            learning_path = self._generate_learning_path(profile)
            
            # 推荐能力提升
            ability_improvements = self._generate_ability_improvements(profile)
            
            return PersonalizationResult(
                success=True,
                user_id=user_id,
                result={
                    "recommendations_count": len(recommendations),
                    "learning_path": learning_path,
                    "ability_improvements": ability_improvements
                },
                details={
                    "recommendations": recommendations
                }
            )
            
        except Exception as e:
            return PersonalizationResult(
                success=False,
                user_id=user_id,
                result=None,
                error=str(e)
            )
    
    def _calculate_priority(self, profile: Dict[str, Any], interest: str) -> int:
        """计算推荐优先级"""
        # 基于用户兴趣和学习进度计算优先级
        progress = profile["learning_progress"].get(interest, 0)
        priority = 100 - progress  # 学习进度越低，优先级越高
        return max(0, min(100, priority))
    
    def _generate_learning_path(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成学习路径"""
        path = []
        
        # 基于用户兴趣和学习进度生成学习路径
        for interest in profile["interests"]:
            progress = profile["learning_progress"].get(interest, 0)
            
            if progress < 30:
                path.append({
                    "phase": "初级",
                    "category": interest,
                    "content": f"学习{interest}的基础知识",
                    "estimated_time": "2小时"
                })
            elif progress < 60:
                path.append({
                    "phase": "中级",
                    "category": interest,
                    "content": f"深入理解{interest}的核心方法",
                    "estimated_time": "4小时"
                })
            else:
                path.append({
                    "phase": "高级",
                    "category": interest,
                    "content": f"掌握{interest}的高级技巧",
                    "estimated_time": "6小时"
                })
        
        return path
    
    def _generate_ability_improvements(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """生成能力提升建议"""
        improvements = []
        
        ability_scores = profile["ability_scores"]
        
        # 找出需要提升的能力
        for ability, score in ability_scores.items():
            if score < 80:
                improvements.append({
                    "ability": ability,
                    "current_score": score,
                    "target_score": 80,
                    "recommendation": f"加强{ability}能力的学习和实践"
                })
        
        return improvements
    
    def update_progress(self, user_id: str, category: str, progress: int) -> PersonalizationResult:
        """
        更新学习进度
        
        参数:
            user_id: 用户ID
            category: 类别
            progress: 进度（0-100）
        
        返回:
            PersonalizationResult对象
        """
        try:
            if user_id not in self.user_profiles:
                return PersonalizationResult(
                    success=False,
                    user_id=user_id,
                    result=None,
                    error=f"未找到用户画像: {user_id}"
                )
            
            profile = self.user_profiles[user_id]
            profile["learning_progress"][category] = min(100, max(0, progress))
            profile["updated_at"] = datetime.now().isoformat()
            
            return PersonalizationResult(
                success=True,
                user_id=user_id,
                result={"message": "学习进度更新成功"},
                details=profile
            )
            
        except Exception as e:
            return PersonalizationResult(
                success=False,
                user_id=user_id,
                result=None,
                error=str(e)
            )


if __name__ == "__main__":
    # 示例使用
    engine = PersonalizationEngine()
    
    # 创建用户画像
    user_data = {
        "user_id": "user_001",
        "industry": "科技",
        "company_size": "大型",
        "role": "CEO",
        "experience": 10,
        "interests": ["strategic", "crisis", "innovation"]
    }
    
    result = engine.create_profile(user_data)
    if result.success:
        print(f"\n✓ 用户画像创建成功")
        print(f"用户ID: {result.details['user_id']}")
        print(f"行业: {result.details['industry']}")
        print(f"角色: {result.details['role']}")
        print(f"兴趣: {', '.join(result.details['interests'])}")
    else:
        print(f"\n✗ 用户画像创建失败: {result.error}")
    
    # 获取个性化推荐
    result = engine.get_recommendations("user_001")
    if result.success:
        print(f"\n✓ 个性化推荐获取成功")
        print(f"推荐数量: {result.result['recommendations_count']}")
        
        print(f"\n学习路径:")
        for step in result.result['learning_path']:
            print(f"  - [{step['phase']}] {step['content']} ({step['estimated_time']})")
        
        print(f"\n能力提升建议:")
        for imp in result.result['ability_improvements']:
            print(f"  - {imp['ability']}: {imp['current_score']}/100 → {imp['target_score']}/100")
    else:
        print(f"\n✗ 个性化推荐获取失败: {result.error}")
