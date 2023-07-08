from fastapi import APIRouter, Depends
from app.dependencies import check_api_token
from app.users.dao import UsersDAO

router = APIRouter(
    prefix='/MoySklad',
    tags=['Moy Sklad'],
    dependencies=Depends(check_api_token)
)


@router.post('/{user_id}/update_items')
def get_items_from_ms(user_id: int):
    ms_token = UsersDAO.find_one_or_none(id=user_id)
