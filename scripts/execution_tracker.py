#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
决策执行跟踪器
自动分解决策为任务，分配责任人和时间表，监控执行进度，预警风险

使用方法：
1. Python模块调用：
   from execution_tracker import ExecutionTracker
   tracker = ExecutionTracker()
   result = tracker.create_execution_plan(decision_data)
"""

import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass
class ExecutionResult:
    """执行结果数据类"""
    success: bool
    execution_id: str
    result: Any
    details: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class ExecutionTracker:
    """决策执行跟踪器"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.execution_plans = {}
    
    def create_execution_plan(self, decision_data: Dict[str, Any]) -> ExecutionResult:
        """
        创建执行计划
        
        参数:
            decision_data: 决策数据
                {
                    "decision_id": "决策ID",
                    "decision_title": "决策标题",
                    "decision_description": "决策描述",
                    "objective": "决策目标",
                    "deadline": "截止日期",
                    "priority": "high/medium/low",
                    "owner": "负责人"
                }
        
        返回:
            ExecutionResult对象
        """
        try:
            decision_id = decision_data.get("decision_id", "unknown")
            execution_id = f"exec_{decision_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
            
            # 分解决策为任务
            tasks = self._decompose_to_tasks(decision_data)
            
            # 分配责任人
            tasks = self._assign_owners(tasks, decision_data.get("owner", "待分配"))
            
            # 设置时间表
            tasks = self._set_timeline(tasks, decision_data.get("deadline"))
            
            # 识别风险
            risks = self._identify_risks(tasks, decision_data)
            
            # 创建执行计划
            execution_plan = {
                "execution_id": execution_id,
                "decision_id": decision_id,
                "decision_title": decision_data.get("decision_title", "未知"),
                "objective": decision_data.get("objective", "未知"),
                "priority": decision_data.get("priority", "medium"),
                "owner": decision_data.get("owner", "待分配"),
                "status": "in_progress",
                "tasks": tasks,
                "risks": risks,
                "created_at": datetime.now().isoformat(),
                "deadline": decision_data.get("deadline")
            }
            
            # 保存执行计划
            self.execution_plans[execution_id] = execution_plan
            
            return ExecutionResult(
                success=True,
                execution_id=execution_id,
                result={
                    "tasks_count": len(tasks),
                    "risks_count": len(risks),
                    "deadline": execution_plan["deadline"]
                },
                details=execution_plan
            )
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                execution_id="",
                result=None,
                error=str(e)
            )
    
    def _decompose_to_tasks(self, decision_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """分解决策为任务"""
        tasks = []
        
        decision_type = decision_data.get("decision_type", "strategic")
        
        if decision_type == "strategic":
            # 战略决策分解
            tasks = [
                {
                    "task_id": "task_001",
                    "title": "制定详细战略计划",
                    "description": "将战略目标分解为具体的行动计划",
                    "status": "pending",
                    "priority": "high",
                    "estimated_hours": 16
                },
                {
                    "task_id": "task_002",
                    "title": "资源配置和预算",
                    "description": "确定所需的资源和预算",
                    "status": "pending",
                    "priority": "high",
                    "estimated_hours": 8
                },
                {
                    "task_id": "task_003",
                    "title": "团队组建和培训",
                    "description": "组建执行团队并进行必要培训",
                    "status": "pending",
                    "priority": "medium",
                    "estimated_hours": 24
                },
                {
                    "task_id": "task_004",
                    "title": "执行监控和调整",
                    "description": "监控执行进度，根据情况调整策略",
                    "status": "pending",
                    "priority": "medium",
                    "estimated_hours": 40
                },
                {
                    "task_id": "task_005",
                    "title": "结果评估和复盘",
                    "description": "评估执行结果，总结经验教训",
                    "status": "pending",
                    "priority": "low",
                    "estimated_hours": 8
                }
            ]
        elif decision_type == "crisis":
            # 危机应对分解
            tasks = [
                {
                    "task_id": "task_001",
                    "title": "立即响应和危机评估",
                    "description": "快速评估危机情况，制定初步应对方案",
                    "status": "pending",
                    "priority": "high",
                    "estimated_hours": 4
                },
                {
                    "task_id": "task_002",
                    "title": "沟通和透明化",
                    "description": "向相关方沟通情况，保持透明",
                    "status": "pending",
                    "priority": "high",
                    "estimated_hours": 8
                },
                {
                    "task_id": "task_003",
                    "title": "问题解决和修复",
                    "description": "采取措施解决问题，修复损害",
                    "status": "pending",
                    "priority": "high",
                    "estimated_hours": 40
                },
                {
                    "task_id": "task_004",
                    "title": "重建信任和声誉",
                    "description": "采取措施重建信任和声誉",
                    "status": "pending",
                    "priority": "medium",
                    "estimated_hours": 80
                }
            ]
        else:
            # 通用决策分解
            tasks = [
                {
                    "task_id": "task_001",
                    "title": "规划阶段",
                    "description": "制定详细的执行计划",
                    "status": "pending",
                    "priority": "high",
                    "estimated_hours": 8
                },
                {
                    "task_id": "task_002",
                    "title": "执行阶段",
                    "description": "执行决策方案",
                    "status": "pending",
                    "priority": "high",
                    "estimated_hours": 40
                },
                {
                    "task_id": "task_003",
                    "title": "监控阶段",
                    "description": "监控执行进度和结果",
                    "status": "pending",
                    "priority": "medium",
                    "estimated_hours": 16
                },
                {
                    "task_id": "task_004",
                    "title": "总结阶段",
                    "description": "总结经验教训",
                    "status": "pending",
                    "priority": "low",
                    "estimated_hours": 4
                }
            ]
        
        return tasks
    
    def _assign_owners(self, tasks: List[Dict[str, Any]], 
                       default_owner: str) -> List[Dict[str, Any]]:
        """分配责任人"""
        for task in tasks:
            task["owner"] = default_owner
        
        return tasks
    
    def _set_timeline(self, tasks: List[Dict[str, Any]], 
                     deadline: Optional[str]) -> List[Dict[str, Any]]:
        """设置时间表"""
        if deadline:
            deadline_date = datetime.fromisoformat(deadline)
        else:
            deadline_date = datetime.now() + timedelta(days=30)
        
        # 按任务优先级和工时分配时间
        total_hours = sum(task["estimated_hours"] for task in tasks)
        start_date = datetime.now()
        
        current_date = start_date
        for task in tasks:
            task_hours = task["estimated_hours"]
            task_days = task_hours / 8  # 假设每天8小时
            
            task["start_date"] = current_date.isoformat()
            current_date += timedelta(days=task_days)
            task["end_date"] = min(current_date, deadline_date).isoformat()
            
            if current_date >= deadline_date:
                task["deadline_warning"] = True
        
        return tasks
    
    def _identify_risks(self, tasks: List[Dict[str, Any]], 
                       decision_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """识别风险"""
        risks = []
        
        # 识别进度风险
        total_hours = sum(task["estimated_hours"] for task in tasks)
        if total_hours > 100:
            risks.append({
                "risk_id": "risk_001",
                "type": "进度",
                "description": "任务工时较大，可能存在进度风险",
                "severity": "high",
                "mitigation": "考虑增加资源或调整任务优先级"
            })
        
        # 识别资源风险
        if decision_data.get("priority") == "high":
            risks.append({
                "risk_id": "risk_002",
                "type": "资源",
                "description": "高优先级决策可能需要额外资源支持",
                "severity": "medium",
                "mitigation": "提前准备资源，建立应急预案"
            })
        
        # 识别质量风险
        high_priority_tasks = [t for t in tasks if t.get("priority") == "high"]
        if len(high_priority_tasks) > 3:
            risks.append({
                "risk_id": "risk_003",
                "type": "质量",
                "description": "高优先级任务较多，可能存在质量风险",
                "severity": "medium",
                "mitigation": "加强质量控制，定期检查"
            })
        
        return risks
    
    def update_task_status(self, execution_id: str, task_id: str, 
                          status: str, progress: int = 0) -> ExecutionResult:
        """
        更新任务状态
        
        参数:
            execution_id: 执行ID
            task_id: 任务ID
            status: 任务状态（pending/in_progress/completed/blocked）
            progress: 进度百分比（0-100）
        
        返回:
            ExecutionResult对象
        """
        try:
            if execution_id not in self.execution_plans:
                return ExecutionResult(
                    success=False,
                    execution_id=execution_id,
                    result=None,
                    error=f"未找到执行计划: {execution_id}"
                )
            
            execution_plan = self.execution_plans[execution_id]
            task = None
            
            for t in execution_plan["tasks"]:
                if t["task_id"] == task_id:
                    task = t
                    break
            
            if not task:
                return ExecutionResult(
                    success=False,
                    execution_id=execution_id,
                    result=None,
                    error=f"未找到任务: {task_id}"
                )
            
            # 更新任务状态
            task["status"] = status
            task["progress"] = progress
            
            # 更新执行计划状态
            self._update_execution_status(execution_plan)
            
            return ExecutionResult(
                success=True,
                execution_id=execution_id,
                result={
                    "task_id": task_id,
                    "status": status,
                    "progress": progress
                },
                details={
                    "execution_status": execution_plan["status"],
                    "overall_progress": self._calculate_overall_progress(execution_plan)
                }
            )
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                execution_id=execution_id,
                result=None,
                error=str(e)
            )
    
    def _update_execution_status(self, execution_plan: Dict[str, Any]):
        """更新执行计划状态"""
        tasks = execution_plan["tasks"]
        
        # 计算总体进度
        overall_progress = self._calculate_overall_progress(execution_plan)
        
        # 更新状态
        if overall_progress >= 100:
            execution_plan["status"] = "completed"
        elif overall_progress > 0:
            execution_plan["status"] = "in_progress"
        else:
            execution_plan["status"] = "pending"
    
    def _calculate_overall_progress(self, execution_plan: Dict[str, Any]) -> int:
        """计算总体进度"""
        tasks = execution_plan["tasks"]
        
        if not tasks:
            return 0
        
        total_progress = sum(task.get("progress", 0) for task in tasks)
        return total_progress // len(tasks)
    
    def get_execution_status(self, execution_id: str) -> ExecutionResult:
        """
        获取执行状态
        
        参数:
            execution_id: 执行ID
        
        返回:
            ExecutionResult对象
        """
        try:
            if execution_id not in self.execution_plans:
                return ExecutionResult(
                    success=False,
                    execution_id=execution_id,
                    result=None,
                    error=f"未找到执行计划: {execution_id}"
                )
            
            execution_plan = self.execution_plans[execution_id]
            
            return ExecutionResult(
                success=True,
                execution_id=execution_id,
                result={
                    "status": execution_plan["status"],
                    "overall_progress": self._calculate_overall_progress(execution_plan),
                    "tasks_completed": len([t for t in execution_plan["tasks"] if t["status"] == "completed"]),
                    "tasks_total": len(execution_plan["tasks"])
                },
                details=execution_plan
            )
            
        except Exception as e:
            return ExecutionResult(
                success=False,
                execution_id=execution_id,
                result=None,
                error=str(e)
            )


if __name__ == "__main__":
    # 示例使用
    tracker = ExecutionTracker()
    
    # 创建执行计划
    decision_data = {
        "decision_id": "decision_001",
        "decision_title": "市场扩张战略",
        "decision_type": "strategic",
        "decision_description": "拓展到相关细分市场",
        "objective": "在12个月内占据细分市场30%份额",
        "deadline": (datetime.now() + timedelta(days=90)).isoformat(),
        "priority": "high",
        "owner": "张三"
    }
    
    result = tracker.create_execution_plan(decision_data)
    
    if result.success:
        print(f"\n✓ 执行计划创建成功")
        print(f"执行ID: {result.execution_id}")
        print(f"任务数量: {result.result['tasks_count']}")
        print(f"风险数量: {result.result['risks_count']}")
        
        if result.details:
            print(f"\n任务列表:")
            for task in result.details['tasks']:
                print(f"  - {task['task_id']}: {task['title']} ({task['estimated_hours']}小时)")
            
            print(f"\n风险列表:")
            for risk in result.details['risks']:
                print(f"  - {risk['type']}: {risk['description']} (严重性: {risk['severity']})")
    else:
        print(f"\n✗ 执行计划创建失败: {result.error}")
