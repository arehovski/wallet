from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.categories.exceptions import CategoryAlreadyExists
from core.categories.repository import get_category_repository, CategoryRepository
from core.categories.schemas import CategoryCreate, CategoryGet
from core.users.api import current_user
from core.users.models import User

router = APIRouter()


@router.post("/")
async def create(
    data: CategoryCreate,
    user: User = Depends(current_user),
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategoryGet:
    try:
        category = await repository.create(data, user)
    except CategoryAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category has already exists."
        )
    return category
