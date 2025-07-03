from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

class Task:
    def __init__(self, title: str, deadline: datetime, priority: str, estimated_hours: float, 
                 id: str = None, tags: List[str] = None, earliest_start: datetime = None, 
                 dependencies: List[str] = None):
        self.title = title
        self.deadline = deadline
        self.priority = priority
        self.estimated_hours = estimated_hours
        self.id = id
        self.tags = tags or []
        self.earliest_start = earliest_start
        self.dependencies = dependencies or []

class ScoringStrategy(ABC):
    @abstractmethod
    def score(self, task: Task, current_date: datetime, weights: dict) -> float:
        pass

class SimpleScoringStrategy(ScoringStrategy):
    def score(self, task: Task, current_date: datetime, weights: dict) -> float:
        urgency = (task.deadline - current_date).days
        priority_level = {'low': 1, 'med': 2, 'high': 3}.get(task.priority, 0)
        effort_penalty = task.estimated_hours
        
        score = (weights['w1'] * urgency) + (weights['w2'] * priority_level) - (weights['w3'] * effort_penalty)
        return score

# TODO: Implement additional scoring strategies as needed.