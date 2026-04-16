#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人际交互系统
通过AI+即时通讯实现人际交往能力：情感分析、激励团队、冲突管理、谈判支持、关系管理

使用方法：
1. Python模块调用：
   from interaction_system import InteractionSystem
   system = InteractionSystem()
   result = system.handle_message(user_id, message)
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class InteractionResult:
    """交互结果数据类"""
    success: bool
    interaction_type: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class EmotionAnalyzer:
    """情感分析引擎"""
    
    def __init__(self):
        self.emotion_keywords = {
            "frustrated": ["失败", "问题", "困难", "挫败", "恼火", "不满"],
            "happy": ["成功", "完成", "满意", "开心", "兴奋", "棒"],
            "worried": ["担心", "焦虑", "不确定", "风险", "压力", "困惑"],
            "conflict": ["不同意", "反对", "冲突", "分歧", "争执", "矛盾"],
            "motivated": ["动力", "挑战", "目标", "愿景", "机会", "成长"]
        }
    
    def analyze(self, message: str) -> str:
        """分析消息的情感"""
        message_lower = message.lower()
        
        max_score = 0
        detected_emotion = "neutral"
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > max_score:
                max_score = score
                detected_emotion = emotion
        
        return detected_emotion


class MotivationEngine:
    """激励策略引擎"""
    
    def __init__(self):
        self.motivation_templates = {
            "frustrated": [
                "我理解你的挫败感。让我们一起分析问题，找到解决方案。",
                "困难是暂时的，你的能力是长期的。我们如何能更好地支持你？",
                "每次挫折都是成长的机会。你想要讨论具体的问题吗？"
            ],
            "worried": [
                "担心是正常的，但让我们基于事实来评估风险。",
                "我们有哪些数据可以帮助我们更好地理解情况？",
                "不确定性是机会，而不仅仅是风险。你看到了哪些机会？"
            ],
            "motivated": [
                "太棒了！你的积极性会激励整个团队。",
                "让我们将这份动力转化为具体的行动计划。",
                "保持这个势头！我们如何能支持你实现目标？"
            ]
        }
    
    def generate(self, emotion: str, context: str = "") -> str:
        """生成激励消息"""
        templates = self.motivation_templates.get(emotion, [])
        if templates:
            import random
            return random.choice(templates)
        return "我理解你的感受。让我们一起讨论如何推进。"


class ConflictResolver:
    """冲突管理系统"""
    
    def __init__(self):
        self.conflict_keywords = ["不同意", "反对", "冲突", "分歧", "争执", "矛盾"]
    
    def detect_conflict(self, message: str) -> bool:
        """检测是否是冲突"""
        return any(keyword in message for keyword in self.conflict_keywords)
    
    def resolve(self, message: str) -> str:
        """提供冲突解决方案"""
        return "我听到了不同的观点。让我们找出共同的目标，寻找共赢的解决方案。你愿意详细说明你的关注点吗？"


class NegotiationHelper:
    """谈判支持系统"""
    
    def __init__(self):
        self.negotiation_strategies = {
            "prepare": "准备阶段：明确你的BATNA（最佳替代方案），识别对方的需求和约束。",
            "listen": "倾听阶段：积极倾听，理解对方的真正需求。",
            "propose": "提议阶段：提出双赢的解决方案。",
            "close": "成交阶段：总结协议，确保双方理解一致。"
        }
    
    def suggest_strategy(self, context: str) -> str:
        """提供谈判策略"""
        return "基于当前情况，建议采用以下策略：首先明确双方的核心利益，然后寻找共赢点。我建议我们列出各自的优先级，找到共同点。"


class RelationshipManager:
    """关系管理系统"""
    
    def __init__(self):
        self.relationships = {}
    
    def add_relationship(self, user_id: str, name: str, role: str, 
                        importance: str = "medium"):
        """添加关系"""
        self.relationships[user_id] = {
            "name": name,
            "role": role,
            "importance": importance,
            "interactions": [],
            "last_interaction": None
        }
    
    def log_interaction(self, user_id: str, interaction: str):
        """记录交互"""
        if user_id in self.relationships:
            self.relationships[user_id]["interactions"].append({
                "timestamp": datetime.now().isoformat(),
                "interaction": interaction
            })
            self.relationships[user_id]["last_interaction"] = datetime.now().isoformat()
    
    def get_relationship_info(self, user_id: str) -> Optional[Dict[str, Any]]:
        """获取关系信息"""
        return self.relationships.get(user_id)


