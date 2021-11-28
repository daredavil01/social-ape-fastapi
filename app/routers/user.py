from fastapi import status, HTTPException, APIRouter
from fastapi.params import Depends
from sqlalchemy import exc
from sqlalchemy.exc import IntegrityError

from .. import models, schemas
from ..database import SessionLocal, get_db
from .. import utils

router = APIRouter(
    prefix='/users',
    tags=["Users"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate,  db: SessionLocal = Depends(get_db)):
    try:
        user.password = utils.hash(user.password)
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: SessionLocal = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} not found")
    return user
