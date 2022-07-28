from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.categories.exceptions import CategoryAlreadyExists
from core.categories.repository import get_category_repository, CategoryRepository
from core.categories.schemas import CategoryCreate, Category
from core.users.api import current_user
from core.users.models import User

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    name="category:create",
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "description": "Category has already exists."
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Unauthorized"
        },
    }
)
async def create(
    data: CategoryCreate,
    user: User = Depends(current_user),
    repository: CategoryRepository = Depends(get_category_repository),
) -> Category:
    try:
        category = await repository.create(data, user)
    except CategoryAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category has already exists."
        )
    return category
