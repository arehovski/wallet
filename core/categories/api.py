from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from core.categories.exceptions import CategoryAlreadyExists
from core.categories.models import CategoryType
from core.categories.repository import get_category_repository, CategoryRepository
from core.categories.schemas import CategoryCreate, CategorySchema, CategoryUpdate
from core.users.api import current_user
from core.users.models import User

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    name="category:create",
    response_model=CategorySchema,
    responses={
        status.HTTP_400_BAD_REQUEST: {
            "content": {
                "application/json": {
                    "examples": {
                        "Category has already exists.": {
                            "summary": "A category for this user has already exists.",
                            "value": {"detail": CategoryAlreadyExists("Salary").msg},
                        },
                    }
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


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    name="category:list",
    response_model=list[CategorySchema]
)
async def categories_list(
    category_type: CategoryType | None = None,
    user: User = Depends(current_user),
    repository: CategoryRepository = Depends(get_category_repository),
) -> list[CategorySchema]:
    return await repository.categories_list(user, category_type)


@router.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    name="category:update",
    response_model=CategorySchema
)
async def update(
    id: int,
    data: CategoryUpdate,
    user: User = Depends(current_user),
    repository: CategoryRepository = Depends(get_category_repository),
) -> CategorySchema:
    return await repository.update(id, user, data) #TODO
