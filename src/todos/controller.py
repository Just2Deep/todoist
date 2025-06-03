from uuid import UUID

from fastapi import APIRouter, status

from src.auth.service import CurrentUser
from src.database.core import DbSession
from src.todos import model, service

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=model.TodoResponse)
def create_todo(
    todo_data: model.TodoCreate,
    current_user: CurrentUser,
    db: DbSession,
) -> model.TodoResponse:
    """
    Create a new todo item.
    """
    return service.create_todo(db=db, todo_data=todo_data, current_user=current_user)


@router.get("/", response_model=list[model.TodoResponse])
def get_todos(
    current_user: CurrentUser,
    db: DbSession,
) -> list[model.TodoResponse]:
    """
    Retrieve all todo items for the authenticated user.
    """
    return service.get_todos(db=db, current_user=current_user)


@router.get("/{todo_id}", response_model=model.TodoResponse)
def get_todo_by_id(
    todo_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
) -> model.TodoResponse:
    """
    Retrieve a todo item by its ID.
    """
    return service.get_todo_by_id(db=db, todo_id=todo_id, current_user=current_user)


@router.put("/{todo_id}", response_model=model.TodoResponse)
def update_todo(
    todo_id: UUID,
    todo_update: model.TodoCreate,
    current_user: CurrentUser,
    db: DbSession,
) -> model.TodoResponse:
    """
    Update an existing todo item.
    """
    return service.update_todo(
        db=db, todo_id=todo_id, todo_update=todo_update, current_user=current_user
    )


@router.put(
    "/{todo_id}/complete",
    status_code=status.HTTP_200_OK,
    response_model=model.TodoResponse,
)
def complete_todo(
    todo_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
) -> model.TodoResponse:
    """
    Mark a todo item as completed.
    """
    return service.complete_todo(current_user=current_user, db=db, todo_id=todo_id)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: UUID,
    current_user: CurrentUser,
    db: DbSession,
) -> None:
    """
    Delete a todo item.
    """
    service.delete_todo(current_user=current_user, db=db, todo_id=todo_id)
