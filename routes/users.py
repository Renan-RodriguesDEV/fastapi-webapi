from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.config.config import get_session
from database.models.user import User
from database.schemas.user import UserSchema, UserSchemaList
from routes.auth import get_current_user, hash_password

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=UserSchemaList)
def read_users(
    curren_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return {"status": status.HTTP_200_OK, "users": session.query(User).all()}


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(user: UserSchema, session: Session = Depends(get_session)):
    nw_user = User(user.username, hash_password(user.password))
    session.add(nw_user)
    session.commit()
    session.refresh(nw_user)
    return nw_user


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
