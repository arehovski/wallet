from fastapi import APIRouter, Depends

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
    category_dict = data.dict()
    category_dict["user_id"] = user.id
    category = await repository.create(category_dict)
    return category
