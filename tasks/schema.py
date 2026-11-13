from ninja import ModelSchema, Schema
from pydantic import field_validator, model_validator
from pydantic_core import PydanticCustomError

from accounts.schemas import UserOut
from projects.schema import LabelOut
from tasks.models import Comment, Priority, TaskStatus

from .models import Task


class TaskUpdate(ModelSchema):
    priority: Priority = Priority.MEDIUM

    class Meta:
        model = Task
        fields = ["title", "description", "due_date"]

    @field_validator("title", "description", "priority", check_fields=False)
    @classmethod
    def not_null(cls, value):
        if value is None:
            raise PydanticCustomError("not_null", "This field cannot be null")
        return value

    @field_validator("title", check_fields=False)
    @classmethod
    def title_not_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise PydanticCustomError("blank", "Title cannot be blank")
        return value


class TaskIn(TaskUpdate):
    assignee_id: int | None = None
    label_ids: list[int] = []

    @model_validator(mode="after")
    def urgent_needs_due_date(self):
        if self.priority == Priority.URGENT and self.due_date is None:
            raise ValueError("Urgent tasks need a due date")
        return self


class StatusIn(Schema):
    status: TaskStatus


class TaskOut(ModelSchema):
    assignee: UserOut | None
    labels: list[LabelOut]
    status: TaskStatus
    priority: Priority

    class Meta:
        model = Task
        fields = ["id", "project", "title", "description", "created_at", "due_date"]


class CommentIn(ModelSchema):
    class Meta:
        model = Comment
        fields = ["body"]


class CommentOut(ModelSchema):
    author: UserOut

    class Meta:
        model = Comment
        fields = ["id", "body", "created_at"]
