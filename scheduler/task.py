from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Task:
    title: str
    deadline: datetime
    priority: str  # Should be one of {low, med, high}
    estimated_hours: float
    id: Optional[int] = field(default=None)
    tags: List[str] = field(default_factory=list)
    earliest_start: Optional[datetime] = field(default=None)
    dependencies: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.priority not in {'low', 'med', 'high'}:
            raise ValueError(f"Invalid priority '{self.priority}'. Must be one of {{'low', 'med', 'high'}}.")
        if self.estimated_hours <= 0:
            raise ValueError("Estimated hours must be a positive number.")
        if not isinstance(self.tags, list):
            raise ValueError("Tags must be a list of strings.")
        if self.dependencies and not all(isinstance(dep, int) for dep in self.dependencies):
            raise ValueError("All dependencies must be integers.")