from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.config.config import get_session
from database.models.user import User
from database.schemas.user import (
    UserSchema,
    UserSchemaList,
    UserSchemaPatch,
    UserSchemaPublic,
)
from security.auth import get_current_user, hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserSchemaList)
def read_users(
    curren_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return {"status": status.HTTP_200_OK, "users": session.query(User).all()}


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=UserSchemaPublic)
def read_user(
    _id: int,
    curren_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if _id != curren_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Your dont access was user"
        )
    return curren_user


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: UserSchema, session: Session = Depends(get_session)):
    nw_user = User(user.username, hash_password(user.password))
    session.add(nw_user)
    session.commit()
    session.refresh(nw_user)
    return nw_user


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=UserSchemaPublic)
def put(
    id: int,
    user: UserSchema,
    curren_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if id != curren_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    curren_user.username = user.username
    curren_user.password = hash_password(user.password)
    session.commit()
    session.refresh(curren_user)
    return curren_user


@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=UserSchemaPublic)
def patch(
    id: int,
    user: UserSchemaPatch,
    curren_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if id != curren_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )
    # converte o user_data apenas para os campos que
    # foram passado no user. ex: {'username':'my_username'}
    user_data = user.model_dump(exclude_unset=True)
    # itera sobre chave e valores de user_data
    for field, value in user_data.items():
        # altera o atributo do obj (curren_user:User)
        # no campo (field) pelo novo valor (value) de user_data
        if field == "password":
            setattr(curren_user, field, hash_password(value))
        else:
            setattr(curren_user, field, value)
    session.commit()
    session.refresh(curren_user)
    return curren_user


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    if id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="your dont can delete is user"
        )
    user = session.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED)
    session.delete(user)
    session.commit()
    return {
        "status": status.HTTP_204_NO_CONTENT,
        "message": "successfully in delete user",
    }
