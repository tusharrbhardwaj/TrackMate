"""Plain data objects: no Flask, SQLAlchemy, or database dependency."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Goal:
    id: int | None
    owner_id: int
    title: str
    description: str | None
    supervisor_id: int | None = None


@dataclass(frozen=True)
class Task:
    id: int | None
    goal_id: int
    title: str
    description: str | None
    deadline: datetime
    weight: int


@dataclass(frozen=True)
class CreateGoal:
    title: str
    description: str | None


@dataclass(frozen=True)
class CreateTask:
    title: str
    description: str | None
    deadline: datetime
    weight: int