class InteractionSystem:
    """人际交互系统"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.emotion_analyzer = EmotionAnalyzer()
        self.motivation_engine = MotivationEngine()
        self.conflict_resolver = ConflictResolver()
        self.negotiation_helper = NegotiationHelper()
        self.relationship_manager = RelationshipManager()
    
    def handle_message(self, user_id: str, message: str) -> InteractionResult:
        """
        处理消息
        
        参数:
            user_id: 用户ID
            message: 用户消息
        
        返回:
            InteractionResult对象
        """
        try:
            # 1. 分析情感
            emotion = self.emotion_analyzer.analyze(message)
            
            # 2. 记录交互
            self.relationship_manager.log_interaction(user_id, f"{emotion}: {message}")
            
            # 3. 生成响应
            if emotion == "conflict":
                response = self.conflict_resolver.resolve(message)
                interaction_type = "conflict_resolution"
            elif emotion in ["frustrated", "worried", "motivated"]:
                response = self.motivation_engine.generate(emotion, message)
                interaction_type = "motivation"
            else:
                response = self._generate_default_response(emotion, message)
                interaction_type = "conversation"
            
            # 4. 获取关系信息
            relationship_info = self.relationship_manager.get_relationship_info(user_id)
            
            return InteractionResult(
                success=True,
                interaction_type=interaction_type,
                result={
                    "response": response,
                    "detected_emotion": emotion,
                    "user_id": user_id
                },
                details={
                    "message": message,
                    "relationship_info": relationship_info,
                    "handled_at": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return InteractionResult(
                success=False,
                interaction_type="unknown",
                result=None,
                error=str(e)
            )
    
    def _generate_default_response(self, emotion: str, message: str) -> str:
        """生成默认响应"""
        if emotion == "neutral":
            return "我理解你的观点。你想继续讨论这个话题，还是转向其他议题？"
        elif emotion == "happy":
            return "很高兴听到这个！我们如何能进一步推进？"
        else:
            return "我理解你的感受。让我们一起讨论如何推进。"
    
    def add_team_member(self, user_id: str, name: str, role: str):
        """添加团队成员"""
        self.relationship_manager.add_relationship(user_id, name, role)
    
    def get_team_status(self) -> InteractionResult:
        """获取团队状态"""
        try:
            relationships = self.relationship_manager.relationships
            
            team_status = {
                "total_members": len(relationships),
                "members": []
            }
            
            for user_id, info in relationships.items():
                team_status["members"].append({
                    "user_id": user_id,
                    "name": info["name"],
                    "role": info["role"],
                    "importance": info["importance"],
                    "interaction_count": len(info["interactions"]),
                    "last_interaction": info["last_interaction"]
                })
            
            return InteractionResult(
                success=True,
                interaction_type="team_status",
                result=team_status,
                details={"generated_at": datetime.now().isoformat()}
            )
            
        except Exception as e:
            return InteractionResult(
                success=False,
                interaction_type="team_status",
                result=None,
                error=str(e)
            )
    
    def suggest_motivation_strategy(self, user_id: str) -> InteractionResult:
        """建议激励策略"""
        try:
            relationship_info = self.relationship_manager.get_relationship_info(user_id)
            
            if not relationship_info:
                return InteractionResult(
                    success=False,
                    interaction_type="motivation_strategy",
                    result=None,
                    error=f"未找到用户: {user_id}"
                )
            
            # 基于交互历史生成激励策略
            interactions = relationship_info.get("interactions", [])
            
            strategy = {
                "user_id": user_id,
                "name": relationship_info["name"],
                "role": relationship_info["role"],
                "suggested_actions": [
                    "定期检查，了解他们的需求和挑战",
                    "提供具体的反馈和认可",
                    "创造成长和发展的机会",
                    "确保清晰的目标和期望"
                ],
                "preferred_communication_style": "开放和支持",
                "recommended_frequency": "每周至少一次"
            }
            
            return InteractionResult(
                success=True,
                interaction_type="motivation_strategy",
                result=strategy,
                details={"generated_at": datetime.now().isoformat()}
            )
            
        except Exception as e:
            return InteractionResult(
                success=False,
                interaction_type="motivation_strategy",
                result=None,
                error=str(e)
            )


if __name__ == "__main__":
    # 示例使用
    system = InteractionSystem()
    
    # 添加团队成员
    system.add_team_member("user_001", "张三", "产品经理")
    system.add_team_member("user_002", "李四", "技术负责人")
    
    # 处理消息
    print("\n处理消息:")
    result = system.handle_message("user_001", "项目遇到了很多困难，我感到很挫败")
    if result.success:
        print(f"✓ 消息处理成功")
        print(f"检测到的情感: {result.result['detected_emotion']}")
        print(f"响应: {result.result['response']}")
    else:
        print(f"✗ 消息处理失败: {result.error}")
    
    # 获取团队状态
    print("\n获取团队状态:")
    result = system.get_team_status()
    if result.success:
        print(f"✓ 团队状态获取成功")
        print(f"团队成员数量: {result.result['total_members']}")
        for member in result.result['members']:
            print(f"  - {member['name']} ({member['role']}): {member['interaction_count']}次交互")
    else:
        print(f"✗ 团队状态获取失败: {result.error}")
    
    # 建议激励策略
    print("\n建议激励策略:")
    result = system.suggest_motivation_strategy("user_001")
    if result.success:
        print(f"✓ 激励策略生成成功")
        print(f"用户: {result.result['name']} ({result.result['role']})")
        print(f"建议行动:")
        for action in result.result['suggested_actions']:
            print(f"  - {action}")
    else:
        print(f"✗ 激励策略生成失败: {result.error}")
