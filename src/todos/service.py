import logging
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.orm import Session

from src.auth.model import TokenData
from src.entities.todo import Todo
from src.exceptions import TodoCreationError, TodoNotFoundError
from src.todos.model import TodoCreate


def create_todo(db: Session, todo_data: TodoCreate, current_user: TokenData) -> Todo:
    try:
        todo = Todo(**todo_data.model_dump(), user_id=current_user.get_uuid())
        db.add(todo)
        db.commit()
        db.refresh(todo)
        logging.info(f"Todo created successfully: {todo.id}")
        return todo
    except Exception as e:
        logging.error(f"Error creating todo: {e}")
        raise TodoCreationError(str(e))


def get_todos(db: Session, current_user: TokenData) -> list[Todo]:
    todos = db.query(Todo).filter(Todo.user_id == current_user.get_uuid()).all()
    logging.info(f"Retrieved {len(todos)} todos for user {current_user.get_uuid()}")
    return todos


def get_todo_by_id(db: Session, todo_id: UUID, current_user: TokenData) -> Todo:
    todo = (
        db.query(Todo)
        .filter(Todo.id == todo_id, Todo.user_id == current_user.get_uuid())
        .first()
    )
    if not todo:
        logging.warning(
            f"Todo with id {todo_id} not found for user {current_user.get_uuid()}"
        )
        raise TodoNotFoundError()
    logging.info(f"Todo retrieved successfully: {todo.id}")
    return todo


def update_todo(
    db: Session, todo_id: UUID, todo_update: TodoCreate, current_user: TokenData
) -> Todo:
    todo_data = todo_update.model_dump(exclude_unset=True)

    db.query(Todo).filter(
        Todo.id == todo_id, Todo.user_id == current_user.get_uuid()
    ).update(todo_data)

    db.commit()
    logging.info(f"Todo updated successfully: {todo_id}")
    return get_todo_by_id(db, todo_id, current_user)


def complete_todo(db: Session, todo_id: UUID, current_user: TokenData) -> Todo:
    todo = get_todo_by_id(db, todo_id, current_user)
    if todo.is_completed:
        logging.warning(f"Todo {todo_id} is already completed.")
        return todo

    todo.is_completed = True
    todo.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(todo)

    logging.info(f"Todo completed successfully: {todo_id}")
    return todo


def delete_todo(db: Session, todo_id: UUID, current_user: TokenData) -> None:
    todo = get_todo_by_id(db, todo_id, current_user)
    db.delete(todo)
    db.commit()
    logging.info(f"Todo deleted successfully: {todo_id}")
