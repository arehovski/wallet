from fastapi import APIRouter, Depends

from core.categories.repository import get_category_repository
from core.categories.schemas import CategoryCreate
from core.users.api import current_user

router = APIRouter()


@router.post("/")
def create(user: Depends(current_user), data: CategoryCreate, repository: Depends(get_category_repository)):
    pass
