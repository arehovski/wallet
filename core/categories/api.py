from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.categories.exceptions import CategoryAlreadyExists, CategoryNotFound
from core.categories.models import CategoryType
from core.categories.repository import get_category_repository, CategoryRepository
from core.categories.schemas import CategoryCreate, CategorySchema, CategoryUpdate
from core.users.api import current_user
from core.users.models import User

router = APIRouter()


CATEGORY_EXISTS_RESPONSE = {
    "Category has already exists.": {
        "summary": "A category for this user has already exists.",
        "value": {"detail": CategoryAlreadyExists("Salary").msg},
    }
}
CATEGORY_NOT_FOUND_RESPONSE = {
    "Category not found.": {
        "summary": "A category not found for this user.",
        "value": {"detail": "Not Found"},
    }
}


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    name="category:create",
    response_model=CategorySchema,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "examples": CATEGORY_EXISTS_RESPONSE,
                }
            }
        }
    },
)
async def create(
    data: CategoryCreate,
    user: User = Depends(current_user),
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategorySchema:
    try:
        category = await repository.create(data, user)
    except CategoryAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg)
    return category


@router.get("/", status_code=status.HTTP_200_OK, name="category:list", response_model=list[CategorySchema])
async def list_(
    category_type: CategoryType | None = None,
    user: User = Depends(current_user),
    repository: CategoryRepository = Depends(get_category_repository),
) -> list[CategorySchema]:
    return await repository.list(user, category_type)


@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    name="category:update",
    response_model=CategorySchema,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "examples": CATEGORY_EXISTS_RESPONSE,
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "examples": CATEGORY_NOT_FOUND_RESPONSE,
                }
            }
        },
    },
)
async def update(
    id: int,
    data: CategoryUpdate,
    user: User = Depends(current_user),
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategorySchema:
    try:
        return await repository.update(id, user, data)
    except CategoryAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.msg)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="category:delete",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "content": {
                "application/json": {
                    "examples": CATEGORY_NOT_FOUND_RESPONSE,
                }
            }
        },
    },
)
async def delete(
    id: int,
    user: User = Depends(current_user),
    repository: CategoryRepository = Depends(get_category_repository),
) -> None:
    try:
        await repository.delete(id, user)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND) from e
