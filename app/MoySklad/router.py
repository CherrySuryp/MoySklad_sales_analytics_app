from fastapi import APIRouter, Depends

from app.MoySklad.dependecies import check_ms_token_validity

router = APIRouter(
    prefix='/MoySklad',
    tags=['Moy Sklad'],
    dependencies=[Depends(check_ms_token_validity)]
)
